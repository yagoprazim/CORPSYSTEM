import csv
from io import BytesIO
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from api.models.sale import Sale

class BaseExportSalesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        sales = self.get_filtered_sales(request)
        return self.generate_report(sales)

    def get_filtered_sales(self, request):
        vendor_id = request.GET.get('vendor')
        client_id = request.GET.get('client')
        date_str = request.GET.get('date')

        sales = Sale.objects.all()

        if vendor_id:
            sales = sales.filter(vendor_id=vendor_id)
        if client_id:
            sales = sales.filter(client_id=client_id)
        if date_str:
            date_obj = parse_date(date_str)
            if date_obj:
                sales = sales.filter(date=date_obj)
            else:
                print(f"Invalid date format: {date_str}")

        return sales

    def generate_report(self, sales):
        raise NotImplementedError("Subclasses must implement this method")

class ExportSalesToCSVView(BaseExportSalesView):
    def generate_report(self, sales):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Vendor', 'Client', 'Payment Method', 'Date', 'Total Amount', 'Finalized', 'Products'])

        for sale in sales:
            products = [f"Product: {item.product.name}, Quantity: {item.quantity}, Total Price: {item.total_price}" for item in sale.items.all()]
            products_str = "; ".join(products)

            writer.writerow([
                sale.vendor.name,
                sale.client.name,
                sale.payment_method,
                sale.date,
                sale.total_amount,
                sale.is_finalized,
                products_str
            ])

        return response
    
class ExportSalesToPDFView(BaseExportSalesView):
    def generate_report(self, sales):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        content = []
        content.append(Paragraph("Sales Report", styles['Title']))
        content.append(Spacer(1, 12))

        for sale in sales:
            content.append(Paragraph("Sale:", styles['Heading2']))
            content.append(Spacer(1, 6))

            sale_info = [
                [f"Vendor: {sale.vendor.name}"],
                [f"Client: {sale.client.name}"],
                [f"Payment Method: {sale.payment_method}"],
                [f"Date: {sale.date}"],
                [f"Total Amount: {sale.total_amount}"],
                [f"Finalized: {sale.is_finalized}"]
            ]

            content.append(Table(sale_info, colWidths=[6*inch], style=[
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]))

            products = []
            for item in sale.items.all():
                product_info = f"Product: {item.product.name}, Quantity: {item.quantity}, Total Price: {item.total_price}"
                products.append([product_info])
            
            if products:
                content.append(Paragraph("Products:", styles['Heading5']))
                product_table = Table(products, colWidths=[6*inch])
                product_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ]))
                content.append(product_table)
                content.append(Spacer(1, 12))

        doc.build(content)
        buffer.seek(0)
        response.write(buffer.getvalue())
        buffer.close()

        return response