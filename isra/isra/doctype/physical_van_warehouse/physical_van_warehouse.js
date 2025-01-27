// Copyright (c) 2025, isra and contributors
// For license information, please see license.txt

frappe.ui.form.on("Physical Van Warehouse", {
	refresh: function (frm) {
        // Show the custom button only if the document is saved
        frm.add_custom_button(__('Get Items'), function () {
            // Call the Python function via Frappe API
            frappe.call({
                method: "isra.isra.doctype.physical_van_warehouse.physical_van_warehouse.get_sales_invoice_items",
                args: {
                    date: frm.doc.date,
                    items:frm.doc.items

                },
                callback: function(response) {
                    var items = response.message; 
                    // Now update the child table in the client-side
                    for (var item_code in items) {
                        var item = items[item_code];
                       //Add each item to your child table here
                        frm.add_child('items', {
                            'item': item.item_code,
                            'item_name': item.item_name,
                            'quantity': item.qty,
                            'rate': item.rate,
                            'amount': item.amount
                        });
                    }
                    frm.refresh_field('items');  // Refresh the child table field to show updated data
                }
            });
        }, __('Actions')); // Optional: Group the button under a section
    }
});
