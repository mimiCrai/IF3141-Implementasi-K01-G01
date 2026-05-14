from odoo import models, fields, api

class Pengguna(models.Model):
    _name = 'reveuse_resto.pengguna'
    _description = 'Data Master Pengguna'

    name = fields.Char(string='Nama Lengkap', required=True) 
    id_pengguna = fields.Char(string='ID Pengguna', required=True)    
    user_id = fields.Many2one('res.users', string="User Akun") # Tetap ada di DB, tapi nanti disembunyikan dari layar
    email = fields.Char(string='Email (Login)', required=True) # Jadikan required buat login
    no_telp = fields.Char(string='Nomor Telepon')

    peran = fields.Selection([
        ('kasir', 'Kasir'),
        ('kitchen', 'Kitchen Staff'),
        ('warehouse', 'Divisi Warehouse'),
        ('manager', 'Assistant Manager')
    ], string='Peran', required=True)
    password = fields.Char(string='Password', required=True)
    status_notif = fields.Boolean(string='Terima Notifikasi Minimum', default=False)

    # 1. FUNGSI OTOMATIS BIKIN AKUN SAAT DATA BARU DIBUAT
    @api.model
    def create(self, vals):
        # 1. Simpan data staf ke tabel custom kita (Reveuse Resto)
        record = super(Pengguna, self).create(vals)
        
        group_map = {
            'kasir': 'reveuse_resto.group_kasir',
            'warehouse': 'reveuse_resto.group_warehouse',
            'kitchen': 'reveuse_resto.group_kitchen',
            'manager': 'reveuse_resto.group_assistant_manager',
        }

        # 2. Bikin akun Odoo pakai ID Pengguna sebagai Username Login
        if record.id_pengguna and record.peran in group_map:
            group = self.env.ref(group_map[record.peran], raise_if_not_found=False)
            
            new_user = self.env['res.users'].create({
                'name': record.name,
                'login': record.id_pengguna, # <-- KUNCI PERUBAHAN: Pakai ID Pengguna buat login
                'password': record.password,
                'email': record.email,       # <-- Simpan email asli di data user Odoo juga (opsional tapi bagus)
                'groups_id': [(4, group.id)] if group else []
            })
            
            # 3. Link akun Odoo ke profil staf
            record.user_id = new_user.id
            
        return record

    # 2. FUNGSI OTOMATIS UPDATE GRUP KALAU ROLE DIGANTI (Yang kemarin)
    @api.onchange('peran')
    def _sync_user_groups(self):
        for record in self:
            if not record.user_id:
                continue
            
            group_map = {
                'kasir': 'reveuse_resto.group_kasir',
                'warehouse': 'reveuse_resto.group_warehouse',
                'kitchen': 'reveuse_resto.group_kitchen',
                'manager': 'reveuse_resto.group_assistant_manager',
            }

            all_groups = [self.env.ref(g, raise_if_not_found=False) for g in group_map.values()]
            record.user_id.write({'groups_id': [(3, g.id) for g in all_groups if g]})

            if record.peran in group_map:
                new_group = self.env.ref(group_map[record.peran], raise_if_not_found=False)
                if new_group:
                    record.user_id.write({'groups_id': [(4, new_group.id)]})

    def action_open_user_detail(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'User Detail',
            'res_model': 'reveuse_resto.pengguna',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }