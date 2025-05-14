import frappe
@frappe.whitelist()
def update_joining_date(job_offer, new_date):
    doc = frappe.get_doc("Job Offer", job_offer)
    doc.custom_jo_expiry_date = new_date
    doc.save()

@frappe.whitelist()
def rescind_offer(job_offer):
    doc = frappe.get_doc("Job Offer", job_offer)
    doc.status = "Rescinded"
    doc.save()

    recipient_email = doc.get("applicant_email") or doc.get("email_id")
    sender_email = frappe.db.get_value("Email Account", {"default_outgoing": 1}, "email_id")

    message = f"""
        Dear {doc.applicant_name},<br><br>
        As you have not accepted and joined within the expected time, we regret to inform you that your offer has been rescinded.<br><br>
        Your offer letter was valid until <b>{frappe.utils.formatdate(doc.custom_jo_expiry_date)}</b>.<br><br>
        Regards,<br>
        HR Team
    """

    # Send email
    frappe.sendmail(
        recipients=[recipient_email],
        sender=sender_email,
        subject=f"Offer Rescinded - {doc.name}",
        message=message
    )

    # Create Email Communication
    frappe.get_doc({
        "doctype": "Communication",
        "subject": f"Offer Rescinded - {doc.name}",
        "communication_type": "Communication",
        "communication_medium": "Email",
        "reference_doctype": "Job Offer",
        "reference_name": doc.name,
        "recipients": recipient_email,
        "sender": sender_email,
        "content": message,
        "sent_or_received": "Sent",
        "status": "Linked"
    }).insert(ignore_permissions=True)

