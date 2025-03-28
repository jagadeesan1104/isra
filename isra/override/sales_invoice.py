import frappe
from frappe import _


@frappe.whitelist()
def validate_item_price_less_than_buying_price(doc, method):
    try:
        for item in doc.items:
            # Get last purchase order for the item
            last_po = frappe.db.get_value("Purchase Order Item",{"item_code": item.item_code,"docstatus": 1},["rate", "parent"])

            if last_po:
                last_purchase_rate = last_po[0]
                purchase_order_id = last_po[1]
                result = last_purchase_rate * (3 / 100)
                percentage_added_amount = last_purchase_rate + result
                # Compare with current item rate (not total amount)
                if item.rate < percentage_added_amount:
                    frappe.throw(_(
                        f"Item {item.item_code} price {item.rate} is less than minimum selling price {percentage_added_amount:.2f} "
                        f"(Last Purchase Order: {purchase_order_id}, rate: {last_purchase_rate} + 3%)"
                    ))
                    
    except Exception as e:
        frappe.throw(_(f"{e}"))