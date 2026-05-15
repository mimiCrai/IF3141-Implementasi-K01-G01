from odoo import api, fields, models
from odoo.exceptions import ValidationError

class BahanBaku(models.Model):
    _name = 'reveuse_resto.bahan_baku'
    _description = 'Data Master Bahan Baku'

    _sql_constraints = [
        ('unique_id_bahan', 'unique(id_bahan)', 'ID Bahan harus unik.'),
    ]

    name = fields.Char(string='Nama Bahan', required=True)
    id_bahan = fields.Char(
        string='ID Bahan',
        required=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('reveuse_resto.bahan_baku')
    )
    kategori = fields.Selection([
        ('sayur', 'Sayuran'),
        ('daging', 'Daging'),
        ('bumbu', 'Bumbu'),
        ('minuman', 'Minuman')
    ], string='Kategori', required=True)
    product_id = fields.Many2one(
        'product.product',
        string='Produk Inventory',
        domain="[('type', '=', 'product')]",
        help='Produk stok Odoo yang dipakai oleh Inventory, Manufacturing BoM, dan POS.',
    )
    stok_sekarang = fields.Float(
        string='Stok Saat Ini',
        compute='_compute_stok_sekarang',
        digits='Product Unit of Measure',
    )
    batas_minimum = fields.Integer(string='Batas Minimum Stok', default=5)
    satuan_id = fields.Many2one(
        'uom.uom',
        string='Satuan',
        compute='_compute_satuan_id',
        store=True,
        readonly=False,
        required=True,
    )

    @api.depends('product_id.qty_available')
    def _compute_stok_sekarang(self):
        for record in self:
            record.stok_sekarang = record.product_id.qty_available if record.product_id else 0.0

    @api.depends('product_id.uom_id')
    def _compute_satuan_id(self):
        for record in self:
            if record.product_id:
                record.satuan_id = record.product_id.uom_id

    def _prepare_inventory_product_vals(self):
        self.ensure_one()
        return {
            'name': self.name,
            'detailed_type': 'product',
            'uom_id': self.satuan_id.id,
            'uom_po_id': self.satuan_id.id,
        }

    def _ensure_inventory_product(self):
        Product = self.env['product.product'].sudo()
        for record in self:
            if not record.product_id and record.satuan_id:
                record.product_id = Product.create(record._prepare_inventory_product_vals())

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('product_id') and not vals.get('satuan_id'):
                product = self.env['product.product'].browse(vals['product_id'])
                vals['satuan_id'] = product.uom_id.id
        records = super().create(vals_list)
        records._ensure_inventory_product()
        return records

    def write(self, vals):
        result = super().write(vals)
        self._ensure_inventory_product()
        product_vals = {}
        if 'name' in vals:
            product_vals['name'] = vals['name']
        if 'satuan_id' in vals:
            product_vals.update({
                'uom_id': vals['satuan_id'],
                'uom_po_id': vals['satuan_id'],
            })
        if product_vals:
            self.mapped('product_id').sudo().write(product_vals)
        if 'stok_sekarang' in vals:
            for record in self:
                if record.stok_sekarang <= record.batas_minimum:
                    record._send_low_stock_email()
                    
        return result

    @api.constrains('batas_minimum')
    def _check_non_negative_stock(self):
        for record in self:
            if record.batas_minimum < 0:
                raise ValidationError('Batas Minimum Stok tidak boleh negatif.')

    def _send_low_stock_email(self):
        # 1. Search the Pengguna model for managers who have notifications turned on
        managers = self.env['reveuse_resto.pengguna'].search([
            ('peran', '=', 'manager'),
            ('status_notif', '=', True)
        ])

        # 2. Extract their emails into a list, ignoring any users who forgot to put an email
        manager_emails = [m.email for m in managers if m.email]

        # 3. If there are no managers or no emails, stop the function so it doesn't crash
        if not manager_emails:
            print("No manager emails found. Skipping notification.")
            return

        email_string = ','.join(manager_emails)

        for record in self:
            subject = f"⚠️ Peringatan Stok Menipis: {record.name}"
            body = f"""
                <div style="font-family: Arial, sans-serif;">
                    <p>Halo Tim Manager,</p>
                    <p>Sistem mendeteksi bahwa stok untuk bahan baku <strong>{record.name}</strong> saat ini berada di bawah batas aman.</p>
                    <ul>
                        <li><strong>ID Bahan:</strong> {record.id_bahan}</li>
                        <li><strong>Kategori:</strong> {dict(self._fields['kategori'].selection).get(record.kategori)}</li>
                        <li><strong style="color: red;">Stok Saat Ini:</strong> {record.stok_sekarang} {record.satuan_id.name}</li>
                        <li><strong>Batas Minimum:</strong> {record.batas_minimum} {record.satuan_id.name}</li>
                    </ul>
                    <p>Harap segera menjadwalkan pembelian ulang (restock) untuk bahan ini.</p>
                </div>
            """
            
            mail_values = {
                'subject': subject,
                'body_html': body,
                'email_to': email_string,
                'email_from': 'reveuseresto@gmail.com',
            }
            
            # Create and send the email
            self.env['mail.mail'].sudo().create(mail_values).send()
