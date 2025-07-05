// Copyright (c) 2023, ISRA and contributors
// For license information, please see license.txt

// This file extends the Payment Entry functionality from ERPNext

frappe.ui.form.on('Payment Entry', {
	// Override the party_type function from ERPNext
	party_type: function(frm) {
		if (frm.doc.party_type === "Warehouse") {
			frm.set_query("party", function() {
				return {
					doctype: "Warehouse",
					filters: {
						company: frm.doc.company,
						custom_is_mobile_warehouse: 1  // Only show warehouses marked as mobile warehouse
					}
				};
			});
		}
	},
	// Handle when warehouse party is selected
	party: function(frm) {
		if (frm.doc.party_type === "Warehouse") {
			frm.set_df_property('party_name', 'hidden', 1);
		}
	},

	get_outstanding_documents: function(frm, filters, get_outstanding_invoices, get_orders_to_be_billed) {
        if (frm.doc.party_type === "Warehouse" && get_outstanding_invoices) {
            frm.clear_table("references");
            
            // Prepare filters for warehouse invoices
            let invoice_filters = {
                docstatus: 1,
                outstanding_amount: ['>', 0],
                custom_warehouse: frm.doc.party
            };
            
            // Add date filters if provided
            if (filters.from_posting_date && filters.to_posting_date) {
                invoice_filters.posting_date = ['between', [filters.from_posting_date, filters.to_posting_date]];
            }
            
            // Add outstanding amount filters if provided
            if (filters.outstanding_amt_greater_than) {
                invoice_filters.outstanding_amount = ['>', flt(filters.outstanding_amt_greater_than)];
            }
            if (filters.outstanding_amt_less_than) {
                invoice_filters.outstanding_amount = ['<', flt(filters.outstanding_amt_less_than)];
            }
            
            // Get sales invoices for the selected warehouse
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Sales Invoice',
                    filters: invoice_filters,
                    fields: ['name', 'posting_date', 'due_date', 'outstanding_amount', 'grand_total']
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        // Add each invoice to the references table
                        r.message.forEach(function(invoice) {
                            let row = frm.add_child('references');
                            row.reference_doctype = 'Sales Invoice';
                            row.reference_name = invoice.name;
                            row.due_date = invoice.due_date;
                            row.total_amount = invoice.grand_total;
                            row.outstanding_amount = invoice.outstanding_amount;
                        });
                        
                        // Refresh the form
                        frm.refresh_fields();
                        frm.events.set_total_allocated_amount(frm);
                    } else {
                        frappe.msgprint(__('No outstanding invoices found for the selected warehouse'));
                    }
                }
            });
            return;
        }
        
        // For non-warehouse party types, use the standard ERPNext implementation
        frm.clear_table("references");

        if (!frm.doc.party) {
            return;
        }

        frm.events.check_mandatory_to_fetch(frm);
        var company_currency = frappe.get_doc(":Company", frm.doc.company).default_currency;

        var args = {
            posting_date: frm.doc.posting_date,
            company: frm.doc.company,
            party_type: frm.doc.party_type,
            payment_type: frm.doc.payment_type,
            party: frm.doc.party,
            party_account: frm.doc.payment_type == "Receive" ? frm.doc.paid_from : frm.doc.paid_to,
            cost_center: frm.doc.cost_center,
        };

        for (let key in filters) {
            args[key] = filters[key];
        }

        if (get_outstanding_invoices) {
            args["get_outstanding_invoices"] = true;
        } else if (get_orders_to_be_billed) {
            args["get_orders_to_be_billed"] = true;
        }

        if (frm.doc.get_all_invoices) {
            args.get_all_invoices = true;
        }

        frappe.call({
            method: "erpnext.accounts.doctype.payment_entry.payment_entry.get_outstanding_reference_documents",
            args: {
                args: args,
            },
            callback: function(r, rt) {
                if (r.message) {
                    var total_positive_outstanding = 0;
                    var total_negative_outstanding = 0;

                    $.each(r.message, function(i, d) {
                        var c = frm.add_child("references");
                        c.reference_doctype = d.voucher_type;
                        c.reference_name = d.voucher_no;
                        c.due_date = d.due_date;
                        c.total_amount = d.invoice_amount;
                        c.outstanding_amount = d.outstanding_amount;
                        c.bill_no = d.bill_no;

                        if (!in_list(["Sales Order", "Purchase Order", "Expense Claim", "Fees"], d.voucher_type)) {
                            if (flt(d.outstanding_amount) > 0)
                                total_positive_outstanding += flt(d.outstanding_amount);
                            else
                                total_negative_outstanding += Math.abs(flt(d.outstanding_amount));
                        }

                        var party_account_currency = frm.doc.payment_type=="Receive" ? frm.doc.paid_from_account_currency : frm.doc.paid_to_account_currency;
                        if(party_account_currency != company_currency) {
                            c.exchange_rate = d.exchange_rate;
                        } else {
                            c.exchange_rate = 1;
                        }
                        if (in_list(['Sales Invoice', 'Purchase Invoice', 'Expense Claim', 'Fees'], d.voucher_type)) {
                            c.due_date = d.due_date;
                        }
                    });

                    if(
                        (frm.doc.payment_type=="Receive" && frm.doc.party_type=="Customer") ||
                        (frm.doc.payment_type=="Pay" && frm.doc.party_type=="Supplier")  ||
                        (frm.doc.payment_type=="Pay" && frm.doc.party_type=="Employee") ||
                        (frm.doc.payment_type=="Receive" && frm.doc.party_type=="Student")
                    ) {
                        if(total_positive_outstanding > total_negative_outstanding)
                            if (!frm.doc.paid_amount)
                                frm.set_value("paid_amount",
                                    total_positive_outstanding - total_negative_outstanding);
                    } else if (
                        total_negative_outstanding &&
                        total_positive_outstanding < total_negative_outstanding
                    ) {
                        if (!frm.doc.received_amount)
                            frm.set_value("received_amount",
                                total_negative_outstanding - total_positive_outstanding);
                    }
                }

                frm.events.allocate_party_amount_against_ref_docs(frm,
                    (frm.doc.payment_type=="Receive" ? frm.doc.paid_amount : frm.doc.received_amount));
            }
        });
    }
});
frappe.ui.form.on('Denomination', {
	pieces: function(frm, cdt, cdn) {
		var deno_row = locals[cdt][cdn];
        if (deno_row.pieces) {
            deno_row.amount = deno_row.pieces * deno_row.deno;
            // Refresh the field to update the UI immediately
            refresh_field('amount', deno_row.name, 'custom_denomination');
        }
		var total_amount = 0
		$.each(frm.doc.custom_denomination, function(i, d) { total_amount += d.amount; });
		frm.set_value("custom_total_amount", total_amount);
	},
	deno: function(frm, cdt, cdn) {
		var deno_row = locals[cdt][cdn];
        if (deno_row.deno) {
            deno_row.amount = deno_row.pieces * deno_row.deno;
            // Refresh the field to update the UI immediately
            refresh_field('amount', deno_row.name, 'custom_denomination');
        }
		var total_amount = 0
		$.each(frm.doc.custom_denomination, function(i, d) { total_amount += d.amount; });
		frm.set_value("custom_total_amount", total_amount);
	},
	before_custom_denomination_remove: function(frm, cdt, cdn) {
		var deleted_row = frappe.get_doc(cdt, cdn);
		var total_amount = frm.doc.custom_total_amount - deleted_row.amount
		frm.set_value("custom_total_amount", total_amount);
	},
});
