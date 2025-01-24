import frappe
from erpnext.stock.doctype.warehouse.warehouse import Warehouse

class CustomWarehouse(Warehouse):
    def autoname(self):
        self.autoname()



    def autoname(self):
        if self.custom_is_mobile_warehouse:  # Check if 'is_mobile_warehouse' checkbox is enabled
            # Fetch the highest existing "VAN" number
            last_van_name = frappe.db.sql("""
                SELECT name FROM `tabWarehouse`
                WHERE name LIKE 'VAN%' ORDER BY CAST(SUBSTRING(name, 4) AS UNSIGNED) DESC LIMIT 1
            """)

            if last_van_name:
                # Extract the numeric part and increment
                last_number = int(last_van_name[0][0][3:])
                new_number = last_number + 1
            else:
                # Start with VAN1 if no previous entries exist
                new_number = 1

            self.name = f"VAN{new_number}"
            return

        # If 'is_mobile_warehouse' is not enabled, fall back to the original naming logic
        if self.company:
            suffix = " - " + frappe.get_cached_value("Company", self.company, "abbr")
            if not self.warehouse_name.endswith(suffix):
                self.name = self.warehouse_name + suffix
                return

        self.name = self.warehouse_name
