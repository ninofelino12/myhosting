from flask import Flask, Blueprint, render_template,jsonify,request,redirect,Response, send_file, make_response
import requests
from myclass import Felino
import sqlite3
import json
import  odoorpc
import base64
import yaml
from duckduckgo_search import *
from dotenv import load_dotenv
from flask_cors import CORS
import os
import socket

http = Flask(__name__)
# CORS(http)
http.config['STATIC_FOLDER'] = 'static'
#http.jinja_env.add_static_folder('templates', 'static')
cse_key = "f4d4e4f0e6b294bd7"  # Replace with your actual key
cse_engine_id = "flaskodoo"  # Replace with your engine 
base_url = os.getenv("BASE_URL")
base_odoo = os.getenv("ODOO")
base_database    = os.getenv("DATABASE")
base_port = os.getenv("PORT")
base_user = os.getenv("ODOOUSER")
base_pass = os.getenv("PASS")
print(base_url)
local_ip = socket.gethostbyname(socket.gethostname())
print(local_ip)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]
s.close()
print(local_ip)
odoo=Felino()
  #self.odoo  =  ODOO ('203.194.112.105',  port = 80 )
        #self.odoo  =  ODOO (self.server,  port = self.porta )
try:
    #odoo.connect('localhost',8015)
    odoo.connect('203.194.112.105',16000)
    print(base_pass)
    odoo.logon(base_database,base_user,'odooadmin')
except Exception as e:
    print("Connection error:", e)    
finally:
    print("not connect")    
menu=[{"name":"Partner","url":"partner"}]
#print(odoo.session)     

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

@http.route("/home")
def home():
    menu=""
    menu+=menuodoo('Partner','dataset/res.partner')
    menu+=menuodoo('Product Category','dataset/product.category')
    menu+=menuodoo('Product','dataset/product.product')
    menu+=menuodoo('Product Template','dataset/product.template')  
    menu+=menuodoo('WareHouse','dataset/stock.warehouse')
    menu+=menuodoo('Addons category','dataset/ir.module.category')
    menu+=menuodoo('Addons','dataset/ir.module.module')
    menu+=menuodoo('Addons','dataset/ir.module.module')
    menu+=menuodoo('Report','dataset/ir.actions.report')
    menu+=menuodoo('View','dataset/ir.ui.view')
    menu+=menuodoo('Model','dataset/ir.model')

    return render_template("index.html",menu=menu)

@http.route("/dashboard")
def dasboard():
    menu=""
    menu+=menuodoo('Partner','dataset/res.partner')
    menu+=menuodoo('Product Category','dataset/product.category')
    menu+=menuodoo('Product','dataset/product.product')
    menu+=menuodoo('WareHouse','dataset/stock.warehouse')
    menu+=menuodoo('Addons','dataset/ir.module.module')
    menu+=menuodoo('Report','dataset/ir.actions.report')
    menu+=menuodoo('View','dataset/ir.ui.view')
    menu+=menuodoo('Model','dataset/ir.ui.view')


    return render_template("dashboard.html",menu=menu)


@http.route("/")
def index():
    return '1'

@http.route("/view")
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



@http.route("/image/<model>/<field>/<id>")
def image(model,field,id):
    gbr=odoo.image(model,field,id)
    if len(gbr)>0:
       first_element = gbr[0]
       #avatar_128= first_element.get('image_1920', '')
       avatar_128= first_element.get(field, '')
       binary_image = base64.b64decode(avatar_128)
       print('simpan gambar')
       with open(f'img/{model}-{id}.png', 'wb') as file:
            file.write(binary_image)
       return Response(binary_image, mimetype='image/png')
    else:
        return "No Image"

    return base64.b64decode(result[0].get(field))

@http.route("/imagesql/<model>/<id>")
def imagesql(model,id):
    return   send_file(f'img/{model}-{id}.png', mimetype='image/png')   

@http.route("/getimage/<model>")
def imagesqlget(model):
    return   send_file(f'img/{model}', mimetype='image/png')  
  

     
@http.route("/sql/<model>")
def datasql(model):
    data=odoo.getJson(model)
    dataw=f'[{data[1:-1]}]'
    return dataw


