from odoo import fields, models


class BahanBaku(models.Model):
    _name = "reveuse_resto.bahan_baku"
    _description = "Reveuse Warehouse Mock Model"

    name = fields.Char(string="Name", required=True, default="Warehouse Mock Record")
