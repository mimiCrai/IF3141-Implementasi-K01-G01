from odoo import models, fields

class Transaksi(models.Model):
    _name = 'reveuse_resto.transaksi'
    _description = 'Data Riwayat Transaksi'

    name = fields.Char(string='ID Transaksi', required=True)
    tanggal = fields.Date(string='Tanggal', default=fields.Date.context_today)
    jenis_transaksi = fields.Selection([
        ('masuk', 'Masuk (Penerimaan)'),
        ('keluar', 'Keluar (Penggunaan)')
    ], string='Jenis Transaksi', required=True)
    
    pengguna_id = fields.Many2one('reveuse_resto.pengguna', string='Penanggung Jawab')
    detail_ids = fields.One2many('reveuse_resto.detail.transaksi', 'transaksi_id', string='Rincian Bahan')

class DetailTransaksi(models.Model):
    _name = 'reveuse_resto.detail.transaksi'
    _description = 'Rincian Item Transaksi'
    transaksi_id = fields.Many2one('reveuse_resto.transaksi', string='Transaksi ID', ondelete='cascade')
    bahan_id = fields.Many2one('reveuse_resto.bahan_baku', string='Bahan Baku', required=True)
    kuantitas = fields.Integer(string='Kuantitas', required=True)