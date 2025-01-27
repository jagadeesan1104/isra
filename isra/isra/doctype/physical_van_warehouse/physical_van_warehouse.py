import frappe
from frappe.model.document import Document
from frappe.utils import flt
import json  # To parse the JSON string

class PhysicalVanWarehouse(Document):
    pass

@frappe.whitelist()
def get_sales_invoice_items(date, items):
    # Parse the JSON string of items
    get_items = json.loads(items)
    
    # Extract item codes from the provided list (this can be adapted based on your fields)
    item_codes = [item['item'] for item in get_items]

    # Fetch all Sales Invoices for the selected date
    sales_invoices = frappe.get_all('Sales Invoice', filters={'posting_date': date, 'docstatus': 1}, fields=['*'])
    
    # Initialize an empty dictionary to store summed quantities for each item
    items_dict = {}

    # Loop through each sales invoice
    for si in sales_invoices:
        si_items = frappe.get_all('Sales Invoice Item', filters={'parent': si.name,}, fields=['item_code', 'item_name', 'qty', 'rate', 'amount'])
        
        for item in si_items:
        # If the item already exists in the dictionary, sum the quantities and amounts
            if item['item_code'] in items_dict:
                items_dict[item['item_code']]['qty'] += item['qty']
                items_dict[item['item_code']]['amount'] += item['amount']
            else:
                # If the item is new, add it to the dictionary
                items_dict[item['item_code']] = {
                    'item_code': item['item_code'],
                    'item_name': item['item_name'],
                    'qty': item['qty'],
                    'rate': item['rate'],
                    'amount': item['amount']
                }
    return items_dict
    # Return the items dictionary or process it as needed
    # This is where you can handle it differently based on your requirements
    # return items_dict  # You can return or process the result here, depending on your next steps