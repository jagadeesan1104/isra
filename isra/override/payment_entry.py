import frappe
from frappe import _
from frappe.utils import flt

def update_invoice_status_after_submit(doc, method):
    """
    Update the status of sales invoices referenced in a warehouse-based payment entry
    This function should be called after a payment entry is submitted
    """
    if doc.party_type != "Warehouse":
        return
        
    # Process only for warehouse-based payment entries
    for ref in doc.references:
        if ref.reference_doctype == "Sales Invoice" and ref.allocated_amount > 0:
            # Get the sales invoice
            invoice = frappe.get_doc("Sales Invoice", ref.reference_name)
            
            # Calculate the new outstanding amount
            outstanding_amount = flt(invoice.outstanding_amount) - flt(ref.allocated_amount)
            
            # Update the outstanding amount in the database
            frappe.db.set_value("Sales Invoice", ref.reference_name, "outstanding_amount", outstanding_amount)
            
            # Update the status based on the outstanding amount
            status = None
            if outstanding_amount <= 0:
                status = "Paid"
            elif outstanding_amount < invoice.grand_total:
                status = "Partly Paid"
                
            if status:
                frappe.db.set_value("Sales Invoice", ref.reference_name, "status", status)
                
    # Commit the transaction to ensure changes are saved
    frappe.db.commit()

def update_invoice_status_on_cancel(doc, method):
    """
    Revert the status of sales invoices when a warehouse-based payment entry is cancelled
    """
    if doc.party_type != "Warehouse":
        return
        
    # Process only for warehouse-based payment entries
    for ref in doc.references:
        if ref.reference_doctype == "Sales Invoice" and ref.allocated_amount > 0:
            # Get the sales invoice
            invoice = frappe.get_doc("Sales Invoice", ref.reference_name)
            
            # Add back the allocated amount to outstanding
            outstanding_amount = flt(invoice.outstanding_amount) + flt(ref.allocated_amount)
            
            # Update the outstanding amount in the database
            frappe.db.set_value("Sales Invoice", ref.reference_name, "outstanding_amount", outstanding_amount)
            
            # Update the status based on the outstanding amount
            status = None
            if outstanding_amount <= 0:
                status = "Paid"
            elif outstanding_amount < invoice.grand_total:
                status = "Partly Paid"
            else:
                status = "Unpaid"
                
            if status:
                frappe.db.set_value("Sales Invoice", ref.reference_name, "status", status)
                
    # Commit the transaction to ensure changes are saved
    frappe.db.commit()