from odoo import models, fields

class BahanBaku(models.Model):
    _name = 'reveuse_resto.bahan_baku'
    _description = 'Data Master Bahan Baku'

    name = fields.Char(string='Nama Bahan', required=True)
    id_bahan = fields.Char(string='ID Bahan', required=True)
    kategori = fields.Selection([
        ('sayur', 'Sayuran'),
        ('daging', 'Daging'),
        ('bumbu', 'Bumbu'),
        ('minuman', 'Minuman')
    ], string='Kategori', required=True)
    stok_sekarang = fields.Integer(string='Stok Saat Ini', default=0)
    batas_minimum = fields.Integer(string='Batas Minimum Stok', default=5)
    satuan = fields.Char(string='Satuan (Contoh: kg, liter)', required=True)