from odoo import fields, models


class KitchenIngredientUsage(models.Model):
    _name = "reveuse_resto.kitchen_ingredient_usage"
    _description = "Kitchen Ingredient Usage Mock Data"

    name = fields.Char(string="Usage Ref", required=True, default="KITCHEN-USG-001")
    order_id = fields.Many2one("reveuse_resto.kitchen_order", string="Kitchen Order")
    ingredient_name = fields.Char(string="Ingredient", default="Beef")
    qty_used = fields.Float(string="Used Qty", default=1.0)
    unit = fields.Char(string="Unit", default="kg")
