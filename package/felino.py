form odoorpc import ODOO

class Felino(ODOO)
odoo  =  odoorpc.ODOO ('203.194.112.105',  port = 80 )
print(odoo.db.list())
odoo.login('SPRINGBED-OdooMates', 'felino', 'felino')

def record(model,search):
    return odoo.env[model].search(search)

def listrecord(model,listrecord,field):
    result=odoo.execute(model, 'read',listrecord,field) 
    return result

def Datarecord(model,search,field):
    return listrecord(model,record(model,[]),[field]) 