from odoo import fields, models


class KitchenIngredientUsage(models.Model):
    _name = "reveuse_resto.kitchen_ingredient_usage"
    _description = "Kitchen Ingredient Usage"
    _order = "usage_datetime desc, id desc"

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
