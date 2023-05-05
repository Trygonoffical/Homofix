from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse,HttpResponseRedirect
from django.urls import reverse
from .models import Support,Customer,Product,Booking,CustomUser,Task,Technician,Category,STATE_CHOICES,Rebooking,BookingProduct,SubCategory,ContactUs,JobEnquiry,Addon
# from datetime import datetime,timedelta
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum
from django.http import Http404
import random
import datetime
import requests
import urllib.parse
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER,TA_LEFT,TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph,Image



def index(request,id):
    booking_id = Booking.objects.get(id=id)
    context={
        'booking_id':booking_id
    }
    return render(request, 'Support_templates/index.html',context)
   
    
	
	


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


data = {
	"company": "Dennnis Ivanov Company",
	"address": "123 Street name",
	"city": "Vancouver",
	"state": "WA",
	"zipcode": "98663",


	"phone": "555-555-2345",
	"email": "youremail@dennisivy.com",
	"website": "dennisivy.com",
	}
# class ViewPDF(View):
#     def get(self, request, *args, **kwargs):
#         booking_id = kwargs['booking_id']
#         booking = Booking.objects.get(id=booking_id)
#         context = {
#             'booking': booking,
#             "header":"header"
#         }
#         pdf = render_to_pdf('Support_templates/Invoice/invoice.html', context)
#         return HttpResponse(pdf, content_type='application/pdf')


# def ViewPDF(request,booking_id):
#     import os
        
#     if os.path.exists('last_invoice_number.txt'):
#         with open('last_invoice_number.txt', 'r') as f:
#             last_invoice_number = int(f.read().strip())
#     else:
#         last_invoice_number = 0

# # Increment the last invoice number
#     new_invoice_number = f'INV-{last_invoice_number+1:03d}'

# # Save the new invoice number to the file
#     with open('last_invoice_number.txt', 'w') as f:
#         f.write(str(last_invoice_number+1))

# # Print the new invoice number
#     print("newwwwww",new_invoice_number)
#     # print("ggggg")
#     book_id = Booking.objects.get(id=booking_id)

#     my_path = f"F:\\Homofix\\v73\\invoice_{book_id.order_id}.pdf"
#     print("my path",my_path)
#     # filename = f"invoice_{instance.order_id}.pdf"
#     doc = SimpleDocTemplate(my_path, pagesize=letter,topMargin=0)

    
#     # Add the title to the document
#     para_style2 = ParagraphStyle(
#     'title',
#     fontSize=18,
#     leading=20,
#     alignment=TA_CENTER,  # align text to the left
#     textColor=colors.black,
#     spaceBefore=0,  # no space before the paragraph
#     spaceAfter=12,
# )

    
#     title = Paragraph('LIST OF ITEM', para_style2)
#     addon_title = Paragraph('LIST OF Addon', para_style2)
#     inv = Paragraph('Invoice',para_style2)
#     title.spaceBefore = 0  # set spaceBefore to zero
#     addon_title.spaceBefore = 0  # set spaceBefore to zero
#      # Create the table for bill to information
#     bookingid=Booking.objects.get(id=booking_id)
   
#     bill_to_data = [    ['Bill To:', bookingid.customer.admin.first_name],
#         ['Address:', bookingid.customer.address],     
#         ['Mobile:', f'+91{bookingid.customer.mobile}' ],
#         ['Email:', bookingid.customer.admin.email],
#     ]
#     bill_to_table = Table(bill_to_data, colWidths=[150, None], hAlign='LEFT')
    


# # Apply the bill to table style
#     # bill_to_style = TableStyle([    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    ('FONTSIZE', (0, 0), (-1, -1), 11),    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),])

#     bill_to_style = TableStyle([
#     ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
#     ('FONTSIZE', (0, 0), (-1, -1), 11),
#     # ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    
#     ('LINEAFTER', (1, 0), (1, -1), 0.5, colors.black),
# ])

#     bill_to_table.setStyle(bill_to_style)

#     # Get the last invoice number from a file
    
# # Create the table for invoice details
#     invoice_data = [    ['Invoice No:', 'INV-001'],
#         ['Invoice Date:', '18-Apr-2023'],
#         # ['Due Date:', '30-Apr-2023'],
#     ]

#     invoice_table = Table(invoice_data, colWidths=[150, None], hAlign='LEFT')



#     # Apply the invoice table style
#     # invoice_style = TableStyle([    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    ('FONTSIZE', (0, 0), (-1, -1), 11),    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),])
#     invoice_style = TableStyle([
#     ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
#     ('FONTSIZE', (0, 0), (-1, -1), 11),
#     ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
#     ('LEFTPADDING', (0, 0), (-1, -1), 6),
# ])

#     invoice_table.setStyle(invoice_style)
    
#     nested_table_style = TableStyle([
#     ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
#     ('FONTSIZE', (0, 0), (-1, -1), 11),
#     ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
#     ('BOX', (0, 0), (-1, -1), 1, colors.black),
# ])

#     # Create the nested table with two columns and one row
#     nested_table_data = [[bill_to_table, invoice_table]]
#     nested_table = Table(nested_table_data, colWidths=[250, 250])
#     nested_table.setStyle(nested_table_style)


#     # Define the table data
    
#     data = [['Product Name', 'Qty','RATE','TAX','AMOUNT'],]
#     addon = [['Addon Name', 'Qty','RATE','TAX','AMOUNT'],]
#     bookingProd=BookingProduct.objects.filter(booking=booking_id)
#     adon = Addon.objects.filter(booking_prod_id__booking=booking_id)
#     # stu = Booking.objects.all()
#     for bookingprod in bookingProd:

#         price = 0
#         if bookingprod.product.selling_price != None:
#             price = bookingprod.product.selling_price
#         else:
#             price = bookingprod.product.price
        
