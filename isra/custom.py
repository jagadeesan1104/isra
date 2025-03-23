import frappe
from frappe import _
from frappe.utils import flt
import erpnext
from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry

@frappe.whitelist()
def get_warehouse_and_location(customer):
    if not customer:
        return {"warehouse": None, "location": None, "sales_in_charge": None, "message": "Customer is required."}
    
    customer_location = frappe.db.get_value("Customer", customer, "custom_location")
    if not customer_location:
        return {"warehouse": None, "location": None, "sales_in_charge": None, "message": "Customer does not have a location specified."}

    warehouses = frappe.get_all("Warehouse", fields=["name","custom_sales_in_charge"])
    for warehouse in warehouses:
        warehouse_doc = frappe.get_doc("Warehouse", warehouse["name"])

        for row  in warehouse_doc.get("custom_location"):
            if row.location == customer_location:  # Match location in the child table
                # Return the matching warehouse and location
                return {
                    "warehouse": warehouse_doc.name,
                    "location": customer_location,
                    "sales_in_charge": warehouse_doc.custom_sales_in_charge
                }
    return None
    # 
    #     "warehouse": None,
    #     "location": None,
    #     "sales_in_charge": None,
    #     "message": f"No warehouse found for the customer's location: {customer_location}"
    # }


@frappe.whitelist()
def get_sales_invoice_item_rates(item_code, price_list=None,customer=None):
    # Fetch selling rate from Item Price
    selling_rate = frappe.db.get_value(
        'Item Price',
        filters={
            'item_code': item_code,
            'price_list': price_list,
            'selling': 1
        },
        fieldname='price_list_rate'
    )

    # Fetch previous invoice rate
    query = """
        SELECT item.rate
        FROM `tabSales Invoice Item` AS item
        JOIN `tabSales Invoice` AS invoice
        ON item.parent = invoice.name
        WHERE invoice.docstatus = 1
        AND item.item_code = %s
    """
    
    params = [item_code]
    if customer:
        query += " AND invoice.customer = %s"
        params.append(customer)
    query += " ORDER BY invoice.creation DESC LIMIT 1"
    previous_invoice_rate = frappe.db.sql(query, tuple(params), as_dict=True)

    return {
        'selling_rate': selling_rate,
        'previous_invoice_rate': previous_invoice_rate[0].rate if previous_invoice_rate else None
    }

@frappe.whitelist()
def get_sales_order_item_rates(item_code, price_list=None,customer=None):
    # Fetch selling rate from Item Price
    selling_rate = frappe.db.get_value(
        'Item Price',
        filters={
            'item_code': item_code,
            'price_list': price_list,
            'selling': 1
        },
        fieldname='price_list_rate'
    )

    # Fetch previous invoice rate
    query = """
        SELECT item.rate
        FROM `tabSales Order Item` AS item
        JOIN `tabSales Order` AS invoice
        ON item.parent = invoice.name
        WHERE invoice.docstatus = 1
        AND item.item_code = %s
    """

    params = [item_code]
    if customer:
        query += " AND invoice.customer = %s"
        params.append(customer)
    query += " ORDER BY invoice.creation DESC LIMIT 1"
    previous_invoice_rate = frappe.db.sql(query, tuple(params), as_dict=True)

    return {
        'selling_rate': selling_rate,
        'previous_invoice_rate': previous_invoice_rate[0].rate if previous_invoice_rate else None
    }


@frappe.whitelist()
def get_uoms_for_item(doctype, txt, searchfield, start, page_len, filters):
    item_code = filters.get("item_code")
    
    if not item_code:
        return []

    uoms = frappe.get_all(
        "UOM Conversion Detail",
        filters={"parent": item_code, "parenttype": "Item", "parentfield": "uoms"},
        fields=["uom"],
        order_by="idx asc"
    )

    return [[u["uom"]] for u in uoms] 

