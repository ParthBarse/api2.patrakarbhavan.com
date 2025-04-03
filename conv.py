from fpdf import FPDF
from num2words import num2words

class PDF(FPDF):
    def header(self):
        # Set background image (Ensure the file exists in the same directory)
        self.image("template.jpeg", x=0, y=0, w=210, h=297)  # A4 size (210x297 mm)
        pdf.set_font("Arial",size=12)

# Initialize PDF
pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", size=10)


# Receipt Data
receipt_data = {
    
  "date": "2025-04-06",
  "start_time": "10:00",
  "end_time": "14:00",
  "duration": "240",
  "status": "booked",
  "name": "Yash",
  "email": "yash.potdar@aissmsioit.org",
  "contact": "+918793015610",
  "serviceId": "press-conference",
  "serviceName": "PUWJ | B. V. Rao Press Conference Hall",
  "phnNo": "08793015610",
  "amount": 563300,
  "method": "upi",
  "payment_id": "pay_QDlLON9pb93hYR",
  "order_id": "order_QDlKlqweJhsiAG",
  "insName": "BnB",
  "subCatType": "Program",
  "bookedBy": "Online",
  "gstNo": "1234567890",
  "govId": "1234567890",
  "subject": "Testing UI",
  "gst": 839,
  "platformFee": 133,
  "baseAmount": "4661",
  "invoice_no":1234,
}

receipt_data["words"] = num2words(receipt_data["amount"]/100, lang='en_IN').capitalize()
receipt_data["tcswords"] = num2words(receipt_data["gst"], lang='en_IN').capitalize()
receipt_data['base']= int(receipt_data['baseAmount']) + receipt_data['platformFee']

pdf.set_xy(101, 27)
pdf.cell(0, 10, f"{receipt_data['invoice_no']}", ln=True)
pdf.set_xy(141, 27)
pdf.cell(0, 10, f"{receipt_data['date']}", ln=True)

pdf.set_xy(14, 60)
pdf.set_font("Arial", style="B", size=10) 
pdf.cell(0, 10, f"name: {receipt_data['name']}", ln=True)

pdf.set_xy(14, 70)
pdf.set_font("Arial", size=10) 
pdf.cell(0, 10, f"Time: {receipt_data['start_time']}-{receipt_data['end_time'] }", ln=True)


pdf.set_xy(14, 80)
pdf.cell(0, 10, f"phnNo: {receipt_data['phnNo']}", ln=True)


pdf.set_xy(14, 90)
pdf.cell(0, 10, f"Email: {receipt_data['email']}", ln=True)



pdf.set_xy(170, 163)
pdf.set_font("Arial", style="B", size=10) 
pdf.cell(0, 10, f"{receipt_data['amount']/100}", ln=True)

pdf.set_xy(14, 172)
pdf.set_font("Arial", style="B", size=10) 
pdf.cell(0, 10, f"{receipt_data['words']}", ln=True)


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

if(receipt_data['subCatType']=='Program'):
    
    pdf.set_xy(30, 128)
    pdf.cell(0, 10, f"Platform platformFee", ln=True)
    pdf.set_xy(70, 136)
    pdf.cell(0, 10, f"Output CGST%@9", ln=True)
    pdf.set_xy(136, 128)
    pdf.cell(0, 10, f"18", ln=True)
    pdf.set_xy(148, 144)
    pdf.cell(0, 10, f"9      %", ln=True)
    pdf.set_xy(148, 136)
    pdf.cell(0, 10, f"9      %", ln=True)
    pdf.set_xy(70, 144)
    pdf.cell(0, 10, f"Output SGST%@9", ln=True)
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
    pdf.cell(0, 10, f"Platform platformFee", ln=True)
    pdf.set_xy(70, 144)
    pdf.cell(0, 10, f"Output CGST@9%", ln=True)
    pdf.set_xy(136, 136)
    pdf.cell(0, 10, f"18", ln=True)
    pdf.set_xy(148, 152)
    pdf.cell(0, 10, f"9       %", ln=True)
    pdf.set_xy(148, 144)
    pdf.cell(0, 10, f"9       %", ln=True)
    pdf.set_xy(70, 152)
    pdf.cell(0, 10, f"Output SGST@9%", ln=True)
    pdf.set_xy(30, 120)
    pdf.cell(0, 10, f"{receipt_data['serviceName']}", ln=True)
    pdf.set_xy(30, 128)
    pdf.cell(0, 10, f"News Distribution", ln=True)
    pdf.set_xy(136, 128)
    pdf.cell(0, 10, f"18", ln=True)
    pdf.set_xy(170, 120)
    pdf.cell(0, 10, f"{receipt_data['baseAmount']}", ln=True)
    pdf.set_xy(170, 144)
    pdf.cell(0, 10, f"{receipt_data['gst']/2}", ln=True)
    pdf.set_xy(170, 152)
    pdf.cell(0, 10, f"{receipt_data['gst']/2}", ln=True)
    pdf.set_xy(170, 136)
    pdf.cell(0, 10, f"{receipt_data['platformFee']}", ln=True)
    pdf.set_xy(170, 128)
    pdf.cell(0, 10, f"254.27", ln=True)

    

    


# Save PDF
pdf.output("invoice23.pdf")

print("PDF with background image generated successfully!")
