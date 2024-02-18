# import odoorpc
import yaml
import logging
import pickle
from odoorpc import ODOO,report
from odoo_rpc_client import Client


import base64


class OdooClient(ODOO):
    '''
      
    '''  
    
    
             
    def __init__(self, server,port,dbname,user,password):
        super(OdooClient, self).__init__(server, port=port)
        self.login(dbname, user, password)
        self.session = super.env.session
        #self.infoo = self.get.session()
        # with open('model.yaml', "r") as f:
        #      self.data = yaml.load(f, Loader=yaml.FullLoader)
        # self.model=self.data['model']

    def setmodel(self,model,field,search,image):
        self.model=model
        self.field=field
        self.search=search
        self.image=image
    
    def getmodel(self):
        record=self.env[self.model].search(self.search)
        hasil=self.execute(self.model, 'read',record,self.field)
        result=[]
        for item in hasil:  
            if self.image:
               item[self.image] = f'<img src="image/{self.model}/{item["id"]}"/>'
            result.append(item)
        return result

    def getAttachment(self):
        data=self.f_browse('ir.model.fields',[('model','=',self.model),('ttype','=','binary')],['id','name','ttype'])
        return  [item['name'] for item in data if item['ttype'] == 'binary']
    def user(self):
        """
        This method is a custom method that is added to the class.
        """

        return self.odoo.env.user
    
    def f_execute_byid(self, models, id, type):
        with open('model.yaml', 'r') as f:
             model_data = yaml.load(f, Loader=yaml.FullLoader)
        #model_data=self.data
        model_name = model_data[models]['model']
        field='image_128'
        record=[int(id)]
        result = self.execute(model_name, 'read',[int(id)] ,[field])      
        return base64.b64decode(result[0].get(field))    
    
    def get_view(self, models, field, id):
        record=[int(id)]
        result = self.execute(models, 'read',[int(id)] ,[field])      
        return result[0].get(field)

    def nav(self):
        with open('model.yaml', 'r') as f:
             data = yaml.load(f, Loader=yaml.FullLoader)
        #data=self.data
        links = [value['name'] for value in data.values()] 
        combined_list = [(data[key]['name'], data[key]['model']) for key in data]
        html_links = ['<a href="/model/{}">{}</a>'.format(model, name) for name, model in combined_list]
        html_string = ''.join([f'<a href="">{link}</a>' for link in links])

        html_links_string = ''.join(['<button class="btn btn-primary o_form_button_edit"  onclick="getContent(\'{}\',\'html\')">{}</button>'.format(model,name) for name, model in combined_list])
        model_name =  data.get('name')
        model_model = data.get('model')
           
        return html_links_string     
        
    def f_browse(self,model,search,field):
        '''
        f_browse(model,search,field)
        model
        search [('id', '=', int(id))]
        field
        limit
        '''   
        record = self.env[model].search(search) 
        result = self.execute(model, 'read', record, field)
        return result
           
        
        
    def nav2(self):
        with open('model.yaml', "r") as f:
             data = yaml.load(f, Loader=yaml.FullLoader)
             links = [value['name'] for value in data.values()] 
             combined_list = [(data[key]['name'], data[key]['model']) for key in data]
             html_links = ['<a href="/model/{}">{}</a>'.format(model, name) for name, model in combined_list]
             html_string = ''.join([f'<a href="">{link}</a>' for link in links])

             html_links_string = ''.join(['<button onclick="getContent(\'{}\',\'html\')">{}</button>'.format(model,name) for name, model in combined_list])
             model_name =  data.get('name')
             model_model = data.get('model')
           
        return html_links_string 
    
    def f_execute_byid2(self,models,
                       id,type):
        with open('model.yaml', "r") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        # oo
        if type=="jpg":
            if (models=="res.partner"):
                field="avatar_128"
            else:
              field="image_128"
            
            record = super().env[data[models]['model']].search([('id', '=',int(id))])
            partner_data = record[0]
            #image_data = partner_data.get('avatar_128')
            result=self.execute(data[models]['model'], 'read',record,[field])  
            return base64.b64decode(result[0].get(field))
        elif type=="xml":
            field="arch_base"
            record = super().env[data[models]['model']].search([('id', '=', 4)])
            partner_data = record[0]
            result=self.execute(data[models]['model'], 'read',record,[field])  
            return result[0].get(field)
        else:
            field=data[models]['field'].split(',')
            record=super().env[data[models]['model']].search([])
            result=self.execute(data[models]['model'], 'read',record,field)    
        return result
    
    def f_execute(self,models,type):
        with open('model.yaml', "r") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        # oo
        if type=="jpg":
            field="avatar_128"
            record = super().env[data[models]['model']].search([('id', '=', 15)])
            partner_data = record[0]
            #image_data = partner_data.get('avatar_128')
            result=self.execute(data[models]['model'], 'read',record,[field])  
            return base64.b64decode(result[0].get(field))
        elif type=="xml":
            field="arch_base"
            record = super().env[data[models]['model']].search([('id', '=', 4)])
            partner_data = record[0]
            result=self.execute(data[models]['model'], 'read',record,[field])  
            return result[0].get(field)
        else:
            field=data[models]['field'].split(',')
            record=super().env[data[models]['model']].search([])
            result=self.execute(data[models]['model'], 'read',record,field)    
        return result
        
    def image():
        return "image"  
    def save():
        serialized_object = pickle.dumps(MyOdooClient)
        with open('object.class', 'wb') as file:
            file.write(serialized_object)

    def has_key(item,key):
        return key in item

    def ubah_key(item,model):
        if self.has_key(item,'avatar_128'):
            item['avatar_128']=f'<img src="image?id={item["id"]}&model={model}"/>'
        if self.has_key(item,'image_128'):
            item['image_128']=f'<img src="image?id={item["id"]}&model={model}"/>'     
        return item

    def company(self):
        user = super().env.user
        # print(user.name)            # name of the user connected
        # print(user.company_id.name)
        # print(dir(user))
        
        # print(user.company_id.email)
        # print(user.company_id.website_url)
        # print(user.company_id.phone)
        # print(user.company_id.street)
        # print(dir(user.company_id.message_unread))
        reports = super().report.list()
        print(dir(report)) 
        #report_data = super().report('repor').get_pdf([212])
        client = Client("localhost:8015", 'felino','ninofelino@gmail.com','felino')
        print(dir(client))
        report_list = client.report.list()
        for report_info in report_list:
            print("Report ID:", report_info.get('id'))
            print("Report Name:", report_info.get('name'))
            print("Report Model:", report_info.get('model'))
            print("-------------")
        return "info"
    
    def process_value(self,key, value):
        if isinstance(value, dict):
            return self.generate_html2(value)
        else:
            return f"{key}>{value}</{key}>"

    
    
    def generate_html(self,my_dict):
        html = ""
        for key, value in my_dict.items():
            html += f"<{key}>"
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    html += f"<{subkey}>"
                if subvalue:
                    #html += f"<{subkey}>{''.join(str(x) for x in subvalue)}</{subkey}>"
                   if type(subvalue) is dict:
                      #print(subkey,type(subvalue),'--------------->',subvalue)
                      buttons = subvalue.get('button', [])
                      if buttons:
                         print(buttons)
                         for button in buttons:
                             print(button['@string'])   
                             tag=button['@string']
                             fclass=button['@class']
                             html +=f'<button class="{fclass}">{tag}</button>'
                             print('000000000000000000')
                         #isinya = buttons.get('@string', None)
                         
                elif isinstance(subvalue, dict):
                    html += self.generate_html(subvalue)  # Recursion for nested dictionaries
                    html += f"</{subkey}>"
                else:
                    html += str(value)  # Handle non-dictionary values directly
        html += f"</{key}>"
        return html

# Prepare the connection to the server

