from odoorpc import ODOO,rpc
from pprint import pprint as pp
import base64
# from tabulate import tabulate

import sqlite3
import json

class Felino(ODOO):

    def __init__(self):
        #super().__init__()
        self.model = 'res.partner'
        self.database ='DEMO'
        self.user='admin'
        self.password='odooadmin'
        self.field=['id','name']
        self.images=''
        self.lsrecord=[]
        self.search=[]
        self.server='localhost'
        self.porta=8015
        _name = 'my.model'
        #self.odoo  =  ODOO ('203.194.112.105',  port = 80 )
        #self.odoo  =  ODOO (self.server,  port = self.porta )
       
        
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS json_data
                (key  TEXT  PRIMARY KEY ,name TEXT , data TEXT, yaml TEXT)
                       ''')
    def connect(self,server,port):
        self.odoo  =  ODOO (server,  port = port ) 
        print(self.odoo.db.list())

    def logon(self,database,user,password):
        self.odoo.login(database,user,password)

    def record(self):
        self.lsrecord=self.odoo.env[self.model].search(self.search)
        return self.lsrecord

    def listrecord(self):
        # result=self.odoo.execute(self.model, 'read',
        result=self.odoo.execute(self.model, 'read',self.lsrecord,self.field)
        if self.images !='':
           print('ada')
           print(self.images)  
           for item in result:
                item["img"] = f'<img src="image/'+f'{self.model}/{self.images}/{item["id"]}'+'">'
                item['model']=self.model

                print( item["img"])    
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
    def safeJson(self,model,data):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('REPLACE INTO json_data (data,key) VALUES (?,?)', (data,model))
        conn.commit()
        conn.close()
    def getJson(self,model):
        query = f'SELECT data FROM json_data WHERE key="{model}"'
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute(query)
        data = c.fetchone()
        print(data[0])
        conn.close()
        return data[0]
    
    def rootJson(self):
        query = f'SELECT key,name FROM json_data '
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute(query)
        data = c.fetchall()
        conn.close()
        return data
    
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
