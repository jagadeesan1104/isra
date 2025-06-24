import frappe
import pandas as pd
from io import BytesIO
from frappe.desk.query_report import run
from datetime import date

@frappe.whitelist()
def export_gross_profit_excel():
	# try:
	form_params = frappe._dict(frappe.local.form_dict)
	data = run("Gross Profit", form_params.filters, are_default_filters=False)
	data = frappe._dict(data)
	total = data.get("result")[-1] if len(data.get("result")) > 0 else []
	# total["parent_invoice"] = total.get("sales_invoice")
	# del total["sales_invoice"]
	records = data.get("result")[:-1]
	column_list = data.get("columns")
	column_list[0] = {"fieldname": "parent_invoice", "label": "Sales Invoice"}
	column_list.insert(1, {"fieldname": "item_code", "label": "Item"})
	column_list.pop()
	columns = [column.get("fieldname") for column in column_list]
	labels = {col.get("fieldname"):col.get("label") for col in column_list}
	records = [row for row in records if row.get("indent") == 1]

	for row in records:
		for key in list(row.keys()):
			if key not in columns:
				del row[key]
			elif row[key] is None:
				row[key] = ""
			elif isinstance(row[key], date):
				row[key] = row[key].strftime('%d-%m-%Y')

	records.append(total)
	records_dict = {}
	records_dict = {}
	for index, key in enumerate(columns):
		records_dict[key] = []
		for row in records:
			if isinstance(row, dict):
				records_dict[key].append(row.get(key))
			else:
				records_dict[key].append(row[index])
	df = pd.DataFrame(records_dict)
	df.rename(columns=labels, inplace=True)

	output = BytesIO()
	with pd.ExcelWriter(output, engine='openpyxl') as writer:
		df.to_excel(writer, index=False, sheet_name='Report')

	frappe.local.response.filename = "Gross Profit.xlsx"
	frappe.local.response.filecontent = output.getvalue()
	frappe.local.response.type = "binary"
	# except Exception as err:
	# 	frappe.log_error(title="GP Custom Invoice Excel Export Issue", message=f"{err}")
	# 	return err

