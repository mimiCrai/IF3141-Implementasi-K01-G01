/** @odoo-module **/

import { registry } from "@web/core/registry";

const stockDashboardService = {
    start() {
        // Placeholder service for future realtime stock dashboard extension.
        return {};
    },
};

registry.category("services").add("reveuse_resto_stock_dashboard", stockDashboardService);
