from odoorpc import ODOO,rpc
from pprint import pprint as pp
import base64
# from tabulate import tabulate

import sqlite3
import json

class Felino(ODOO):

    def __init__(self):
        #super().__init__()
        self.odoo  =  ODOO('203.194.112.105',  port = 80 )

        self.model = 'res.partner'
        self.database ='DEMO'
        self.user='admin'
        self.password='odooadmin'
        self.field=['id','name']
        self.lsrecord=[]
        self.search=[]
        # self.session=''
        _name = 'my.model'
        self.odoo  =  ODOO ('203.194.112.105',  port = 80 )
        # self.odoo  =  ODOO ('sunber-digital.odoo.com',  port = 80 )
        self.session=self.odoo.login(self.database,self.user,self.password)
        print('---------------------------------------')
        print(self.session)
        print(self.odoo.db.list())
        
        # cnt = rpc.ConnectorJSONRPC('203.194.112.105', port=80)    
        # info=cnt.proxy_json.web.session.authenticate(db=self.database, login=self.user, password=self.password)      
        # info=info.get('result')
        # print(info.get('web.base.url'))
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS json_data
                (id INTEGER PRIMARY KEY, data JSON)''')
        data = {'name': 'John', 'age': 30, 'city': 'New York'}
        cursor.execute("INSERT INTO json_data (data) VALUES (?)", (json.dumps(data),))

        # Melakukan commit transaksi
        conn.commit()

# Mengambil data JSON dari database
        cursor.execute("SELECT data FROM json_data")
        result = cursor.fetchone()
    def logon(self):
        self.odoo.login(self.database,self.user,self.password)

    def record(self):
        self.lsrecord=self.odoo.env[self.model].search(self.search);
        return self.lsrecord

    def listrecord(self):
        # result=self.odoo.execute(self.model, 'read',
        result=self.odoo.execute(self.model, 'read',self.lsrecord,self.field) 
        return result

    def Datarecord(self,**kwargs):
        self.model = kwargs.get("model",self.model) 
       
        self.record()
        # hasil=self.listrecord()
        print(self.model)
        print(self.lsrecord)
        hasil=self.odoo.execute(self.model, 'read',self.lsrecord,self.field)
        return hasil 
    def getFields2(self):
        result=self.odoo.execute(self.model, 'read',self.lsrecord)
        for item in result:
            print(item)
        #print(result)
    def getFields(self):
        return self.odoo.env[self.model].fields_get()
    def report(self):
        cetak=self.odoo.report.list()
        report = self.odoo.report.download('account.report_invoice', [1])
        print(cetak)
        return cetak
    def image(self,model,field,id):
         result=self.odoo.execute(model, 'read',[int(id)],[field])
         #gbr=base64.b64decode(result[0].get(field))
         #return f'<img src="data:image/png;base64,{gbr} alt="Gambar">'
         return result
    def addons(self):
        self.model='ir.module.module'
        self.field=['id','name','website','author','sequence','category_id','reports_by_module']
        my_dict = self.Datarecord(model='ir.module.module')
        # max_key_len = max(len(key) for key in my_dict.keys())
        # max_val_len = [max(len(str(val)) for val in vals) for vals in my_dict.values()]
        # header = "| " + " ".join([key.ljust(max_key_len) for key in my_dict.keys()]) + " |"
        # print(header)
        hasil=''
        for item in my_dict:
            hasil+=f'<li><div>{item["reports_by_module"]}{item["category_id"]}<a href="{item["website"]}">{item["name"]}</a><span>{item["author"]}</span></li></div>'
            item['description']='<a href=""></a>'
            item['name']=f"<a>{item['name']}</a>"
           
        #print(tabulate(my_dict,headers="keys"))
        return hasil
    def kanban(self,header,content):
        formatted_text = f"""This is a very long string that spans multiple lines
(It can be difficult to read and work with in Python code.)
Using f-strings can make it easier to manage and format long strings"""

        
        htm = f"""
        <div class= 'oe_kanban_color_0 o_kanban_record ' name= 'stock_picking ' modifiers= ' ' tabindex= '0 ' role= 'article '>
             <div modifiers= ' '>
            <div class= 'o_kanban_card_header ' modifiers=>
                                        <div class= 'o_kanban_card_header_title ' modifiers= ' '>
                                        {header}
                                            <div class= 'o_primary ' modifiers= ' '>
                                            pRIMARY
                                                <a modifiers= ' ' data-type= 'object ' data-name= 'get_stock_picking_action_picking_type ' href= '# ' class= ' oe_kanban_action oe_kanban_action_a '>
                                                    <span>{header}</span>
                                                </a>
                                            </div>
                                            
                                            <div class= 'o_secondary ' modifiers= ' '></div>
                                        </div>
                                        <div class= 'o_kanban_manage_button_section ' modifiers= ' '>
                                            o_kanban_manage_button_section
                                            <a class= 'o_kanban_manage_toggle_button ' href= '# ' modifiers= ' '><i class= 'fa fa-ellipsis-v ' role= 'img ' aria-label= 'Manage ' title= 'Manage ' modifiers= '  '></i></a>
                                        </div>
                                    </div>
                                    <div class= 'container o_kanban_card_content ' modifiers= ' '>
                                     {content}
                                        <div class= 'row ' modifiers= ' '>
                                            <div class= 'col-6 o_kanban_primary_left ' modifiers= ' '>
                                                <button class= 'btn btn-primary oe_kanban_action oe_kanban_action_button ' modifiers= ' ' options= ' ' data-name= 'get_action_picking_tree_ready ' data-type= 'object ' type= 'button '>
                                                    <span modifiers= ' '>3 To Process</span>
                                                   
                                                    
                                                </button>
                                            </div>
                                            <div class= 'col-6 o_kanban_primary_right ' modifiers= ' '>
                                                <div class= 'row ' modifiers= ' '>
                                                </div>

                                                

                                                <div class= 'row ' modifiers= ' '>
                                                    <div class= 'col-12 ' modifiers= ' '>
                                                        <a class= 'oe_kanban_stock_picking_type_list oe_kanban_action oe_kanban_action_a ' modifiers= '  ' data-name= 'get_action_picking_tree_late ' data-type= 'object ' href= '# '>
                                                            <span>3</span>
                                                            Late
                                                        </a>
                                                    </div>
                                                </div>                   
        </div>                                            
        """
        
        return htm
    def warehouse(self):
        self.model='stock.location'
        self.field=['id','name','location_id']
        my_dict = self.Datarecord(model='stock.location')
        hasil='<div class="o_kanban_view oe_background_grey o_kanban_dashboard o_emphasize_colors o_stock_kanban o_kanban_ungrouped">'
        for item in my_dict:
            hasil+=self.kanban(item["location_id"],item["name"])
            # hasil+=f'<div class="oe_kanban_color_0 o_kanban_record">'
            # hasil+=f'<div class="oe_kanban_color_0 o_kanban_record">'
            # hasil+=f'<div class="o_kanban_card_header">'
            # hasil+=f'{item["location_id"]}</div>'
            # hasil+=f'<div class="oe_kanban_action oe_kanban_action">'
            # hasil+=f'{item["name"]}<a href="{item["id"]}">{item["name"]}</a><span>{item["name"]}</span></div></div></div>'
        
        print(my_dict)
        return hasil+'</div>'
        
# datas = Felino()
# datas.warehouse()
# datas.addons()
# datas.model='res.partner'
# datas.field=['id','name']
# datas.record()
# datas.listrecord()
#print('------------ My class')
#print(datas.Datarecord())
#print(datas.Datarecord(model="product.product"))
# print(datas.Datarecord(model="product.product",field=['id','name','desc']))
#print(datas.getFields())
#datas.report()
# print(datas.getFields2())
