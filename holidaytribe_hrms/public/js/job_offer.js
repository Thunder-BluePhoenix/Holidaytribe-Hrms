frappe.ui.form.on('Job Offer', {
    refresh(frm) {
        if (!frm.is_new() && frm.doc.status !== "Accepted") {
            // Add buttons under "Actions" menu properly
            frm.add_custom_button("Extend Offer Expiry Date", () => {
                let dialog = new frappe.ui.Dialog({
                    title: "Extend Offer Expiry Date",
                    fields: [
                        {
                            fieldname: "new_expiry_date",
                            label: "New Expiry Date",
                            fieldtype: "Date",
                            reqd: 1
                        }
                    ],
                    primary_action_label: "Update",
                    primary_action(values) {
                        dialog.hide();
                        frappe.call({
                            method: "holidaytribe_hrms.overrides.job_offer.update_joining_date",
                            args: {
                                job_offer: frm.doc.name,
                                new_expiry_date: values.new_expiry_date
                            },
                            callback: () => {
                                frappe.msgprint("Offer expiry date extended.");
                                frm.reload_doc();
                            }
                        });
                    }
                });
                dialog.show();
            }, "Actions");
            if (!frm.is_new() && !["Accepted", "Rescinded"].includes(frm.doc.status)) {
            frm.add_custom_button("Rescind Offer", () => {
                frappe.call({
                    method: "holidaytribe_hrms.overrides.job_offer.rescind_offer",
                    args: {
                        job_offer: frm.doc.name
                    },
                    callback: () => {
                        frappe.msgprint("Offer rescinded and candidate notified.");
                        frm.reload_doc();
                    }
                });
            }, "Actions");
        }
    }
}
});
