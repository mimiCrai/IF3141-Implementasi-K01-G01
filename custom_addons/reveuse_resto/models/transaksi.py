from odoo import fields, models


class Transaksi(models.Model):
    _name = "reveuse_resto.transaksi"
    _description = "Reveuse Riwayat Transaksi Mock Model"

    name = fields.Char(string="Name", required=True, default="Riwayat Transaksi Mock Record")
