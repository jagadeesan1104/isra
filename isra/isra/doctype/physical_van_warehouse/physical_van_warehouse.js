// Copyright (c) 2025, isra and contributors
// For license information, please see license.txt

frappe.ui.form.on("Physical Van Warehouse", {
    refresh: function (frm) {
        if (frm.is_new()) {
            return;
        }
        // // Show the custom button only if the document is saved
        // frm.add_custom_button(__('Sales Invoice Item'), function () {
        //     // Call the Python function via Frappe API
        //     if (frm.doc.material_transfer_items_added) {
        //         frappe.msgprint(__('Material Transfer items are already added. Please create a new document.'));
        //         return;
        //     }
        //     frappe.call({
        //         method: "isra.isra.doctype.physical_van_warehouse.physical_van_warehouse.get_sales_invoice_items",
        //         args: {
        //             date: frm.doc.date,
        //             warehouse: frm.doc.warehouse, // Pass the warehouse field value
        //             items: frm.doc.items // Pass existing items (if needed)
        //         },
        //         callback: function (response) {
        //             var items = response.message;
        //             // Update the child table in the client-side
        //             if (items) {
        //                 frm.clear_table('items'); // Clear the child table first
        //                 for (var item_code in items) {
        //                     var item = items[item_code];
        //                     // Add each item to your child table
        //                     frm.add_child('items', {
        //                         'item': item.item_code,
        //                         'item_name': item.item_name,
        //                         'quantity': item.qty,
        //                         'rate': item.rate,
        //                         'amount': item.amount
        //                     });
        //                 }
        //                 frm.refresh_field('items'); // Refresh the child table field to show updated data
        //                 frm.set_value("sales_invoice_items_added", 1);
        //             }
        //         }
        //     });
        // }, __('Actions')); // Optional: Group the button under a section
        frm.add_custom_button(__('Material Transfer Item'), function () {
            if (frm.doc.sales_invoice_items_added) {
                frappe.msgprint(__('Items from "Sales Invoice Item" already added. Please create a new document for "Material Transfer Item".'));
            } else {
                frappe.call({
                    method: "isra.isra.doctype.physical_van_warehouse.physical_van_warehouse.get_material_transfer_items",
                    args: {
                        date: frm.doc.date,
                        warehouse: frm.doc.warehouse,
                        items: frm.doc.items
                    },
                    callback: function (response) {
                        var items = response.message;
                        if (items) {
                            frm.clear_table('items'); 
                            for (var item_code in items) {
                                var item = items[item_code];
                                frm.add_child('items', {
                                    'item': item.item_code,
                                    'item_name': item.item_name,
                                    'quantity': item.qty,
                                    'rate': item.rate,
                                    'amount': item.amount
                                });
                            }
                            frm.refresh_field('items');
                            frm.set_value("material_transfer_items_added", 1);
                        }
                    }
                });
            }
        }, __('Actions'));
    }
    
});
