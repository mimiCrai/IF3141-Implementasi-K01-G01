from odoo import api, fields, models
from odoo.exceptions import ValidationError

class BahanBaku(models.Model):
    _name = 'reveuse_resto.bahan_baku'
    _description = 'Data Master Bahan Baku'

    _sql_constraints = [
        ('unique_id_bahan', 'unique(id_bahan)', 'ID Bahan harus unik.'),
    ]

    name = fields.Char(string='Nama Bahan', required=True)
    id_bahan = fields.Char(
        string='ID Bahan',
        required=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('reveuse_resto.bahan_baku')
    )
    kategori = fields.Selection([
        ('sayur', 'Sayuran'),
        ('daging', 'Daging'),
        ('bumbu', 'Bumbu'),
        ('minuman', 'Minuman')
    ], string='Kategori', required=True)
    stok_sekarang = fields.Integer(string='Stok Saat Ini', default=0)
    batas_minimum = fields.Integer(string='Batas Minimum Stok', default=5)
    satuan_id = fields.Many2one('uom.uom', string='Satuan', required=True)

    @api.constrains('stok_sekarang', 'batas_minimum')
    def _check_non_negative_stock(self):
        for record in self:
            if record.stok_sekarang < 0:
                raise ValidationError('Stok Saat Ini tidak boleh negatif.')
            if record.batas_minimum < 0:
                raise ValidationError('Batas Minimum Stok tidak boleh negatif.')