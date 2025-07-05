frappe.ui.form.on('Sales Order', {
    customer: function (frm) {
        if (frm.doc.customer) {
            // Call the server-side function to get the warehouse and location
            frappe.call({
                method: "isra.custom.get_warehouse_and_location", // Update with the correct path
                args: {
                    customer: frm.doc.customer
                },
                callback: function (r) {
                    if (r.message) {
                        const { warehouse, location, sales_in_charge, message } = r.message;

                        if (warehouse && location && sales_in_charge) {
                            // Set the fields in the form
                            frm.set_value("set_warehouse", warehouse);
                            frm.set_value("custom_location", location);
                            frm.set_value("custom_van_sales_in_charge", sales_in_charge);
                        } else {
                            // Clear the fields and show a message
                            frm.set_value("warehouse", null);
                            frm.set_value("location", null);
                            frm.set_value("van_sales_in_charge", null);

                            if (message) {
                                frappe.msgprint(__(message));
                            }
                        }
                    }
                }
            });
        } else {
            // Clear the fields if no customer is selected
            frm.set_value("warehouse", null);
            frm.set_value("location", null);
        }
    }
});
