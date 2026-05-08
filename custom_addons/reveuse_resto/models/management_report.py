from odoo import models, fields

class ManagementReport(models.TransientModel):
    _name = 'reveuse_resto.management_report'
    _description = 'Form Cetak Laporan Stok'

    tanggal_mulai = fields.Date(string='Periode Mulai', required=True)
    tanggal_akhir = fields.Date(string='Periode Akhir', required=True)

    def action_view_report(self):
        self.ensure_one()
        domain = [
            ('tanggal', '>=', self.tanggal_mulai),
            ('tanggal', '<=', self.tanggal_akhir)
        ]
        return {
            'name': 'Laporan Mutasi Stok (%s s/d %s)' % (self.tanggal_mulai, self.tanggal_akhir),
            'type': 'ir.actions.act_window',
            'res_model': 'reveuse_resto.transaksi',
            'view_mode': 'tree,form',
            'domain': domain,
            'context': {'create': False, 'edit': False, 'delete': False},
            'target': 'current',
        }

    def action_print_pdf(self):
        self.ensure_one()
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'tanggal_mulai': self.tanggal_mulai,
                'tanggal_akhir': self.tanggal_akhir,
            },
        }
        return self.env.ref('reveuse_resto.action_report_stok_pdf').report_action(self, data=data)