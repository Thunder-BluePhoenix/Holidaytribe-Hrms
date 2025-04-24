import frappe
from frappe.utils.file_manager import save_file
import base64
import json
import re

def save_document_attachment(doc, field_name, document_data):
    if isinstance(document_data, str):
        document_data = json.loads(document_data)
    if isinstance(document_data, list) and len(document_data) > 0:
        document_data = document_data[0]
        file_content = base64.b64decode(document_data["url"].split(",")[1])
        filename = document_data["name"]
        saved_file = save_file(
            filename,
            file_content,
            dt=doc['doctype'],
            dn=doc['name'],
            df=field_name,
            is_private=1
        )
        return saved_file.file_url
    return None

def applicant_data_insertion(variables):
    documents = variables["documents"]
    doc = variables["doc_data"]

    attachment_fields = {
        "custom_adhar_card": "custom_adhar_card_front",
        "panCard": "custom_pan_card",
        "lastYearIncreament": "custom_last_year_increment_letter_or_offer_letter",
        "custom_3_month_salary_slip_bank_statement1": "custom_adhar_card_back",
        "custom_qualification_attachments": "custom_qualification_attachments",
        "custom_salary_slip_1":"custom_salary_slip_1",
        "custom_salary_slip_2":"custom_salary_slip_2",
        "custom_salary_slip_3":"custom_salary_slip_3",
        "custom_additional_documents":"custom_additional_documents"
    }

    ja_doc = frappe.get_doc(doc['doctype'], doc['name'])

    for doc_key, field_name in attachment_fields.items():
        if documents.get(doc_key):
            file_url = save_document_attachment(doc, field_name, documents[doc_key])
            if file_url:
                setattr(ja_doc, field_name, file_url)
    # Update non-attachment fields
    ja_doc.email_id = documents.get("email_id")
    ja_doc.custom_gender = documents.get("custom_gender")
    ja_doc.custom_name_as_per_aadhar_card = documents.get("custom_name_as_per_aadhar_card")
    ja_doc.custom_name_as_per_pan_card = documents.get("custom_name_as_per_pan_card")
    ja_doc.custom_aadhar_card_no = documents.get("custom_aadhar_card_no")
    ja_doc.custom_pan_card_no = documents.get("custom_pan_card_no")
    ja_doc.custom_address_as_per_aadhar_card = documents.get("custom_address_as_per_aadhar_card")
    # Update date fields by converting them to date objects
    ja_doc.custom_expected_doj = frappe.utils.getdate(documents.get("custom_expected_doj"))
    ja_doc.custom_dob_as_per_pan = frappe.utils.getdate(documents.get("custom_dob_as_per_pan"))
    ja_doc.custom_birth_date = frappe.utils.getdate(documents.get("custom_birth_date"))
    # Save the updated Job Applicant record
    ja_doc.save(ignore_permissions=True, ignore_version=True)



