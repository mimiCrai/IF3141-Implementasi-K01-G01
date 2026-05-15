import logging
from odoo import models

_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = "pos.order"

    def _should_create_picking_real_time(self):
        return True

    def _get_pos_ingredient_lines(self):
        self.ensure_one()
        bom_model = self.env["mrp.bom"].sudo()
        ingredient_lines = []

        for order_line in self.lines:
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
                ingredient_lines.append({
                    "menu_product": product,
                    "menu_qty": order_line.qty,
                    "ingredient_product": bom_line.product_id,
                    "qty_used": qty_used,
                    "uom": bom_line.product_uom_id,
                })

        return ingredient_lines

    def _format_ingredients_needed(self):
        self.ensure_one()
        totals = {}
        for line in self._get_pos_ingredient_lines():
            key = (line["ingredient_product"].id, line["uom"].id)
            if key not in totals:
                totals[key] = {
                    "product": line["ingredient_product"],
                    "qty": 0.0,
                    "uom": line["uom"],
                }
            totals[key]["qty"] += line["qty_used"]

        return "\n".join(
            "%s %s %s" % (
                ("%g" % value["qty"]),
                value["uom"].name,
                value["product"].display_name,
            )
            for value in totals.values()
        )

    def _log_ingredient_usage(self):
        usage_model = self.env["reveuse_resto.kitchen_ingredient_usage"].sudo()

        for order in self:
            usage_model.search([("pos_order_id", "=", order.id)]).unlink()
            usage_vals = []

            for line in order._get_pos_ingredient_lines():
                usage_vals.append({
                    "name": "%s - %s" % (order.name, line["ingredient_product"].display_name),
                    "pos_order_id": order.id,
                    "pos_reference": order.pos_reference or order.name,
                    "usage_datetime": order.date_order,
                    "menu_product_id": line["menu_product"].id,
                    "menu_qty": line["menu_qty"],
                    "ingredient_product_id": line["ingredient_product"].id,
                    "ingredient_name": line["ingredient_product"].display_name,
                    "qty_used": line["qty_used"],
                    "uom_id": line["uom"].id,
                    "unit": line["uom"].name,
                })

            if usage_vals:
                usage_model.create(usage_vals)

    def _create_kitchen_order(self):
        kitchen_model = self.env["reveuse_resto.kitchen_order"].sudo()
        
        for order in self:
            kitchen_model.search([("pos_order_id", "=", order.id)]).unlink()
            items = []
            for line in order.lines:
                items.append("%g x %s" % (line.qty, line.product_id.display_name))
            
            item_summary = " \n".join(items)
            
            table_no = "Walk-in"
            if hasattr(order, 'table_id') and order.table_id:
                table_no = order.table_id.name
            
            kitchen_model.create({
                "name": order.pos_reference or order.name,
                "table_number": table_no,
                "status": "waiting",
                "item_summary": item_summary,
                "ingredients_needed": order._format_ingredients_needed() or "Tidak ada BoM Kit untuk item ini",
            })

    def _process_order(self, order, draft, existing_order):
        pos_order = super()._process_order(order, draft, existing_order)
        order_record = self.browse(pos_order)
        if not draft:
            order_record._log_ingredient_usage()
            order_record._create_kitchen_order()
            _logger.info(
                "Kalkulasi bahan baku untuk pesanan POS %s sedang diproses di belakang layar",
                order_record.name,
            )
        return pos_order
