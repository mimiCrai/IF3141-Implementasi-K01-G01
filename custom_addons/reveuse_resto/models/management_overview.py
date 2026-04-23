from odoo import fields, models


class ManagementOverview(models.Model):
    _name = "reveuse_resto.management_overview"
    _description = "Management Overview Mock Data"

    name = fields.Char(string="Overview Ref", required=True, default="MGT-OVR-001")
    branch = fields.Char(string="Branch", default="Bandung Central")
    orders_count = fields.Integer(string="Orders", default=242)
    avg_ticket = fields.Char(string="Avg Ticket", default="Rp 86.000")
    waste_ratio = fields.Char(string="Waste", default="2.1%")
    health_flag = fields.Selection(
        selection=[("healthy", "Healthy"), ("watch", "Watch"), ("review", "Review")],
        string="Flag",
        default="healthy",
    )
    manager_note = fields.Text(string="Manager Note")
