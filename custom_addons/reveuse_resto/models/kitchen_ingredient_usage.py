from odoo import api, fields, models

class KitchenIngredientUsage(models.Model):
    _name = "reveuse_resto.kitchen_ingredient_usage"
    _description = "Kitchen Ingredient Usage"
    _order = "usage_datetime desc, id desc"

    # ... (Keep your existing fields here) ...
    name = fields.Char(string="Usage Ref", required=True, default="/")
    order_id = fields.Many2one("reveuse_resto.kitchen_order", string="Kitchen Order")
    pos_order_id = fields.Many2one("pos.order", string="POS Order", ondelete="cascade")
    pos_reference = fields.Char(string="POS Ref")
    usage_datetime = fields.Datetime(string="Waktu", default=fields.Datetime.now, required=True)
    menu_product_id = fields.Many2one("product.product", string="Menu")
    menu_qty = fields.Float(string="Jumlah Menu")
    ingredient_product_id = fields.Many2one("product.product", string="Bahan")
    ingredient_name = fields.Char(string="Ingredient")
    qty_used = fields.Float(string="Used Qty", default=1.0)
    uom_id = fields.Many2one("uom.uom", string="Unit of Measure")
    unit = fields.Char(string="Unit")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            # Integration logic: Find the warehouse item by name and deduct stock
            if record.ingredient_name:
                bahan = self.env['reveuse_resto.bahan_baku'].search([
                    ('name', '=ilike', record.ingredient_name)
                ], limit=1)
                if bahan:
                    bahan.stok_sekarang -= record.qty_used
        return records