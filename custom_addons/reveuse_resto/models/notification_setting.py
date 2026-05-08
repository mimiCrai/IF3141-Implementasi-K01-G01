from odoo import models, fields

class NotificationSetting(models.Model):
    _name = 'reveuse_resto.notification.setting'
    _description = 'Pengaturan Notifikasi Asisten Manajer'

    pengguna_id = fields.Many2one('reveuse_resto.pengguna', string='Pilih Akun', required=True)
    
    terima_notifikasi = fields.Boolean(
        related='pengguna_id.status_notif', 
        readonly=False, 
        string='Terima Peringatan Stok Minimum'
    )