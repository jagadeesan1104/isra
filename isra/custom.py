import frappe

@frappe.whitelist()
def get_warehouse_and_location(customer):
    if not customer:
        return {"warehouse": None, "location": None, "sales_in_charge": None}
    
    customer_location = frappe.db.get_value("Customer", customer, "custom_location")
    if not customer_location:
        return {"warehouse": None, "location": None, "sales_in_charge": None, "message": "Customer does not have a location specified."}
    
    warehouses = frappe.get_all("Warehouse", fields=["name"])
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
    return {
        "warehouse": None,
        "location": None,
        "sales_in_charge": None,
        "message": f"No warehouse found for the customer's location: {customer_location}"
    }


@frappe.whitelist()
def get_sales_invoice_item_rates(item_code, price_list=None):
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
    previous_invoice_rate = frappe.db.sql("""
        SELECT item.rate
        FROM `tabSales Invoice Item` AS item
        JOIN `tabSales Invoice` AS invoice
        ON item.parent = invoice.name
        WHERE invoice.docstatus = 1
        AND item.item_code = %s
        ORDER BY invoice.creation DESC
        LIMIT 1
    """, (item_code), as_dict=True)

    return {
        'selling_rate': selling_rate,
        'previous_invoice_rate': previous_invoice_rate[0].rate if previous_invoice_rate else None
    }

@frappe.whitelist()
def get_sales_order_item_rates(item_code, price_list=None):
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
    previous_invoice_rate = frappe.db.sql("""
        SELECT item.rate
        FROM `tabSales Order Item` AS item
        JOIN `tabSales Order` AS invoice
        ON item.parent = invoice.name
        WHERE invoice.docstatus = 1
        AND item.item_code = %s
        ORDER BY invoice.creation DESC
        LIMIT 1
    """, (item_code), as_dict=True)

    return {
        'selling_rate': selling_rate,
        'previous_invoice_rate': previous_invoice_rate[0].rate if previous_invoice_rate else None
    }