#         data.append([bookingprod.product.name, bookingprod.quantity,price,'18%',f'{bookingprod.quantity*price*1.18:.2f}'])
#         # data.append([bookingprod.product.name, bookingprod.quantity,price,'18%',bookingprod.quantity*price*1.18])
#         for i in adon:
#             if i.spare_parts_id.product == bookingprod.product:
#                 # addon.append([i.spare_parts_id.spare_part,i.quantity,i.spare_parts_id.price,'18%',i.quantity*i.spare_parts_id.price*1.18])
#                 addon.append([i.spare_parts_id.spare_part, i.quantity, i.spare_parts_id.price, '18%', f'{i.quantity * i.spare_parts_id.price * 1.18:.2f}'])


#         # if i.spare_parts_id.product ==  bookingprod.product:
#         #     addon.append([i.spare_parts_id.spare_part])
            
        
# #     data.append(['Ac Repairing', '2','100','18%','200'])
        

#     # Create the table
#     # col_widths = [100, 100]
#     col_widths = [270, 30, 75, 50, 70]
#     table = Table(data,colWidths=col_widths)
#     addon_col_widths = [270, 30, 75, 50, 70]
#     addontable = Table(addon,colWidths=addon_col_widths)

#     # Apply the table style
#     style = TableStyle([
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
#         # ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black),
#         ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, 0), 14),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#         ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
#         # ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
#         ('FONTSIZE', (0, 1), (-1, -1), 12),
#         ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
#         ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
#     ])
#     table.setStyle(style)
    
#     addonstyle = TableStyle([
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
#         # ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black),
#         ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, 0), 14),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#         ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
#         # ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
#         ('FONTSIZE', (0, 1), (-1, -1), 12),
#         ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
#         ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
#     ])
#     addontable.setStyle(addonstyle)
    

#     # Define the paragraph style
#     para_style = ParagraphStyle(
#         'title',
#         fontSize=18,
#         leading=24,
#         alignment=TA_CENTER,
#         textColor=colors.black,
#         spaceBefore=12,
#         spaceAfter=12,
#     )
    
    
#     logo_path = "F:\pdf genera django\LOGO2.jpeg"
    
#     logo = Image(logo_path, width=1.5*inch, height=1.5*inch)
#     logo.hAlign = 'LEFT'



    
    
#     # Create the table for invoice totals
#     booking = Booking.objects.get(id=booking_id)
#     tax_rate = 0.18
#     total_price = total_price = booking.total_amount
#     print("ttoaalll",total_price)
#     gst = int(total_price * 18)/100
#     total = total_price+gst
#     # print("gsstttt",gst)

#     invoice_totals_data = [    ['Subtotal:', f'{total_price:.2f}'],
#         ['CGST @9%:', f'{gst/2:.2f}'],
#         ['SGST @9%:', f'{gst/2:.2f}'],
#         ['Total:', f'{total:.2f}'],
#     ]

#     invoice_totals_table = Table(invoice_totals_data, colWidths=[90, None], hAlign='RIGHT')

# # Apply the invoice totals table style
#     # invoice_totals_style = TableStyle([    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    ('FONTSIZE', (0, 0), (-1, -1), 11),    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),])
#     invoice_totals_style = TableStyle([    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    ('FONTSIZE', (0, 0), (-1, -1), 11),    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),    ('LINEABOVE', (0, 3), (-1, 3), 1, colors.black),('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),])
#     invoice_totals_table.setStyle(invoice_totals_style)


#     # Create the table for company information
#     company_data = [        [''],  # Add an empty row before the company information
#         [f'{"Homofix Technologies PVT Ltd":^65}'],
#         # [''],
#         [f'{"Corporate Office: 2nd Floor, WP-501-D, Unit 209, Shiv Market, Wazirpur Village ,":^50}'],
#         [f'{"Ashok Vihar, New Delhi, Central Delhi, Delhi, 110052":^90}'],
#         [f'{"Regd Office: 5139, Awas Vikas 3, Kalyanpur,Kanpur,Uttar Pradesh, India,208017":^50}'],
#         [f'{"GSTIN:07AAGCH4863F1Z1":^110}'],

#         # ['Ashok Vihar Delhi,New Delhi 110052'],
#         # [ '+1 (555) 987-6543'],
#         # ['info@abccorp.com'],
#     ]
    

#     # company_table = Table(company_data, colWidths=[90, None])
#     company_table = Table(company_data, colWidths=[doc.width, 0])

#     # Apply the company table style
 
#     # Apply the company table style
#     company_style = TableStyle([
#     ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
#     ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),  # Add line below style to the first row
#     ('FONTSIZE', (0, 1), (-1, -1), 20),
#     ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
#     ('TOPPADDING', (0, 0), (0, 0), 6),  # Add top padding to the first cell of the first row
#     ('LEFTPADDING', (0, 0), (0, 0), 50),  # Add left padding to the first cell of the first row
#     ('ALIGN', (0, 0), (0, 0), 'CENTER'),  # Align the first cell of the first row to the center
#     # ('TEXTCOLOR', (0, 0), (-1, -1), colors.blue),
#     # ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid style to all cells
#     ('FONTSIZE', (0, 2), (-1, 2), 12),
#     ('FONTSIZE', (0, 3), (-1, 3), 12),
#     ('TOPPADDING', (0, 3), (-1, 3), -8),
#     ('FONTSIZE', (0, 4), (-1, 4), 12),
#     ('FONTSIZE', (0, 5), (-1, 5), 12),
#     ('TOPPADDING', (0, 5), (-1, 5), -6),
#     # ('LINEBELOW', (-1, -1), (-1, -1), 1, colors.black)  # Add line below style to the last row
# ])
#     company_table.setStyle(company_style)

   
#     # doc = SimpleDocTemplate(f'invoice{}.pdf', topMargin=0)

#     doc.build([inv,logo, nested_table, Spacer(1, 0.*inch),title, table,Spacer(1, 0.1*inch),addon_title,addontable, Spacer(1, 0.5*inch), invoice_totals_table, Spacer(1, 0.5*inch), company_table])
#     import os
#     if os.path.exists(my_path):
#         with open(my_path, 'rb') as pdf:
#             response = HttpResponse(pdf.read(), content_type='application/pdf')
#             response['Content-Disposition'] = 'inline; filename="invoice.pdf"'
#             return response
#     # else:
#     #     return HttpResponse("The requested file does not exist.")

