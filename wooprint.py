#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

#the program is developed and maintained by Cristopher Loya <https://github.com/Neincriss>

import requests, json
import tempfile
import win32api
import win32print
import base64
from fpdf import FPDF
from pprint import pprint

username = 'user'
password = 'pass'
var = 0
last_id = 0



while True:
    request = requests.get('https://yourwordpresspage.com/wp-json/receipt-print/v1/prints', auth=(username,password))
    prints = json.loads(request.text)
    request = requests.get(prints['print'], auth=(username,password))
    receipt = json.loads(request.text)
    if receipt['id'] == last_id:
        var=0
    else:  
        last_id = receipt['id']
        fpdf = FPDF(orientation='P', unit='mm', format=(58,500) )
        fpdf.add_page()
        fpdf.set_xy(0,0)
        fpdf.image(name='Logo.png',x=2, w=45, h=22.5)
        
        fpdf.add_font(family="Calibri",fname = "Calibri 400.ttf",uni=True)
        fpdf.set_font( family="Courier", style = '',size = 8 )
        fpdf.set_fill_color(r= 250, g =250, b= 250)
        fpdf.cell(w=50, h = 4, txt = 'YOUR SHOP', border = 0, ln = 2, align = 'C', fill = True)
        fpdf.cell(w=50, h = 4, txt = 'www.yourpage.com', border = 0, ln = 2, align = 'C', fill = True)
        fpdf.cell(w=50, h = 4, txt = 'Av. Street #123', border = 0, ln = 2, align = 'C', fill = True)
        fpdf.cell(w=50, h = 4, txt = '(123)4567890', border = 0, ln = 2, align = 'C', fill = True)
        fpdf.cell(w=50, h = 4, txt = '(123)4567890', border = 0, ln = 2, align = 'C', fill = True)
        fpdf.set_font( family="Arial", style = 'B',size = 8 )
        fpdf.cell(w=50, h = 4, txt = 'ORDER:'+str(receipt['id']), border = 0, ln = 2, align = 'L', fill = True)
        fpdf.set_font( family="Arial", style = '',size = 8 )
        fpdf.cell(w=50, h = 4, txt = 'DATE: '+receipt['date_paid'], border = 0, ln = 2, align = 'L', fill = True)
        fpdf.set_line_width(0)
        fpdf.line(2,fpdf.get_y(),56,fpdf.get_y())
        fpdf.cell(w=50, h = 6, txt = 'Product', border = 0, ln = 2, align = 'L', fill = True)
        fpdf.cell(w=16, h = 4, txt = 'SKU', border = 0, ln = 0, align = 'L', fill = True)
        fpdf.cell(w=16, h = 4, txt = 'Ux$Price', border = 0, ln = 0, align = 'L', fill = True)
        fpdf.cell(w=16, h = 4, txt = 'TotalxU', border = 0, ln = 1, align = 'L', fill = True)
        

        for items in receipt["line_items"]:
            fpdf.ln(h=2)
            fpdf.set_xy(0,fpdf.get_y())
            fpdf.set_line_width(1)
            fpdf.line(4,fpdf.get_y(),52,fpdf.get_y())
            fpdf.set_font( family="Calibri", style = '',size = 9 )
            if items['variation_id'] > 0:
                text = items['name'].encode('utf-8', 'ignore').decode('utf-8')+"-"+items['meta_data'][0]['value'].encode('utf-8', 'replace').decode('utf-8')
                fpdf.cell(w=50, h = 6, txt = text, border = 0, ln = 2, align = 'L', fill = True)
            else:
                text =items['name'].encode('utf-8', 'ignore').decode('utf-8')
                fpdf.cell(w=50, h = 6, txt = text, border = 0, ln = 2, align = 'L', fill = True)
        
            fpdf.cell(w=16, h = 4, txt = items["sku"], border = 0, ln = 0, align = 'L', fill = True)
            fpdf.cell(w=16, h = 4, txt = str(items["quantity"])+'x$'+str(items["price"]), border = 0, ln = 0, align = 'L', fill = True)
            fpdf.cell(w=16, h = 4, txt = str(items["subtotal"]), border = 0, ln = 1, align = 'L', fill = True)
            var = var + items["quantity"]
        fpdf.set_font( family="Arial", style = '',size = 8 )       
        fpdf.ln(h=4)
        fpdf.set_xy(0,fpdf.get_y()) 
        fpdf.cell(w=50, h = 4, txt = "ARTICLES: "+str(var), border = 0, ln = 2, align = 'C', fill = True)
        fpdf.set_font( family="Arial", style = 'B',size = 16 )
        fpdf.cell(w=50, h = 12, txt = "TOTAL: $"+receipt['total'], border = 0, ln = 2, align = 'L', fill = True)
        
        
        fpdf.ln(h=4)
        fpdf.set_xy(0,fpdf.get_y())
        fpdf.set_font( family="Arial", style = 'B',size = 5 )
        fpdf.cell(w=50, h = 8, txt = "Politica de garantias", border = 0, ln = 2, align = 'C', fill = True)
        
        guarantee = open("guarantee.txt",'r',encoding='utf-8')
        fpdf.multi_cell(w=48,h=3,txt=guarantee.read(),align="J")
        
        
        fpdf.ln(h=4)
        fpdf.set_xy(0,fpdf.get_y())
        fpdf.set_font( family="Arial", style = 'B',size = 8 )

        fpdf.cell(w=50, h = 8, txt = "THANKS FOR YOUR VISIT!!!", border = 0, ln = 2, align = 'C', fill = True)
        fpdf.output('receipt.pdf',"F")
        filename="receipt.pdf"
        win32api.ShellExecute (
            0,
            "print",
            filename,
            '"%s"' % win32print.GetDefaultPrinter (),
            ".",
            0
        )