@http.route("/dataset/<model>")
def dataset(model):
   with open('app.yaml', 'r') as file:
        data = yaml.safe_load(file)
   fields_by_model = {}
   for model_name, config in data.items():
        fields = config.get('Field', [])  # Use get() to handle missing 'Field' key
        fields_by_model[model_name] = fields
     
   myid=request.args.get(id,1)  
#    id = request.args.get('id')  # Get `id` from query string
   if request.args.get('field'): 
            fields = request.args.get('field').split(',')  # Get `fields` as a list
   else:
        fields=['id','name']         
   search = request.args.get('search')  # Get `search` string
    
   print(id)  
    
   
   odoo.model=model
   odoo.field=data.get(model)['Fields']
   odoo.images=''
   if 'images' in data.get(model):
      odoo.images=data.get(model)['images'][0] 
    
  
   odoo.record()
   data=odoo.listrecord()
   print(type(data))
   print('------------------------------')
   odoo.safeJson(model,json.dumps(data))
#    rec=record(model,[])
#    data=listrecord(model,rec,fields) 
   return jsonify(data)    
#    return data


@http.route("/addons")
def addons():
    
    model='ir.module.module'
    fields=['name','display_name','icon','reports_by_module','description','application','web','sequence']
              
    return jsonify(result)

@http.route("/product/<model>/<int:id>")
def rubah(model,id):
    if model=='home':
       return render_template("productcategory.html")

    data = {
        "product.category": {
            "search": [],
            "fields": ["id", "name"],
            "child"  : "product.product"
        },
        "product.product": {
            "search": [("categ_id", "=", id)],
            "fields": ["id", "name", "categ_id"],
             "child"  : "product.template"

        },
        "product.template": {
            "search": [],
            "fields": ["id", "name"],
             "child"  : "product.template"
        }
    }
    with open('static/product.yaml', 'w') as file:
         yaml.dump(data, file)
    model_data = data.get(model)
    categories = odoo.odoo.env[model].search(model_data["search"])
    categories = odoo.odoo.execute(model, 'read', categories, model_data["fields"])
    for item in categories:
        item["link"] = f"/product/{model_data['child']}/{item['id']}"
        item["ref"] = f"<a href='product/{model_data['child']}/{item['id']}'>a</a>'"
   
    

    response = make_response(jsonify(categories))
    # response.headers['X-Custom-Header'] =json.dumps(model_data["fields"])
    # response.headers['link'] = '<a href="prod?product_id=${item.id}">${item.name}</a>)'
    response.headers.add('Access-Control-Allow-Origin', '*') 
    return response

   
@http.route("/addon")
def addon4():
    data=Felino()
    hasil=data.addons()
    print(hasil)
    return render_template("base.html",isi=hasil)

@http.route("/warehouse")
def warehouse():
    data=Felino()
    hasil=data.warehouse()
    print(hasil)
    return render_template("base.html",isi='isi')

@http.route("/root")
def rootjs():
    data=Felino()
    hasil=data.rootJson()
    print(hasil)
    return jsonify(hasil)



@http.route('/prod')
def productObject():
    categ_id = request.args.get("categ_id", type=int)
    jenis = request.args.get("type")
    product_id = request.args.get("product_id")
    if categ_id:
        fields=['id','name','child_id','product_count','child_id']
        model='product.product'
        categories = odoo.odoo.env[model].search([('categ_id','=',categ_id)])
        categories = odoo.odoo.execute('product.product', 'read', categories, ['id','name','categ_id'])
     
    elif product_id:
        fields=['id','name','product_variant_id','product_variant_ids']
        categories = odoo.odoo.env['product.template'].search([])
        categories = odoo.odoo.execute('product.template', 'read', categories, fields)
       
    else:
        
        fields=['id','name','child_id','product_count','child_id']
        categories = odoo.odoo.env['product.category'].search([])
        categories = odoo.odoo.execute('product.category', 'read', categories, fields)
       
    
    response = make_response(jsonify(categories))
    response.headers['X-Custom-Header'] =fields
    response.headers['link'] = '<a href="prod?product_id=${item.id}">${item.name}</a>)'
    response.headers.add('Access-Control-Allow-Origin', '*') 
    return response


if __name__ == "__main__":
    http.run(host='0.0.0.0', port=5000)

