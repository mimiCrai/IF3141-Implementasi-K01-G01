from odoo import models, fields, api

class ManagementOverview(models.Model):
    _name = 'reveuse_resto.management_overview'
    _description = 'Managerial Overview Model'

    name = fields.Char(string='Name', default='Managerial Overview')
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

    total_staff = fields.Integer(string='Active Staff', compute='_compute_total_staff')
    
    pengguna_ids = fields.Many2many('reveuse_resto.pengguna', string='Daftar Staff', compute='_compute_pengguna_ids')

    def _compute_total_staff(self):
        for record in self:
            record.total_staff = self.env['reveuse_resto.pengguna'].search_count([])

    def _compute_pengguna_ids(self):
        for record in self:
            record.pengguna_ids = self.env['reveuse_resto.pengguna'].search([])