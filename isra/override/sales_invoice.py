import frappe
from frappe import _


@frappe.whitelist()
def validate_item_price_less_than_buying_price(doc, method):
    company_settings = frappe.get_single("Company Settings")
    si_margin_percent = company_settings.si_margin_percent
    enable_si_margin_validate = company_settings.enable_si_margin_validate
    if enable_si_margin_validate and si_margin_percent > 0:
        for item in doc.items:
            # Get last purchase order for the item
            last_pi = frappe.db.get_value("Purchase Invoice Item",{"item_code": item.item_code,"docstatus": 1},["rate", "parent"], order_by="creation desc")

            if last_pi:
                last_purchase_rate = last_pi[0]
                purchase_invoice_id = last_pi[1]
                result = last_purchase_rate * (si_margin_percent / 100)
                percentage_added_amount = last_purchase_rate + result
                # Compare with current item rate (not total amount)
                if item.rate < percentage_added_amount:
                    frappe.throw(_(
                        f"Item <strong>{item.item_code}</strong> price <strong>{item.rate}</strong> is less than minimum selling price <strong>{percentage_added_amount:.2f}</strong> "
                        f"(Last Purchase Invoice: <strong>{purchase_invoice_id}</strong>, Rate: <strong>{last_purchase_rate} + {si_margin_percent}%</strong>)"
                    ))

def validate_item_uom(self, method):
    for item in self.items:
        if item.item_code:
            item_uoms = frappe.db.get_all("UOM Conversion Detail", filters={"parent": item.item_code, "parenttype": "Item", "parentfield": "uoms"}, fields=["uom"], pluck="uom", order_by="idx asc")
            if item.uom not in item_uoms:
                frappe.throw(_("Item <strong>{0}</strong> UOM <strong>{1}</strong> should be one of the UOM in conversion factor in Item".format(item.item_code, item.uom)))
