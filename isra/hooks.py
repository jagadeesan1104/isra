app_name = "isra"
app_title = "isra"
app_publisher = "isra"
app_description = "ISRA is a custom Frappe app developed by ISRA TRADING LLC to streamline business processes, optimize operations, and deliver specialized solutions tailored to the company\'s unique needs."
app_email = "isra@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "isra",
# 		"logo": "/assets/isra/logo.png",
# 		"title": "isra",
# 		"route": "/isra",
# 		"has_permission": "isra.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/isra/css/isra.css"
# app_include_js = "/assets/isra/js/isra.js"

# include js, css files in header of web template
# web_include_css = "/assets/isra/css/isra.css"
# web_include_js = "/assets/isra/js/isra.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "isra/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

app_include_js = [
    "/assets/isra/js/gross_profit_report.js"
]

# include js in doctype views
doctype_js = {
    # "Sales Order" : "public/js/sales_order.js",
    # "Sales Invoice" : "public/js/sales_order.js",
    "Payment Entry" : "public/js/payment_entry.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "isra/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "isra.utils.jinja_methods",
# 	"filters": "isra.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "isra.install.before_install"
# after_install = "isra.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "isra.uninstall.before_uninstall"
# after_uninstall = "isra.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "isra.utils.before_app_install"
# after_app_install = "isra.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "isra.utils.before_app_uninstall"
# after_app_uninstall = "isra.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "isra.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Warehouse": "isra.override.warehouse.CustomWarehouse"
}

# Document Events
# ---------------
# Hook on document methods and events

# # Add these lines to your hooks.py file

doc_events = {
    "Payment Entry": {
        "on_submit": "isra.override.payment_entry.update_invoice_status_after_submit",
        "on_cancel": "isra.override.payment_entry.update_invoice_status_on_cancel"
    },
    "Sales Invoice": {
        "validate": [
            "isra.override.sales_invoice.validate_item_uom",
            "isra.override.sales_invoice.validate_item_price_less_than_buying_price"
        ]
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"isra.tasks.all"
# 	],
# 	"daily": [
# 		"isra.tasks.daily"
# 	],
# 	"hourly": [
# 		"isra.tasks.hourly"
# 	],
# 	"weekly": [
# 		"isra.tasks.weekly"
# 	],
# 	"monthly": [
# 		"isra.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "isra.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "isra.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "isra.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["isra.utils.before_request"]
# after_request = ["isra.utils.after_request"]

# Job Events
# ----------
# before_job = ["isra.utils.before_job"]
# after_job = ["isra.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"isra.auth.validate"
# ]

# Boot session
# -----------
# boot_session = "isra.custom.boot_session"

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    # {
    # "dt": 'Property Setter',
	# 	"filters": [
	# 	["module","=", "ISRA"]
	# 	]
	# },
    # {
    # "dt": 'Print Format',
	# 	"filters": [
	# 	["module","=", "ISRA"]
	# 	]
	# },
    # {
    #     "dt": 'Warehouse Type',
	# },
    # {
    #     "dt": 'Workspace',
	# },
    # {
    #     "dt": 'Workflow',
	# },
    # {
    #     "dt": 'Workflow State',
	# },
    # {
    #     "dt": 'Workflow Action Master',
	# },
    {
        "dt": 'Client Script',
	},
    {
        "dt":"Letter Head",
    }
    # {
    #     "dt": 'Party Type',
	# }


]
