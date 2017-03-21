# pip install pdfkit
# descargar la version minGw https://wkhtmltopdf.org/downloads.html
# configuar el path en windows de wkhtmltopdf
import pdfkit
pdfkit.from_file('factura.html', 'vane2.pdf')
