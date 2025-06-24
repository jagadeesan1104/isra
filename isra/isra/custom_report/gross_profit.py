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
	records = data.get("result")[:-1]
	column_list = data.get("columns")
	frappe.log_error(message=f"{records}", title="Test")
	columns = [column.get("fieldname") for column in column_list]
	labels = {col.get("fieldname"):col.get("label") for col in column_list}
	records = [row for row in records if row.get("indent") == 1]

	for row in records:
		for key in list(row.keys()):
			if key not in columns:
				del row[key]
			elif row[key] is None or isinstance(row[key], date):
				row[key] = "" if row[key] is None else row[key].strftime('%d-%m-%Y')

	# for key in columns:
	# 	total.setdefault(key, "")
	records.append(total)
	records_dict = {}
	records_dict = {key: [row[key] if isinstance(row, dict) else row[index] for row in records] for index, key in enumerate(columns)}
	df = pd.DataFrame(records_dict)
	df.rename(columns=labels, inplace=True)

	output = BytesIO()
	with pd.ExcelWriter(output, engine='openpyxl') as writer:
		df.to_excel(writer, index=False, sheet_name='Report')

	frappe.local.response.filename = "report_data.xlsx"
	frappe.local.response.filecontent = output.getvalue()
	frappe.local.response.type = "binary"
	# except Exception as err:
	# 	frappe.log_error(title="GP Custom Invoice Excel Export Issue", message=f"{err}")
	# 	return err

