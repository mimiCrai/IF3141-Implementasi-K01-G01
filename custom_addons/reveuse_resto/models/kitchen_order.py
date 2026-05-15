from odoo import fields, models

class KitchenOrder(models.Model):
    _name = "reveuse_resto.kitchen_order"
    _description = "Kitchen Order Data"

    name = fields.Char(string="Order ID", required=True, default="New Order")
    # Field ini dibutuhkan untuk menghubungkan ke data POS asli
    pos_order_id = fields.Many2one("pos.order", string="POS Order Source")
    table_number = fields.Char(string="Table", default="T-01")
    status = fields.Selection(
        selection=[("waiting", "Waiting"), ("on_progress", "On Progress"), ("done", "Done")],
        string="Status",
        default="waiting",
        required=True,
    )
    item_summary = fields.Char(string="Menu Items")
    # Field ini harus ada karena dipanggil di XML
    ingredients_needed = fields.Text(string="Ingredients Needed")
    elapsed_display = fields.Char(string="Elapsed", default="00:00")

    def action_start_progress(self):
        for record in self:
            record.status = 'on_progress'

    def action_mark_done(self):
        self.ensure_one()
        # Mengembalikan aksi untuk membuka Wizard Popup
        return {
            'name': 'Konfirmasi Penggunaan Bahan',
            'type': 'ir.actions.act_window',
            'res_model': 'reveuse_resto.ingredient.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_kitchen_order_id': self.id,
                'default_pos_order_id': self.pos_order_id.id,
            }
        }