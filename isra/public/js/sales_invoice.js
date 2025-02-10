// frappe.ui.form.on('Sales Invoice', {
//     onload: function (frm) {
//         if (frm.doc.customer) {
//             // Call the server-side function to get the warehouse and location
//             frappe.call({
//                 method: "isra.custom.get_warehouse_and_location", // Update with the correct path
//                 args: {
//                     customer: frm.doc.customer
//                 },
//                 callback: function (r) {
//                     if (r.message) {
//                         const { warehouse, location, sales_in_charge, message } = r.message;

//                         if (warehouse && location && sales_in_charge) {
//                             // Set the fields in the form
//                             // frm.set_value("set_warehouse", warehouse);
//                             frm.set_value("custom_location", location);
//                             frm.set_value("custom_van_sales_in_charge", sales_in_charge);
//                         } else {
//                             // Clear the fields and show a message
//                             // frm.set_value("warehouse", null);
//                             frm.set_value("location", null);
//                             frm.set_value("van_sales_in_charge", null);

//                             if (message) {
//                                 frappe.msgprint(__(message));
//                             }
//                         }
//                     }
//                 }
//             });
//         } else {
//             // Clear the fields if no customer is selected
//             frm.set_value("warehouse", null);
//             frm.set_value("location", null);
//         }
//     },
// });
// frappe.ui.form.on('Sales Invoice Item', {
//     item_code: function(frm, cdt, cdn) {
//         let item_row = frappe.get_doc(cdt, cdn);
//         if (item_row.item_code) {
//             frappe.call({
//                 method: 'isra.custom.get_item_rates', // Path to the server-side method
//                 args: {
//                     item_code: item_row.item_code,
//                     price_list: frm.doc.selling_price_list // Pass the price list from the Sales Invoice
//                 },
//                 callback: function(r) {
//                     if (r.message) {
//                         // Prepare the message for the popup
//                         let message = `
//                             <table class="table table-bordered">
//                                 <thead>
//                                     <tr>
//                                         <th>Item Code</th>
//                                         <th>Item Name</th>
//                                         <th>Selling Rate</th>
//                                         <th>Previous Invoice Rate</th>
//                                     </tr>
//                                 </thead>
//                                 <tbody>
//                                     <tr>
//                                         <td>${item_row.item_code}</td>
//                                         <td>${item_row.item_name}</td>
//                                         <td>${r.message.selling_rate || 'N/A'}</td>
//                                         <td>${r.message.previous_invoice_rate || 'N/A'}</td>
//                                     </tr>
//                                 </tbody>
//                             </table>
//                         `;

//                         // Show the rates in a popup
//                         frappe.msgprint({
//                             title: __('Item Rates'),
//                             indicator: 'blue',
//                             message: message
//                         });

//                         // Optionally, set the rate field to the selling rate
//                         frappe.model.set_value(cdt, cdn, 'rate', r.message.selling_rate);
//                     }
//                 }
//             });
//         }
//     }
// });