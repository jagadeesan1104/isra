// Copyright (c) 2025, isra and contributors
// For license information, please see license.txt

frappe.query_reports["Item Stock Info"] = {
	"filters": [
		{
			"fieldname":"item",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse"
		},
		{
			"fieldname":"group_by",
			"label": __("Group By"),
			"fieldtype": "Select",
			"options": "\nItem Code"
		}
	],
	"formatter": function (value, row, column, data, default_formatter) {
		if (column.id == "actual_qty") {
			if (row.length === 7){
				threshold_qty = row[5].content
				actual_qty = row[6].content
			}
			else if (row.length === 6){
				threshold_qty = row[4].content
				actual_qty = row[5].content
			}
			if (threshold_qty >= actual_qty) {
				value = "<span style='color:#FF0000!important;font-weight:bold'>" + actual_qty + "</span>";
			}
		}
		return value;
	},
};
