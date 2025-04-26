# Copyright (c) 2025, BluePhoenix and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class HeadcountPlan(Document):

	import frappe

	def autoname(self, method=None):
		dept_code = (self.department or "").replace(" ", "")[:3].upper()
		desg_code = (self.designation or "").replace(" ", "")[:4].upper()
		
		from_year = self.from_date.split("-")[0][-2:] if self.from_date else "00"  # last two digits
		to_year = self.to_date.split("-")[0][-2:] if self.to_date else "00"        # last two digits

		last_entry = frappe.db.get_value(
			"Headcount Plan",
			filters={
				"from_date": self.from_date,
				"to_date": self.to_date,
				"department": self.department,
				"designation": self.designation
			},
			fieldname="name",
			order_by="creation desc"
		)

		if last_entry and "-" in last_entry:
			last_number = int(last_entry.split("-")[-1]) + 1
		else:
			last_number = 1

		self.name = f"HCP-{dept_code}-{desg_code}-{from_year}-{to_year}-{str(last_number).zfill(4)}"


