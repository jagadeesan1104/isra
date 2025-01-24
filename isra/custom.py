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