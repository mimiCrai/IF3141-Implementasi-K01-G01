from odoo import models, fields

class Pengguna(models.Model):
    _name = 'reveuse_resto.pengguna'
    _description = 'Data Master Pengguna'

    name = fields.Char(string='Nama Lengkap', required=True) 
    id_pengguna = fields.Char(string='ID Pengguna', required=True)    
    email = fields.Char(string='Email')
    no_telp = fields.Char(string='Nomor Telepon')

    peran = fields.Selection([
        ('kasir', 'Kasir'),
        ('kitchen', 'Kitchen Staff'),
        ('warehouse', 'Divisi Warehouse'),
        ('manager', 'Assistant Manager')
    ], string='Peran', required=True)
    password = fields.Char(string='Password')
    status_notif = fields.Boolean(string='Terima Notifikasi Minimum', default=False)