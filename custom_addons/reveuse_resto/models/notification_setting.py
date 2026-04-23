from odoo import models, fields


class NotificationSetting(models.Model):
    _name = 'reveuse_resto.notification_setting'
    _description = 'Mock Notification Setting'

    name = fields.Char(string='Setting Name', default='Default Notification Center')
    