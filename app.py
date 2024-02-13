import base64
from flask import Flask, render_template,jsonify,request,redirect
import xmltodict
from myclass import Felino
# from tabulate import tabulate
import urllib.request

import sqlite3
import json

import  odoorpc


app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'
#app.jinja_env.add_static_folder('templates', 'static')

odoo=Felino()
# data = odoo.json('/web/session/authenticate',
#    {'db': 'db_name', 'login': 'admin', 'password': 'admin'})
# print(data)

menu=[{"name":"Partner","url":"partner"}
      
      ]

def menuodoo(menu,url):
    content=f"""
    <div class="o-dropdown dropdown o-dropdown--no-caret">
        <button class="dropdown-toggle"  onclick="geodoo('{url}')"
            tabindex="0" aria-expanded="false" data-menu-xmlid="stock.menu_stock_inventory_control">
            <span data-section="344">{menu}</span>
        </button>
    </div>
    """
    return content

def record(model,search):
    return odoo.env[model].search(search)

def listrecord(model,listrecord,field):
    result=odoo.execute(model, 'read',listrecord,field) 
    return result

@app.route("/")
def index():
    menu=""
    menu+=menuodoo('Partner','http://127.0.0.1:5000/dataset/res.partner')
    menu+=menuodoo('Product','dataset/product.product')
    menu+=menuodoo('WareHouse','/addon')
    menu+=menuodoo('Addpns','http://127.0.0.1:5000/addon')

    return render_template("index.html",menu=menu)
@app.route("/view")
def view():
    id=1512
    # view=odoo.env['ir.ui.view'].search([('id','=','1512')])[0]
    view=odoo.execute('ir.ui.view', 'read',[id],['arch_base','name','model'])[0]
    xmlstring=view.get('arch_base')
    
    with open(f'templates/{view.get("name")}.xml', "w") as file:
         file.write(xmlstring)
    xml_dict = xmltodict.parse(xmlstring)
    print(xml_dict)
    return view.get('arch_base')

@app.route("/addons")
def addons():
    model='ir.module.module'
    rec=record(model,[])
    image='icon_image';
    data=listrecord(model,rec,['name','display_name','icon','reports_by_module',])
    print(data)
    result=[]
    for recor in data:
        print(recor['name']) 
        recor['image']=f'/image?img={recor["id"]}'
        result.append(recor)                
    return jsonify(result)

@app.route("/image/<model>/<field>/<id>")
def image(model,field,id):
    result=odoo.execute(model, 'read',[int(id)],[field])
    #result=odoo.execute(model, 'read',record,[field])  
    print(result)
    gbr=base64.b64decode(result[0].get(field))
    return f'<img src="data:image/png;base64,{gbr} alt="Gambar">'
    #return base64.b64decode(result[0].get(field))


@app.route("/dataset/<model>")
def dataset(model):
   #result = execute(model, 'read',[int(id)] ,[field])  
   myid=request.args.get(id,1)  
#    id = request.args.get('id')  # Get `id` from query string
   if request.args.get('field'): 
            fields = request.args.get('field').split(',')  # Get `fields` as a list
   else:
        fields=['id','name']         
   search = request.args.get('search')  # Get `search` string

   print(id)  
   odoo.model=model
   odoo.field=fields
   odoo.record()
   data=odoo.listrecord()
#    rec=record(model,[])
#    data=listrecord(model,rec,fields) 
   return jsonify(data)    
#    return data
@app.route("/respartner")
def rubah():
    return redirect('/dataset/res.partner')

@app.route("/addon")
def addon4():
    data=Felino()
    hasil=data.addons()
    print(hasil)
    return render_template("base.html",isi=hasil)

@app.route("/warehouse")
def warehouse():
    data=Felino()
    hasil=data.warehouse()
    print(hasil)
    return render_template("base.html",isi=hasil)


if __name__ == "__main__":
    app.run(debug=True)

