from odoo import models, api

class ReportMutasiStok(models.AbstractModel):
    _name = 'report.reveuse_resto.report_stok_template'
    _description = 'Parser Laporan Mutasi Stok'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['reveuse_resto.management_report'].browse(docids)
        mutasi_list = []
        
        for doc in docs:
            penerimaan = self.env['reveuse_resto.penerimaan'].search([
                ('tanggal', '>=', doc.tanggal_mulai),
                ('tanggal', '<=', doc.tanggal_akhir)
            ])
            for p in penerimaan:
                mutasi_list.append({
                    'tanggal': p.tanggal,
                    'ref': p.id_penerimaan,
                    'ket': 'Penerimaan Bahan',
                    'bahan': p.bahan_id.name,
                    'qty': p.stok_masuk,
                    'sign': '+',
                    'tipe': 'masuk'
                })
                
            penggunaan = self.env['reveuse_resto.kitchen_ingredient_usage'].search([
                ('usage_datetime', '>=', doc.tanggal_mulai),
                ('usage_datetime', '<=', doc.tanggal_akhir)
            ])
            for u in penggunaan:
                mutasi_list.append({
                    'tanggal': u.usage_datetime.date(),
                    'ref': u.pos_reference or u.name,
                    'ket': 'Penggunaan Dapur',
                    'bahan': u.ingredient_name,
                    'qty': u.qty_used,
                    'sign': '-',
                    'tipe': 'keluar'
                })
        
        mutasi_list.sort(key=lambda x: x['tanggal'], reverse=True)
        
        return {
            'docs': docs,
            'mutasi_list': mutasi_list,
        }