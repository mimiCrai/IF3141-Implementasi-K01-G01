from odoo import fields, models


class ManagementReport(models.Model):
    _name = 'reveuse_resto.management_report'
    _description = 'Management Report Mock'

    name = fields.Char(string='Report Title', default='Custom Period Report')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    