#     return HttpResponse("Invoice generated successfully")    


def ViewPDF(request,booking_id):
    
    import os
        
    if os.path.exists('last_invoice_number.txt'):
        with open('last_invoice_number.txt', 'r') as f:
            last_invoice_number = int(f.read().strip())
    else:
        last_invoice_number = 0

# Increment the last invoice number
    new_invoice_number = f'INV-{last_invoice_number+1:03d}'

# Save the new invoice number to the file
    with open('last_invoice_number.txt', 'w') as f:
        f.write(str(last_invoice_number+1))

# Print the new invoice number
    print("newwwwww",new_invoice_number)
    # print("ggggg")
    book_id = Booking.objects.get(id=booking_id)

    filename  = f"invoice_{book_id.order_id}.pdf"
    my_path = os.path.join(settings.MEDIA_ROOT, filename)
    # my_path = f"F:\\Homofix\\v75\\invoice_{book_id.order_id}.pdf"
    print("my path",my_path)
    # filename = f"invoice_{instance.order_id}.pdf"
    doc = SimpleDocTemplate(my_path, pagesize=letter,topMargin=0)

    
    # Add the title to the document
    para_style2 = ParagraphStyle(
    'title',
    fontSize=18,
    leading=20,
    alignment=TA_CENTER,  # align text to the left
    textColor=colors.black,
    spaceBefore=0,  # no space before the paragraph
    spaceAfter=12,
)

    
    title = Paragraph('LIST OF ITEM', para_style2)
    addon_title = Paragraph('LIST OF Addon', para_style2)
    inv = Paragraph('Invoice',para_style2)
    title.spaceBefore = 0  # set spaceBefore to zero
    addon_title.spaceBefore = 0  # set spaceBefore to zero
     # Create the table for bill to information
    bookingid=Booking.objects.get(id=booking_id)
   
    bill_to_data = [    ['Bill To:', bookingid.customer.admin.first_name],
        ['Address:', bookingid.customer.address],     
        ['Mobile:', f'+91{bookingid.customer.mobile}' ],
        ['Email:', bookingid.customer.admin.email],
    ]
    bill_to_table = Table(bill_to_data, colWidths=[150, None], hAlign='LEFT')
    


# Apply the bill to table style
    # bill_to_style = TableStyle([    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    ('FONTSIZE', (0, 0), (-1, -1), 11),    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),])

    bill_to_style = TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    # ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    
    ('LINEAFTER', (1, 0), (1, -1), 0.5, colors.black),
])

    bill_to_table.setStyle(bill_to_style)

    # Get the last invoice number from a file
    
# Create the table for invoice details
    invoice_data = [    ['Invoice No:', 'INV-001'],
        ['Invoice Date:', '18-Apr-2023'],
        # ['Due Date:', '30-Apr-2023'],
    ]

    invoice_table = Table(invoice_data, colWidths=[150, None], hAlign='LEFT')



    # Apply the invoice table style
    # invoice_style = TableStyle([    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    ('FONTSIZE', (0, 0), (-1, -1), 11),    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),])
    invoice_style = TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
])

    invoice_table.setStyle(invoice_style)
    
    nested_table_style = TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('BOX', (0, 0), (-1, -1), 1, colors.black),
])

    # Create the nested table with two columns and one row
    nested_table_data = [[bill_to_table, invoice_table]]
    nested_table = Table(nested_table_data, colWidths=[250, 250])
    nested_table.setStyle(nested_table_style)


    # Define the table data
    
    data = [['Product Name', 'Qty','RATE','TAX','AMOUNT'],]
    addon = [['Addon Name', 'Qty','RATE','TAX','AMOUNT'],]
    bookingProd=BookingProduct.objects.filter(booking=booking_id)
    adon = Addon.objects.filter(booking_prod_id__booking=booking_id)
    # stu = Booking.objects.all()
    for bookingprod in bookingProd:

        price = 0
        if bookingprod.product.selling_price != None:
            price = bookingprod.product.selling_price
        else:
            price = bookingprod.product.price
        
        data.append([bookingprod.product.name, bookingprod.quantity,price,'18%',f'{bookingprod.quantity*price*1.18:.2f}'])
        # data.append([bookingprod.product.name, bookingprod.quantity,price,'18%',bookingprod.quantity*price*1.18])
        for i in adon:
            if i.spare_parts_id.product == bookingprod.product:
                # addon.append([i.spare_parts_id.spare_part,i.quantity,i.spare_parts_id.price,'18%',i.quantity*i.spare_parts_id.price*1.18])
                addon.append([i.spare_parts_id.spare_part, i.quantity, i.spare_parts_id.price, '18%', f'{i.quantity * i.spare_parts_id.price * 1.18:.2f}'])


        # if i.spare_parts_id.product ==  bookingprod.product:
        #     addon.append([i.spare_parts_id.spare_part])
            
        
#     data.append(['Ac Repairing', '2','100','18%','200'])
        

    # Create the table
    # col_widths = [100, 100]
    col_widths = [270, 30, 75, 50, 70]
    table = Table(data,colWidths=col_widths)
    addon_col_widths = [270, 30, 75, 50, 70]
    addontable = Table(addon,colWidths=addon_col_widths)

    # Apply the table style
    style = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        # ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        # ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
    ])
    table.setStyle(style)
    
    addonstyle = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        # ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        # ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
    ])
    addontable.setStyle(addonstyle)
    

    # Define the paragraph style
    para_style = ParagraphStyle(
        'title',
        fontSize=18,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceBefore=12,
        spaceAfter=12,
    )
    
    
    logo_path = os.path.join(settings.MEDIA_ROOT, 'LOGO2.jpeg')

    
    
    logo = Image(logo_path, width=1.5*inch, height=1.5*inch)
    logo.hAlign = 'LEFT'



    
    
    # Create the table for invoice totals
    booking = Booking.objects.get(id=booking_id)
    tax_rate = 0.18
    total_price = total_price = booking.total_amount
    print("ttoaalll",total_price)
    gst = int(total_price * 18)/100
    total = total_price+gst
    # print("gsstttt",gst)

    invoice_totals_data = [    ['Subtotal:', f'{total_price:.2f}'],
        ['CGST @9%:', f'{gst/2:.2f}'],
        ['SGST @9%:', f'{gst/2:.2f}'],
        ['Total:', f'{total:.2f}'],
    ]

    invoice_totals_table = Table(invoice_totals_data, colWidths=[90, None], hAlign='RIGHT')

