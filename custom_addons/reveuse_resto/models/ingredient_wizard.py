from odoo import models, fields, api

class IngredientWizard(models.TransientModel):
    _name = 'reveuse_resto.ingredient.wizard'
    _description = 'Wizard Konfirmasi Bahan Baku'

    kitchen_order_id = fields.Many2one('reveuse_resto.kitchen_order')
    pos_order_id = fields.Many2one('pos.order')
    line_ids = fields.One2many('reveuse_resto.ingredient.wizard.line', 'wizard_id', string='Bahan')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        kitchen_id = self._context.get('default_kitchen_order_id')
        if kitchen_id:
            kitchen_order = self.env['reveuse_resto.kitchen_order'].browse(kitchen_id)
            lines = []
            if kitchen_order.pos_order_id:
                for order_line in kitchen_order.pos_order_id.lines:
                    # Cari BoM otomatis
                    bom = self.env['mrp.bom'].sudo().search([
                        ('type', '=', 'phantom'),
                        '|', ('product_id', '=', order_line.product_id.id),
                        '&', ('product_id', '=', False), ('product_tmpl_id', '=', order_line.product_id.product_tmpl_id.id)
                    ], limit=1)
                    if bom:
                        for bom_line in bom.bom_line_ids:
                            lines.append((0, 0, {
                                'product_id': bom_line.product_id.id,
                                'qty_used': (bom_line.product_qty / (bom.product_qty or 1.0)) * order_line.qty,
                                'uom_id': bom_line.product_uom_id.id,
                            }))
            res.update({'line_ids': lines})
        return res

    def action_confirm(self):
        for line in self.line_ids:
            self.env['reveuse_resto.kitchen_ingredient_usage'].create({
                'order_id': self.kitchen_order_id.id,
                'pos_order_id': self.pos_order_id.id,
                'pos_reference': self.pos_order_id.pos_reference or self.pos_order_id.name, # Ambil Ref Transaksi
                'ingredient_product_id': line.product_id.id,
                'ingredient_name': line.product_id.display_name,
                'qty_used': line.qty_used,
                'uom_id': line.uom_id.id,
            })
        self.kitchen_order_id.status = 'done'

class IngredientWizardLine(models.TransientModel):
    _name = 'reveuse_resto.ingredient.wizard.line'
    _description = 'Line Wizard Bahan'
    wizard_id = fields.Many2one('reveuse_resto.ingredient.wizard')
    product_id = fields.Many2one('product.product', string="Bahan")
    qty_used = fields.Float(string="Kuantitas")
    uom_id = fields.Many2one('uom.uom', string="Satuan")