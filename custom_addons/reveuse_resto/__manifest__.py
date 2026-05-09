{
    "name": "Reveuse Resto",
    "version": "1.0",
    "summary": "Restaurant stock monitoring and transaction logging",
    "description": "Reveuse Resto module for monitoring bahan baku stock.",
    "category": "Inventory",
    "author": "K01 G01",
    "depends": ["base", "mail", "stock", "mrp", "point_of_sale"],
    "data": [
        "security/security_groups.xml",
        "security/ir.model.access.csv",
        "views/bahan_baku_views.xml",
        "views/kitchen_monitor_views.xml",
        "views/reporting_views.xml",
        # "views/notification_setting_views.xml",
        "views/management_report_views.xml",
        "views/templates.xml",
        "views/transaksi_views.xml",
        "reports/stock_report_view.xml",
        "reports/stock_report.xml",
        "data/demo_resto_data.xml",
        "views/menu_views.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "reveuse_resto/static/src/css/style.scss",
            "reveuse_resto/static/src/js/stock_dashboard.js",
            "reveuse_resto/static/src/xml/*.xml"
        ]
    },
    "application": True,
    "installable": True
}
