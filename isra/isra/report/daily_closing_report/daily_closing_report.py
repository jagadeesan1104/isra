# Copyright (c) 2025, isra and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime,format_datetime,format_date)


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    columns = [
        _("Type") + ":Data:120",_("Doc No") + ":Data:200",_("Date") + ":Data:110",_("Narration") + ":Data:150",_("Ref no") + ":Data:80",
        _("Currency") + ":Data:100",_("Amount") + ":Data:100",_("FCY Amount") + ":Data:120",_("Balance Amount") + ":Data:150",_("Balance FCY Amount") + ":Data:180",
        _("Allocated Amount") + ":Data:150", _("Allocated FCY Amount") + ":Data:180",
        
    ]
    return columns

def get_data(filters):
    data = []
    sales_invoice = frappe.db.get_all("Sales Invoice",{"posting_date":('between',(filters.from_date,filters.to_date))},['*'])
    for sales in sales_invoice:
        row = ["",sales.name,format_date(sales.posting_date),sales.customer,"",sales.currency,sales.grand_total,sales.base_grand_total,sales.outstanding_amount,sales.base_outstanding_amount,sales.allocated_amount,sales.base_allocated_amount]
        data.append(row)
    return data