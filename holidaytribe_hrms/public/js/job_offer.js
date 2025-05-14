frappe.ui.form.on('Job Offer', {
    refresh(frm) {
        console.log("Job Offer Refreshed");
        if (!frm.is_new() && frm.doc.status !== "Accepted") {
            // Add buttons under "Actions" menu properly
            frm.add_custom_button("Extend Joining Date", () => {
                let dialog = new frappe.ui.Dialog({
                    title: "Extend Joining Date",
                    fields: [
                        {
                            fieldname: "new_date",
                            label: "New Joining Date",
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
                                new_date: values.new_date
                            },
                            callback: () => {
                                frappe.msgprint("Joining date extended.");
                                frm.reload_doc();
                            }
                        });
                    }
                });
                dialog.show();
            }, "Actions");

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
});
