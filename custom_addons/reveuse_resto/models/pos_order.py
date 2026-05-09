import logging

from odoo import models

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = "pos.order"

    def _should_create_picking_real_time(self):
        return True

    def _log_ingredient_usage(self):
        usage_model = self.env["reveuse_resto.kitchen_ingredient_usage"].sudo()
        bom_model = self.env["mrp.bom"].sudo()

        for order in self:
            usage_model.search([("pos_order_id", "=", order.id)]).unlink()
            usage_vals = []

            for order_line in order.lines:
                product = order_line.product_id
                bom = bom_model.search([
                    ("type", "=", "phantom"),
                    "|",
                    ("product_id", "=", product.id),
                    "&",
                    ("product_id", "=", False),
                    ("product_tmpl_id", "=", product.product_tmpl_id.id),
                ], limit=1)
                if not bom:
                    continue

                bom_qty = bom.product_qty or 1.0
                for bom_line in bom.bom_line_ids:
                    qty_used = (bom_line.product_qty / bom_qty) * order_line.qty
                    usage_vals.append({
                        "name": "%s - %s" % (order.name, bom_line.product_id.display_name),
                        "pos_order_id": order.id,
                        "pos_reference": order.pos_reference or order.name,
                        "usage_datetime": order.date_order,
                        "menu_product_id": product.id,
                        "menu_qty": order_line.qty,
                        "ingredient_product_id": bom_line.product_id.id,
                        "ingredient_name": bom_line.product_id.display_name,
                        "qty_used": qty_used,
                        "uom_id": bom_line.product_uom_id.id,
                        "unit": bom_line.product_uom_id.name,
                    })

            if usage_vals:
                usage_model.create(usage_vals)

    def _process_order(self, order, draft, existing_order):
        pos_order = super()._process_order(order, draft, existing_order)
        order_record = self.browse(pos_order) if isinstance(pos_order, int) else pos_order
        if not draft:
            order_record._log_ingredient_usage()
        order_ref = order_record.name or order.get("name") or order.get("uid") or "POS Order"
        _logger.info(
            "Kalkulasi bahan baku untuk pesanan POS %s sedang diproses di belakang layar",
            order_ref,
        )
        return pos_order
