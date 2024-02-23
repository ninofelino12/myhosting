from flask import Flask, Blueprint, render_template,jsonify,request,redirect,Response, send_file
import requests
from myclass import Felino
import sqlite3
import json
import  odoorpc
import base64
import yaml
from duckduckgo_search import *


# [[pw{Ib=a1!J
#web_bp = Blueprint("web", __name__, static_folder='web', static_url_path="/static")
http = Flask(__name__)
http.config['STATIC_FOLDER'] = 'static'
#http.jinja_env.add_static_folder('templates', 'static')
cse_key = "f4d4e4f0e6b294bd7"  # Replace with your actual key
cse_engine_id = "flaskodoo"  # Replace with your engine ID









odoo=Felino()
  #self.odoo  =  ODOO ('203.194.112.105',  port = 80 )
        #self.odoo  =  ODOO (self.server,  port = self.porta )
try:
    odoo.connect('localhost',8015)
    #odoo.connect('203.194.112.105',16000)
    odoo.logon('DEMO','admin','odooadmin')
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

@http.route("/addons")
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
        result.httpend(recor)                
    return jsonify(result)

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
@http.route("/respartner")
def rubah():
    return redirect('/dataset/res.partner')

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
    return render_template("base.html",isi=hasil)

@http.route("/root")
def rootjs():
    data=Felino()
    hasil=data.rootJson()
    print(hasil)
    return jsonify(hasil)

@http.route('/search', methods=['GET', 'POST'])
def carih():
    # search_term = request.form['search_term']
    search_term='kucing'
    api_url = f"https://api.duckduckgo.com/?q={search_term}&format=json&iax=images&ia=images"
    response = requests.get(api_url)
    search_results = response.json()
    print(search_results)
    # images = [image['image'] for image in search_results['ia_data']['results']]
    return render_template('result.html',images=search_results)

@http.route('/prod')
def iproducta():
    categ_id = request.args.get("categ_id", type=int)
    jenis = request.args.get("type")
    if categ_id:
        categories = odoo.odoo.env['product.product'].search([('categ_id','=',categ_id)])
        categories = odoo.odoo.execute('product.product', 'read', categories, ['id','name','categ_id'])
        if jenis:
           html="<table>"
           for item in categories:
               link=f'{item["categ_id"]}'
               html+=f'<tr><td>{item["name"]}</td><td><a href="{link}">{item["categ_id"]}</a></td></tr>'
               
           return html+'</table>'
          
    else:
        categories = odoo.odoo.env['product.category'].search([])
        categories = odoo.odoo.execute('product.category', 'read', categories, ['id','name','child_id','product_count','child_id'])
        if jenis:
           html="<table>"
           for item in categories:
               link=f'prod?categ_id={item["id"]}&type=html'
               html+=f'<tr><td>{item["name"]}</td><td><a href="{link}">{item["product_count"]}</a></td><td>{item["child_id"]}</td></tr>'
               
           return html+'</table>'
    return jsonify(categories)


if __name__ == "__main__":
    http.run()

