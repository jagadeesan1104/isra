# Copyright (c) 2025, isra and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns= get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [{
			"fieldname":"item_code",
			"label": ("Item Name"),
			"fieldtype": "Link",
			"options": "Item",
			"width": 200
		},
		{
			"fieldname":"stock_uom",
			"label": ("UOM"),
			"fieldtype": "Link",
			"options": "UOM"
		},
		{
			"fieldname":"valuation_rate",
			"label": ("Valuation Rate"),
			"fieldtype": "Float",
			"precision": 3
		},
		{
			"fieldname":"threshold_qty",
			"label": ("Threshold Qty"),
			"fieldtype": "Int"
		},
		{
			"fieldname":"actual_qty",
			"label": ("In Stock Qty"),
			"fieldtype": "Int"
		}
		]
	if filters.get("group_by") != "Item Code":
		columns.insert(1, {
			"fieldname":"warehouse",
			"label": ("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 200
		})
	return columns

def get_data(filters):
	condition = ""
	if filters.get("item"):
		condition += f"""and i.name = "{filters.get('item')}" """
	if filters.get("warehouse"):
		condition += f"""and b.warehouse = "{filters.get('warehouse')}" """
	select = "select i.name as item_code, b.warehouse, i.stock_uom, ROUND(b.valuation_rate, 3) as valuation_rate, b.actual_qty, i.custom_threshold_stock as threshold_qty"
	group_by = ""
	if filters.get("group_by") == "Item Code":
		select = "select i.name as item_code, b.warehouse, i.stock_uom, ROUND(AVG(b.valuation_rate), 3) as valuation_rate, SUM(b.actual_qty) as actual_qty, i.custom_threshold_stock as threshold_qty"
		group_by = "group by i.name"
	query = f"""
		{select}
		from `tabItem` as i
		join `tabBin` as b on b.item_code = i.name
		where is_stock_item = 1 {condition}
		{group_by}
	"""
	data = frappe.db.sql(query, as_dict=True)
	return data