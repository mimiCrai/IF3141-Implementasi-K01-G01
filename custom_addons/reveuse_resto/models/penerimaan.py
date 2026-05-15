from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Penerimaan(models.Model):
    _name = 'reveuse_resto.penerimaan'
    _description = 'Penerimaan Bahan Baku'

    id_penerimaan = fields.Char(
        string='ID Penerimaan',
        required=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('reveuse_resto.penerimaan')
    )
    tanggal = fields.Date(string='Tanggal', default=fields.Date.context_today)
    bahan_id = fields.Many2one('reveuse_resto.bahan_baku', string='Bahan Baku', required=True)
    satuan_id = fields.Many2one(
        'uom.uom',
        string='Satuan',
        related='bahan_id.satuan_id',
        store=True,
        readonly=True
    )
    stok_masuk = fields.Integer(string='Stok Masuk', required=True)
    catatan = fields.Text(string='Catatan')

    @api.constrains('stok_masuk')
    def _check_stok_masuk(self):
        for record in self:
            if record.stok_masuk <= 0:
                raise ValidationError('Stok Masuk harus lebih besar dari 0.')

    def _apply_stock_delta(self, bahan, delta):
        if not bahan or not delta:
            return
        if not bahan.product_id:
            raise ValidationError('Bahan baku harus terhubung ke Produk Inventory sebelum menerima stok.')

        warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)], limit=1)
        location = warehouse.lot_stock_id or self.env.ref('stock.stock_location_stock')
        qty = bahan.satuan_id._compute_quantity(delta, bahan.product_id.uom_id)
        self.env['stock.quant']._update_available_quantity(bahan.product_id, location, qty)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            record._apply_stock_delta(record.bahan_id, record.stok_masuk)
        return records

    def write(self, vals):
        old_values = {record.id: (record.bahan_id, record.stok_masuk) for record in self}
        result = super().write(vals)
        for record in self:
            old_bahan, old_qty = old_values.get(record.id, (None, 0))
            if old_bahan == record.bahan_id:
                delta = record.stok_masuk - old_qty
                record._apply_stock_delta(record.bahan_id, delta)
            else:
                record._apply_stock_delta(old_bahan, -old_qty)
                record._apply_stock_delta(record.bahan_id, record.stok_masuk)
        return result

    def unlink(self):
        for record in self:
            record._apply_stock_delta(record.bahan_id, -record.stok_masuk)
        return super().unlink()
