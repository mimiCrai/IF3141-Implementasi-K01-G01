from odoo import fields, models


class KitchenOrder(models.Model):
    _name = "reveuse_resto.kitchen_order"
    _description = "Kitchen Order Mock Data"

    name = fields.Char(string="Order ID", required=True, default="ORD-MOCK-001")
    table_number = fields.Char(string="Table", default="T-01")
    status = fields.Selection(
        selection=[("waiting", "Waiting"), ("on_progress", "On Progress")],
        string="Status",
        default="waiting",
        required=True,
    )
    item_summary = fields.Char(string="Items", default="Sample Item x1")
    elapsed_display = fields.Char(string="Elapsed", default="00:05")
