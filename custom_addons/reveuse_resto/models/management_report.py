from odoo import models, fields

class ManagementReport(models.TransientModel):
    _name = 'reveuse_resto.management_report'
    _description = 'Form Cetak Laporan Stok'

    tanggal_mulai = fields.Date(string='Periode Mulai', required=True)
    tanggal_akhir = fields.Date(string='Periode Akhir', required=True)

    def action_print_pdf(self):
        self.ensure_one()
        return self.env.ref('reveuse_resto.action_report_stok_pdf').report_action(self)