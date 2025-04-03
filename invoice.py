from fpdf import FPDF
from num2words import num2words
import os
from datetime import datetime

class PDF(FPDF):
    def header(self):
        """ Set background image """
        self.image("template.jpeg", x=0, y=0, w=210, h=297)  # A4 size
        self.set_font("Arial", size=12)

def get_next_invoice_number():
    # """ Fetch and increment the last invoice number from invoice_counters collection. """
    # counter_doc = invoice_counter_collection.find_one_and_update(
    #     {"_id": "invoice_number"},
    #     {"$inc": {"last_invoice": 1}},
    #     upsert=True,
    #     return_document=True
    # )
    
    # if counter_doc and "last_invoice" in counter_doc:
    #     return counter_doc["last_invoice"]
    
    return 1000  # Default starting invoice number if collection was empty


def generate_invoice(receipt_data):
    """ Generates and saves an invoice as a PDF and returns the invoice link & file path """
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # Convert values
    receipt_data["words"] = num2words(receipt_data["amount"]/100, lang='en_IN').capitalize()
    receipt_data["tcswords"] = num2words(receipt_data["gst"], lang='en_IN').capitalize()
    receipt_data['base'] = float(receipt_data['baseAmount'])

    # Invoice details
    pdf.set_xy(101, 27)
    pdf.cell(0, 10, f"{receipt_data['invoice_no']}", ln=True)
    pdf.set_xy(141, 27)
    pdf.cell(0, 10, f"{receipt_data['date']}", ln=True)

    # Customer details
    pdf.set_xy(14, 60)
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, f"Name: {receipt_data['name']}", ln=True)

    pdf.set_xy(14, 70)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Time: {receipt_data['start_time']} - {receipt_data['end_time']}", ln=True)

    pdf.set_xy(14, 80)
    pdf.cell(0, 10, f"Phone: {receipt_data['phnNo']}", ln=True)

    pdf.set_xy(14, 90)
    pdf.cell(0, 10, f"Email: {receipt_data['email']}", ln=True)

    # Amount details
    pdf.set_xy(170, 163)
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, f"{receipt_data['amount']/100}", ln=True)

    pdf.set_xy(14, 172)
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, f"{receipt_data['words']}", ln=True)

    # Tax & GST breakdown
    pdf.set_xy(60, 190)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"{receipt_data['base']}", ln=True)
    pdf.set_xy(90, 190)
    pdf.cell(0, 10, f"9", ln=True)
    pdf.set_xy(105, 190)
    pdf.cell(0, 10, f"{receipt_data['gst']/2}", ln=True)
    pdf.set_xy(125, 190)
    pdf.cell(0, 10, f"9", ln=True)
    pdf.set_xy(140, 190)
    pdf.cell(0, 10, f"{receipt_data['gst']/2}", ln=True)
    pdf.set_xy(175, 190)
    pdf.cell(0, 10, f"{receipt_data['gst']}", ln=True)

    pdf.set_xy(60, 200)
    pdf.cell(0, 10, f"{receipt_data['base']}", ln=True)
    pdf.set_xy(105, 200)
    pdf.cell(0, 10, f"{receipt_data['gst']/2}", ln=True)
    pdf.set_xy(140, 200)
    pdf.cell(0, 10, f"{receipt_data['gst']/2}", ln=True)
    pdf.set_xy(175, 200)
    pdf.cell(0, 10, f"{receipt_data['gst']}", ln=True)

    pdf.set_xy(14, 213)
    pdf.cell(0, 10, f"{receipt_data['tcswords']}", ln=True)

    # Conditional formatting based on subCatType
    if receipt_data['subCatType'] == 'Program':
        pdf.set_xy(30, 128)
        pdf.cell(0, 10, f"Platform Fee", ln=True)
        pdf.set_xy(70, 136)
        pdf.cell(0, 10, f"Output CGST@9%", ln=True)
        pdf.set_xy(136, 128)
        pdf.cell(0, 10, f"18", ln=True)
        pdf.set_xy(148, 144)
        pdf.cell(0, 10, f"9%", ln=True)
        pdf.set_xy(148, 136)
        pdf.cell(0, 10, f"9%", ln=True)
        pdf.set_xy(70, 144)
        pdf.cell(0, 10, f"Output SGST@9%", ln=True)
        pdf.set_xy(30, 120)
        pdf.cell(0, 10, f"{receipt_data['serviceName']}", ln=True)
        pdf.set_xy(170, 120)
        pdf.cell(0, 10, f"{receipt_data['baseAmount']}", ln=True)
        pdf.set_xy(170, 136)
        pdf.cell(0, 10, f"{receipt_data['gst']/2}", ln=True)
        pdf.set_xy(170, 144)
        pdf.cell(0, 10, f"{receipt_data['gst']/2}", ln=True)
        pdf.set_xy(170, 128)
        pdf.cell(0, 10, f"{receipt_data['platformFee']}", ln=True)
    else:
        pdf.set_xy(30, 136)
        pdf.cell(0, 10, f"Platform Fee", ln=True)
        pdf.set_xy(70, 144)
        pdf.cell(0, 10, f"Output CGST@9%", ln=True)
        pdf.set_xy(136, 136)
        pdf.cell(0, 10, f"18", ln=True)
        pdf.set_xy(148, 152)
        pdf.cell(0, 10, f"9%", ln=True)
        pdf.set_xy(148, 144)
        pdf.cell(0, 10, f"9%", ln=True)
        pdf.set_xy(70, 152)
        pdf.cell(0, 10, f"Output SGST@9%", ln=True)
        pdf.set_xy(30, 120)
        pdf.cell(0, 10, f"{receipt_data['serviceName']}", ln=True)
        pdf.set_xy(30, 128)
        pdf.cell(0, 10, f"News Distribution", ln=True)
        pdf.set_xy(136, 128)
        pdf.cell(0, 10, f"18", ln=True)
        pdf.set_xy(170, 120)
        pdf.cell(0, 10, f"{receipt_data['baseAmount'] - 254.27}", ln=True)
        pdf.set_xy(170, 144)
        pdf.cell(0, 10, f"{receipt_data['gst']/2}", ln=True)
        pdf.set_xy(170, 152)
        pdf.cell(0, 10, f"{receipt_data['gst']/2}", ln=True)
        pdf.set_xy(170, 136)
        pdf.cell(0, 10, f"{receipt_data['platformFee']}", ln=True)
        pdf.set_xy(170, 128)
        pdf.cell(0, 10, f"254.27", ln=True)

    # Save PDF
    current_date = datetime.now().strftime('%Y-%m-%d')
    save_path = f"/home/rzeaiuym/files.patrakarbhavan.com/receipts/{current_date}/"
    os.makedirs(save_path, exist_ok=True)
    pdf_file_path = os.path.join(save_path, f"invoice_{receipt_data['invoice_no']}.pdf")
    pdf.output(pdf_file_path)

    invoice_link = f"https://files.patrakarbhavan.com/receipts/{current_date}/invoice_{receipt_data['invoice_no']}.pdf"
    return invoice_link, pdf_file_path