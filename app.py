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
app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'
#app.jinja_env.add_static_folder('templates', 'static')
cse_key = "f4d4e4f0e6b294bd7"  # Replace with your actual key
cse_engine_id = "flaskodoo"  # Replace with your engine ID









odoo=Felino()
  #self.odoo  =  ODOO ('203.194.112.105',  port = 80 )
        #self.odoo  =  ODOO (self.server,  port = self.porta )
try:
    odoo.connect('localhost',8015)
    #odoo.connect('203.194.112.105',16000)
    odoo.logon()
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

@app.route("/home")
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

@app.route("/dashboard")
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


@app.route("/")
def index():
    return '1'

@app.route("/searchimage", methods=["GET", "POST"])
def search_images():
    if request.method == "POST":
        query = request.form.get("query")
        if not query:
            return render_template("index.html", error="Masukkan kata kunci pencarian.")

        url = f"https://www.googleapis.com/customsearch/v1?key={cse_key}&cx={cse_engine_id}&q={query}"
        response = requests.get(url)

        if response.status_code == 200:
            results = response.json().get("items", [])
            formatted_results = []
            print(results)
            for item in results:
                if item.get("image"):
                    title = item.get("title")
                    link = item.get("image").get("link")
                    thumbnail = item.get("image").get("thumbnailLink")
                    formatted_results.append({"title": title, "link": link, "thumbnail": thumbnail})
            return render_template("results.html", images=formatted_results)
        else:
            return render_template("index.html", error="Permintaan API gagal.")

    return render_template("search.html")
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
    gbr=odoo.image(model,field,id)
    print(gbr)
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

@app.route("/imagesql/<model>/<id>")
def imagesql(model,id):
    return   send_file(f'img/{model}-{id}.png', mimetype='image/png')   

@app.route("/getimage/<model>")
def imagesqlget(model):
    return   send_file(f'img/{model}', mimetype='image/png')  
  

     
@app.route("/sql/<model>")
def datasql(model):
    data=odoo.getJson(model)
    dataw=f'[{data[1:-1]}]'
    return dataw


@app.route("/dataset/<model>")
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

@app.route("/root")
def rootjs():
    data=Felino()
    hasil=data.rootJson()
    print(hasil)
    return jsonify(hasil)

@app.route('/search', methods=['GET', 'POST'])
def carih():
    # search_term = request.form['search_term']
    search_term='kucing'
    api_url = f"https://api.duckduckgo.com/?q={search_term}&format=json&iax=images&ia=images"
    response = requests.get(api_url)
    search_results = response.json()
    print(search_results)
    # images = [image['image'] for image in search_results['ia_data']['results']]
    return render_template('result.html',images=search_results)

if __name__ == "__main__":
    app.run()