# Apply the invoice totals table style
    # invoice_totals_style = TableStyle([    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    ('FONTSIZE', (0, 0), (-1, -1), 11),    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),])
    invoice_totals_style = TableStyle([    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    ('FONTSIZE', (0, 0), (-1, -1), 11),    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),    ('LINEABOVE', (0, 3), (-1, 3), 1, colors.black),('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),])
    invoice_totals_table.setStyle(invoice_totals_style)


    # Create the table for company information
    company_data = [        [''],  # Add an empty row before the company information
        [f'{"Homofix Technologies PVT Ltd":^65}'],
        # [''],
        [f'{"Corporate Office: 2nd Floor, WP-501-D, Unit 209, Shiv Market, Wazirpur Village ,":^50}'],
        [f'{"Ashok Vihar, New Delhi, Central Delhi, Delhi, 110052":^90}'],
        [f'{"Regd Office: 5139, Awas Vikas 3, Kalyanpur,Kanpur,Uttar Pradesh, India,208017":^50}'],
        [f'{"GSTIN:07AAGCH4863F1Z1":^110}'],

        # ['Ashok Vihar Delhi,New Delhi 110052'],
        # [ '+1 (555) 987-6543'],
        # ['info@abccorp.com'],
    ]
    

    # company_table = Table(company_data, colWidths=[90, None])
    company_table = Table(company_data, colWidths=[doc.width, 0])

    # Apply the company table style
 
    # Apply the company table style
    company_style = TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),  # Add line below style to the first row
    ('FONTSIZE', (0, 1), (-1, -1), 20),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
    ('TOPPADDING', (0, 0), (0, 0), 6),  # Add top padding to the first cell of the first row
    ('LEFTPADDING', (0, 0), (0, 0), 50),  # Add left padding to the first cell of the first row
    ('ALIGN', (0, 0), (0, 0), 'CENTER'),  # Align the first cell of the first row to the center
    # ('TEXTCOLOR', (0, 0), (-1, -1), colors.blue),
    # ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid style to all cells
    ('FONTSIZE', (0, 2), (-1, 2), 12),
    ('FONTSIZE', (0, 3), (-1, 3), 12),
    ('TOPPADDING', (0, 3), (-1, 3), -8),
    ('FONTSIZE', (0, 4), (-1, 4), 12),
    ('FONTSIZE', (0, 5), (-1, 5), 12),
    ('TOPPADDING', (0, 5), (-1, 5), -6),
    # ('LINEBELOW', (-1, -1), (-1, -1), 1, colors.black)  # Add line below style to the last row
])
    company_table.setStyle(company_style)

   
    # doc = SimpleDocTemplate(f'invoice{}.pdf', topMargin=0)

    doc.build([inv,logo, nested_table, Spacer(1, 0.*inch),title, table,Spacer(1, 0.1*inch),addon_title,addontable, Spacer(1, 0.5*inch), invoice_totals_table, Spacer(1, 0.5*inch), company_table])
    import os
    if os.path.exists(my_path):
        with open(my_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="invoice.pdf"'
            return response
    # else:
    #     return HttpResponse("The requested file does not exist.")

    return HttpResponse("Invoice generated successfully")        
#Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		
		pdf = render_to_pdf('Support_templates/Invoice/invoice.html', data)

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Invoice_%s.pdf" %("12341231")
		content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response

       
@login_required(login_url='/')
def dashboard(request):
    user = request.user
    support = Support.objects.get(admin=user)  
    context = {
        
        'support':support
    }

    return render(request,'Support_templates/Dashboard/dashboard.html',context)

def support_profile(request):
    return render(request,'Support_templates/Profile/profile.html')



def support_profile_update(request):
    if request.method == "POST":
        support_id = request.POST.get('support_id')
       
        profile_pic = request.FILES.get('profile_pic') 
        username = request.POST.get('username')
        email = request.POST.get('email')
        mob_no = request.POST.get('mob_no')
        address = request.POST.get('address')
        status = request.POST.get('status')

        support = Support.objects.get(id=support_id)

       
        support.admin.username =username 
        support.admin.email =email
        if profile_pic != None:
            support.profile_pic =profile_pic
         
        support.address =address 
        support.mobile =mob_no 

        if status == 'Deactivate':
            support.status = "Deactivate"
            
        elif status == 'Hold':
            support.status = 'Hold'
        else:
            support.status = 'Active'

        support.save()
        messages.success(request,'Support Updated Succesffully')
        return HttpResponseRedirect(reverse("support_profile"))


# def support_orders(request):
    
#     technicians = Technician.objects.all()
#     order_count = Booking.objects.filter(status="New").count()
#     user = request.user
#     support = Support.objects.get(admin=user)
    


#     # i want calcualate here 
#     tasks = Task.objects.all()   
#     bookings = Booking.objects.filter(status="New")
    
#     total_price = 0
   
    


#     if request.method == "POST":
       
#         random_number = random.randint(0, 999)
#         unique_number = str(random_number).zfill(3)
       
        
#         # username = request.POST.get('username')
#         first_name = request.POST.get('full_name')
        
#         mob = request.POST.get('mob')

#         cus = Customer.objects.filter(admin__first_name=first_name)
        
 
#         if Customer.objects.filter(admin__first_name=first_name, mobile=mob).exists():
           
#             user= CustomUser.objects.get(first_name=first_name)
#             request.session['cust_id'] = user.customer.id
#             return JsonResponse({'status':'Save'})
        
#         else:
#             # print
#         #     if CustomUser.objects.filter(username=first_name):
#         #         return JsonResponse({'status':'Error'})
#             user = CustomUser.objects.create(username=first_name+unique_number,first_name=first_name, user_type='4')    
#             user.set_password(mob)
#             user.customer.mobile = mob
#             user.save()
#             request.session['customer_id'] = user.customer.id
#             return JsonResponse({'status':'Save'})

#     context = {
#     'bookings':bookings,
#     'technicians':technicians,
#     'tasks':tasks,
#     'order_count':order_count,
#     'total_price':total_price,
#     'support':support
    
    
#    }    
#     return render(request, 'Support_templates/Orders/order.html',context)


def support_orders(request):
    
    technicians = Technician.objects.all()
    order_count = Booking.objects.filter(status="New").count()
    user = request.user
    support = Support.objects.get(admin=user)
    


    # i want calcualate here 
    tasks = Task.objects.all()   
    bookings = Booking.objects.filter(status="New")
    
    total_price = 0
   
    


    if request.method == "POST":
        print("testing")
        otp_number = random.randint(0,9999)
        otp_unique = str(otp_number).zfill(3)
       
        first_name = request.POST.get('full_name')      
        mob = request.POST.get('mob')
        request.session['full_name'] = first_name
        request.session['mob'] = mob
        request.session['otp'] = otp_unique

        if Customer.objects.filter(mobile=mob).exists():

            
            print("helloooo suceess")
            # print("heloooooooo")
            


            # auth_key = "IQkJfqxEfD5l3qCu"
            # sender_id = "TRYGON"
            # route = 2
            # number = mob
       
            # message = f"Dear {first_name} {otp_unique} is the OTP for your login at Trygon. In case you have not requested this, please contact us at info@trygon.in"
            
            
            # template_id = "1707162192151162124"
            # url = f"http://weberleads.in/http-tokenkeyapi.php?authentic-key={auth_key}&senderid={sender_id}&route={route}&number={number}&message={urllib.parse.quote(message)}&templateid={template_id}"
            # response = requests.get(url) 
                
            customer = Customer.objects.get(mobile=mob)
            customer.first_name = first_name
            customer.save()
            return JsonResponse({'status':'Save'})

        # elif Customer.objects.filter(mobile=mob).exists():
        #     print("hellooooo")
        #     return JsonResponse({'status':'Error'})

            
        else:
            
        

            # request.session['full_name'] = first_name
            # request.session['mob'] = mob
            # request.session['otp'] = otp_unique


            # auth_key = "IQkJfqxEfD5l3qCu"
            # sender_id = "TRYGON"
            # route = 2
            # number = mob
        
            # message = f"Dear {first_name} {otp_unique} is the OTP for your login at Trygon. In case you have not requested this, please contact us at info@trygon.in"
        
        
            # template_id = "1707162192151162124"
            # url = f"http://weberleads.in/http-tokenkeyapi.php?authentic-key={auth_key}&senderid={sender_id}&route={route}&number={number}&message={urllib.parse.quote(message)}&templateid={template_id}"
            # response = requests.get(url) 
                    

            return JsonResponse({'status':'Save'})
        
        
        

    context = {
    'bookings':bookings,
    'technicians':technicians,
    'tasks':tasks,
    'order_count':order_count,
    'total_price':total_price,
    'support':support
    
    
   }    
    return render(request, 'Support_templates/Orders/order.html',context)




def support_otp(request):
    if request.method == "POST":
        mob = request.POST.get('mob')
        username = request.POST.get('username')
    

    
   
        if Customer.objects.filter(admin__username=username, mobile=mob).exists():
            user= CustomUser.objects.get(username=username)
            
            request.session['customer_id'] = user.customer.id
            return redirect('support_otp')
        else:
            if CustomUser.objects.filter(username=username):
                messages.error(request, 'Username already exists')
                return redirect('support_orders')
            user = CustomUser.objects.create(username=username, password=mob, user_type='4')    
            user.customer.mobile = mob
            user.save()
            request.session['customer_id'] = user.customer.id
            
            return redirect('support_otp')
    return render(request,'Support_templates/OTP/otp.html')


def support_verify_otp(request):
    if request.method == "POST":
        otp_num = request.session.get('otp', 'Default value if key does not exist')
        
        

        otp = request.POST.get('otp')
        # if otp == otp_num:  
        if otp == "1234":  
            # OTP is correct, redirect to success page
            # return HttpResponse('otp sucess')
            
            random_number = random.randint(0, 999)
            unique_number = str(random_number).zfill(3)
       
            first_name = request.session.get('full_name', 'Default value if key does not exist')
            mob = request.session.get('mob', 'Default value if key does not exist')
            
            
            if Customer.objects.filter(mobile=mob).exists():
                customer = Customer.objects.get(mobile=mob)
                request.session['customer_id'] = customer.id
                # request.session['customer_id'] = Customer.id
                return JsonResponse({'status': 'Save', 'message': 'otp is match'})
                
            else:

                # user = CustomUser.objects.create(username=user.id,first_name=first_name, user_type='4')    
                user = CustomUser.objects.create(first_name=first_name,username=first_name+unique_number, user_type='4')    
                user.set_password(mob)
                user.customer.mobile = mob
                user.save()
                request.session['customer_id'] = user.customer.id

            return JsonResponse({'status': 'Save', 'message': 'otp is match'})
            # return redirect('support_orders')
        else:
            # OTP is incorrect, show error message and reload the page
            # messages.error(request, 'Invalid OTP. Please try again.')
            
            return JsonResponse({'status': 'error', 'message': 'otp is not eeee valid'})
            # return render(request, 'Support_templates/OTP/otp.html')
    # return render(request, 'Support_templates/Orders/otp_modal.html')


# def support_booking(request):
#     prod = Product.objects.all()
#     supported_by = request.user.support
   
#     if request.method == 'POST':
        
#         customer_id = request.session.get('customer_id')       
        
#         product_id = request.POST.get('product_id')
#         booking_date_str = request.POST.get('booking_date')
#         customer = Customer.objects.get(id=customer_id)
        
#         product = Product.objects.get(id=product_id)
     
#         # create the booking object
#         booking = Booking(customer=customer, product=product,booking_date=datetime.strptime(booking_date_str, "%Y-%m-%dT%H:%M"),supported_by=supported_by)
#         booking.save()
#         messages.success(request, 'Booking created successfully.')
#         return redirect('support_orders')
    
   
#     context = {
#         'prod':prod
#         }
#     return render(request, 'Support_templates/Booking/create_booking.html', context)



def support_booking(request):
    order_count = Booking.objects.filter(status="New").count()
    user = request.user
    support = Support.objects.get(admin=user)
    prod = Product.objects.all()
    category = Category.objects.all()
    state_choices = STATE_CHOICES
    supported_by = request.user.support
    

    if request.method == 'POST':
       
        customer_id = request.session.get('customer_id','Default value if key does not exist')
        print("customer id ",customer_id)
        
        product_ids = request.POST.getlist('product_id')
        quantities = request.POST.getlist('quantity')
        
        booking_date_str = request.POST.get('booking_date')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        address = request.POST.get('address')
        city = request.POST.get('city')
        area = request.POST.get('area')
        description = request.POST.get('description')
        total_amount = int(request.POST.get('total_amount'))
        print("sss",total_amount)
        
        customer = Customer.objects.get(id=customer_id)
        if city:
            city = city.lower()
        customer.city = city
        customer.state = state
        customer.area = area
        customer.zipcode = zip_code
        customer.address=address,
        customer.save()
        booking_date = timezone.make_aware(datetime.datetime.fromisoformat(booking_date_str))
        
        
        booking = Booking.objects.create(
            customer=customer,
            booking_date=booking_date,   
            description=description,          
            supported_by=supported_by
        )



        for i, product_id in enumerate(product_ids):
            product = Product.objects.get(id=product_id)
            print("producttttt",product)
            # print("producttttt",product)
            
            quantity = int(quantities[i])
            price = int(request.POST.getlist('price')[i])
            
            BookingProduct.objects.create(
                booking=booking,
                product=product,
                quantity=quantity,
                total_price=total_amount
                # price=price
            )
            # total_price = sum(price_list)
            # booking.total_price = total_price
            booking.save()

        messages.success(request, 'Booking created successfully.')
        return redirect('support_orders')

    context = {
        'prod': prod,
        'state_choices':state_choices,
        'category':category,
        'support':support,
        'order_count':order_count
    }
    return render(request, 'Support_templates/Booking/create_booking.html', context)

def reschedule_booking(request):
    if request.method == "POST":

        booking_id=request.POST.get('booking_id')
        booking_date_str = request.POST.get('booking_date')
        booking_date = timezone.make_aware(datetime.datetime.fromisoformat(booking_date_str))
        print("booking date",booking_date)
        booking = Booking.objects.get(id=booking_id)
        booking.booking_date = booking_date
        booking.save()
        messages.success(request,"Your order reschedule success")

        return redirect('support_orders')



def cancel_booking(request,booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.status = 'cancelled'
    booking.save()
    messages.success(request, 'Booking has been cancelled.')
    return redirect('support_orders')    


# def support_Task_assign(request):
    
#     if request.method == "POST":
#         booking_id = request.POST.get('booking_id')
#         technician_id = request.POST.get('technician_id')

#         booking = Booking.objects.get(id=booking_id)
#         technician = Technician.objects.get(id=technician_id)
#         task = Task.objects.create(booking=booking,technician=technician)
#         task.save()
#         booking.status="Assign"
#         technician.status_choice = "Assign"
#         technician.save()
#         # booking.save()
#         messages.success(request,'Assign Task Successfully')
#         return redirect('support_list_of_task')
   


def support_Task_assign(request):
    user = request.user
    support = Support.objects.get(admin=user)
    
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        technician_id = request.POST.get('technician_id')

        booking = get_object_or_404(Booking, id=booking_id)
        technician = get_object_or_404(Technician, id=technician_id)
        supported_by = request.user.support
        task = Task.objects.create(
            booking=booking,
            technician=technician,
            supported_by=supported_by
        )
        task.save()

        booking.status = "Assign"
        booking.save()
        

        technician.status_choice = "Assign"
        technician.save()

        messages.success(request, 'Assign Task Successfully')
        return redirect('support_list_of_task')




def support_List_of_expert(request,id):
    user = request.user
    support = Support.objects.get(admin=user)  
    
    booking = Booking.objects.get(id=id)
    
   
    expert = Technician.objects.filter(city=booking.customer.city)
    tasks = Task.objects.filter(booking=booking)
    
   
    
    # expert = Technician.objects.filter(city=booking.city, serving_area__icontains=booking.area)
    context = {
        'expert':expert,
        'booking':booking,
        'tasks': tasks,
        'support':support
        
        
        
    }
    
    return render(request,'Support_templates/Orders/list_of_expert.html',context)    

def support_task_counting(request,expert_id):
    technician = Technician.objects.get(id=expert_id)
    print(technician)
    task = Task.objects.filter(id=technician)
    print("tasskkk",task)
    print("gggggggggggg",technician)
    return render(request,'test.html')
    # return redirect('support_List_of_expert',expert_id)

def support_list_of_task(request):
    user = request.user
    support = Support.objects.get(admin=user)
    order_count = Booking.objects.filter(status="New").count()
    task = Task.objects.all()
    context = {
        'task':task,
        'support':support,
        'order_count':order_count,
    }
    return render(request,'Support_templates/Orders/list_of_task.html',context)    

def order_cancel(request):
    user = request.user
    support = Support.objects.get(admin=user)
    order_count = Booking.objects.filter(status="New").count()
    booking = Booking.objects.filter(status="cancelled")
    context = {
        'booking':booking,
        'support':support,
        'order_count':order_count,
    }
    return render(request,'Support_templates/Orders/cancel_order.html',context)    

def support_booking_complete(request):
    user = request.user
    support = Support.objects.get(admin=user)  
    order_count = Booking.objects.filter(status="New").count()
    task = Task.objects.filter(booking__status = "Completed")
    context = {
        'task':task,
        'support':support,
        'order_count':order_count,
    }
    return render(request,'Support_templates/Rebooking/booking_complete.html',context)    
    

# def support_rebooking(request,task_id):
#     task = get_object_or_404(Task, id=task_id)
#     booking_id = task.booking.id
#     booking_prod = BookingProduct.objects.filter(booking_id=booking_id)
#     context = {
#         'booking_prod':booking_prod
#     }
#     # print(booking_prod)
#     return render(request,'Support_templates/Rebooking/rebooking.html',context) 

# def support_rebooking(request, task_id):
#     task = get_object_or_404(Task, id=task_id)
#     booking_id = task.booking.id
#     booking_prod = BookingProduct.objects.filter(booking_id=booking_id)
    
#     context = {
#         'booking_prod': booking_prod,
        
#     }
#     return render(request, 'Support_templates/Rebooking/rebooking.html', context)


def support_rebooking(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    booking_id = task.booking.id
    user = request.user
    support = Support.objects.get(admin=user)
    
    booking_products = BookingProduct.objects.filter(booking_id=booking_id).select_related('booking', 'product')
    
    for booking_product in booking_products:
        rebookings = Rebooking.objects.filter(booking_product_id=booking_product.id).order_by('-id')
        booking_product.rebookings.set(rebookings)

    context = {
        'booking_prod': booking_products,
        'support':support
        
    }
    return render(request, 'Support_templates/Rebooking/rebooking.html', context)

def support_rebooking_list(request):
    user = request.user
    support = Support.objects.get(admin=user)  
    order_count = Booking.objects.filter(status="New").count()
    rebooking = Rebooking.objects.all()
    context = {
        'rebooking' :rebooking,
        'support':support,
        'order_count':order_count,
        
    }
    return render(request,'Support_templates/Rebooking/rebooking_list.html',context)    



def support_rebooking_update(request):
    if request.method == 'POST':
        booking_product_id = request.POST.get('booking_prod_id')
        
        booking_date = request.POST.get('booking_date')
        
        try:
            # booking_product = BookingProduct.objects.get(booking_id=booking_product_id)
            booking_product = BookingProduct.objects.filter(booking=booking_product_id).first()
            booking = booking_product.booking
            task = Task.objects.get(booking=booking)
        except (BookingProduct.DoesNotExist, Task.DoesNotExist):
            raise Http404('BookingProduct or Task matching query does not exist.')
        
        # create a new rebooking object with the same booking and assign it to the same technician
        rebooking = Rebooking.objects.create(
            booking_product=booking_product,
            technician=task.technician,
            booking_date=booking_date
        )
        
        # update the status of the original booking to "completed"
        task.booking.status = "completed"
        task.booking.save()
        
        rebooking.save()
        print("successsss",rebooking)
        messages.success(request, 'Rebooking successfully created.')
        return redirect('support_booking_complete')

    context = {}
    return render(request, 'Support_templates/Rebooking/booking_complete.html', context)



def support_get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(Category_id=category_id)
    data = list(subcategories.values('id', 'name'))
    return JsonResponse(data, safe=False)

def support_get_products(request):
    subcategory_id = request.GET.get('subcategory_id')
    if subcategory_id:
        subcategory_id = int(subcategory_id)
        products = Product.objects.filter(subcategory_id=subcategory_id)
        data = []
        for product in products:
            if product.selling_price is not None:
                price = product.selling_price
            else:
                price = product.price
            data.append({'id': product.id, 'price': price, 'name': product.name})
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse([], safe=False)

# def support_rebooking_update(request):
#     if request.method == 'POST':
#         id = request.POST.get('booking_prod_id')
#         try:
#             task = Task.objects.get(booking__id=id)
#         except Task.DoesNotExist:
#             raise Http404('Task matching query does not exist.')
        
#         # create a new rebooking object with the same booking and assign it to the same technician
#         rebooking = Rebooking.objects.create(
#             booking=task.booking,
#             technician=task.technician,
#             booking_date=request.POST.get('booking_date')
#         )
#         rebooking.save()
        
#         # update the status of the original booking to "completed"
#         task.booking.status = "completed"
#         task.booking.save()
        
#         messages.success(request, 'Rebooking successfully created.')
#         return redirect('support_booking_complete')

#     context = {}
#     return render(request, 'Support_templates/Rebooking/booking_complete.html', context)


def support_rebooking_product(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    booking_id = task.booking.id
    booking_prod = BookingProduct.objects.filter(booking_id=booking_id)
    print(booking_prod)
    return render(request, 'Support_templates/Rebooking/rebooking_product.html', {'booking_prod': booking_prod})


    # return render(request,'Support_templates/Rebooking/rebooking_product.html',{'booking_prod':booking_prod})    
def support_expert_add(request):
    
    category = Category.objects.all()
    user = request.user
    support = Support.objects.get(admin=user) 
    order_count = Booking.objects.filter(status="New").count()
    if request.method == "POST":
        current_user = request.user
        
        random_number = random.randint(0, 999)
        unique_number = str(random_number).zfill(3)
        sub_category_id = request.POST.getlist('sub_category_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        subcat = SubCategory.objects.filter(id__in=sub_category_id)
        # category_id = request.POST.get('category_id')
        # username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

       

        # ctg = Category.objects.get(id=category_id)
      
        # if CustomUser.objects.filter(username = username).exists():
        #     # return JsonResponse({'status': 'error', 'message': 'Username is already Taken'})
        #     messages.error(request,'Username is already Taken')
        #     return redirect('support_list_of_expert')
        supported_by = request.user.support 
        user = CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=first_name+unique_number,password=password,email=email,user_type='2')
        user.technician.subcategories.set(subcat)
        user.technician.status = "New"
        user.technician.supported_by = supported_by
        user.save()
        messages.success(request,'Expert Register Successfully')
        return redirect('support_list_of_expert')

    context = {
        'category':category,
        'support':support,
        'order_count':order_count,
    }
    return render(request,'Support_templates/Expert/add_expert.html',context)
def support_list_of_expert(request):
    user = request.user
    support = Support.objects.get(admin=user)  

    category = Category.objects.all()
    technician = Technician.objects.all()
    task = Task.objects.all()
    order_count = Booking.objects.filter(status="New").count()
    
    context = {
        'category':category,
        'technician':technician,
        'abcc':task,
        'support':support,
        'order_count':order_count,
    }

    return render(request,'Support_templates/Expert/expert.html',context)    


def support_add_expert(request):
    category = Category.objects.all()
    technician = Technician.objects.all()
    if request.method == "POST":
        
        category_id = request.POST.get('category_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

       

        ctg = Category.objects.get(id=category_id)
      
        if CustomUser.objects.filter(username = username).exists():
            # return JsonResponse({'status': 'error', 'message': 'Username is already Taken'})
            messages.error(request,'Username is already Taken')
            return redirect('support_list_of_expert')
            


        user = CustomUser.objects.create_user(username=username,password=password,email=email,user_type='2')
        user.technician.category = ctg
        user.technician.status = "New"
        user.save()
        messages.success(request,'Expert Register Successfully')
        return redirect('support_list_of_expert')
        # if(user.is_active):
        #     return JsonResponse({'status':'Save'})
            
        # else:
        #     return JsonResponse({'status':0})

    # return render(request,'homofix_app/AdminDashboard/Technician/technician.html',{'category':category,'technician':technician})



def expert_edit_profile(request,id):
    user = request.user
    support = Support.objects.get(admin=user) 
    technician = Technician.objects.get(id=id)
    order_count = Booking.objects.filter(status="New").count()
    subcategories = SubCategory.objects.filter(Category_id__id__in=technician.subcategories.values_list('Category_id__id', flat=True))
    state_choices = STATE_CHOICES
    # print("ahsssssss",cit)
    category = Category.objects.all()
    # city_choices = [
    #     ('city1', 'City 1'),
    #     ('city2', 'City 2'),
    #     ('city3', 'City 3'),
    # ]
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        father_name = request.POST.get('father_name')    
        # category_id = request.POST.get('category_id')
        subcategory_id = request.POST.getlist('sub_category_id')
        mob_no = request.POST.get('mob_no')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')
        permanent_address = request.POST.get('permanent_address')
        id_proof = request.POST.get('id_proof')
        id_nob = request.FILES.get('id_nob')
        rating = request.POST.get('rating')
        serving_area = request.POST.get('serving_area')
        highest_qualification = request.POST.get('highest_qualification')
        state = request.POST.get('state')
        city = request.POST.get('city')
        status = request.POST.get('status')   
        date_of_joining = request.POST.get('date_of_joining')   
        application_form = request.FILES.get('application_form')   
        

        technician.admin.first_name = firstname
        technician.admin.last_name = lastname
        technician.admin.username = username
        technician.admin.email = email
        if profile_pic != None:
            technician.profile_pic=profile_pic

        technician.Father_name=father_name
        technician.mobile=mob_no
        technician.present_address=present_address
        technician.permanent_address=permanent_address
        technician.Id_Proof=id_proof

        if id_nob != None:
            technician.id_proof_document=id_nob

        # if status == 'Deactivate':
        #     technician.status = "Deactivate"
            
        # elif status == 'Hold':
        #     technician.status = 'Hold'
        # else:
        #     technician.status = 'Active'

        technician.rating=rating
        technician.serving_area=serving_area
        technician.highest_qualification=highest_qualification
        technician.state=state
        technician.city=city
        technician.joining_date=date_of_joining
        if application_form != None:
            technician.application_form=application_form
        

        # cat = Category.objects.get(id=category_id)
        technician.subcategories.set(subcategory_id)

        # technician.category=cat

        technician.admin.save()
        technician.save()
        messages.success(request,'updated sucessfully')
        return redirect('expert_edit_profile',id=technician.id)
        # return render(request,'homofix_app/AdminDashboard/Technician/technician_profile.html',{'technician':technician,'category':category})
        # return redirect('technician_edit_profile',{'technician_id': technician_id})
    return render(request,'Support_templates/Expert/expert_profile.html',{'technician':technician,'category':category,'state_choices':state_choices,'support':support,'order_count':order_count,'subcategories':subcategories})




# ---------------------------- Invoice ------------------------------- 
def invoice(request,booking_id):
    booking = Booking.objects.get(id=booking_id)
    context = {
        'booking':booking
    }
    return render(request,'Support_templates/Invoice/invoice.html',context)


# -------------------------------- Contact Us -------------------------- 




def support_contact_us(request):
    user = request.user
    support = Support.objects.get(admin=user)   
    contact_us = ContactUs.objects.all()
    context = {
        'contact_us':contact_us,
        'support':support
    }

    return render(request,'Support_templates/ContactUs/contact_us.html',context)    

def support_job_enquiry(request):
    user = request.user
    support = Support.objects.get(admin=user)   
    job_enquiry = JobEnquiry.objects.all()
    context = {
        'job_enquiry':job_enquiry,
        'support':support,
    }

    return render(request,'Support_templates/JobEnquiry/job_enquiry.html',context)

# ------------------------ Testing for session --------------------------- 

def myView(request):
    # Store data in the session
    request.session['my_data'] = 'Hello, World!'
    return HttpResponse('Data stored in the session.')


def another_view(request):
    # Retrieve data from the session
    my_data = request.session.get('my_data', 'Default value if key does not exist')
    return HttpResponse(my_data)


def showproduct(request):
    product = Product.objects.all()
    context = {
        'product':product
    }
    return render(request,'Support_templates/show_product.html',context)


def pdf_report_create(request):
    product = Product.objects.all()
    template_path = "Support_templates/pdfreport.html"
    context = {'product':product}
    response= HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment;filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html,dest=response)

    if pisa_status.err:
        return HttpResponse("We had some error <pre>" + html + '</pre>')
    return response
