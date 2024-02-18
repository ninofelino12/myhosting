import yaml

with open('app.yaml', 'r') as file:
        data = yaml.safe_load(file)

print(type(data))
print(data)
print('-------------------------')
print(data.get('res.partner')['Fields'])
fields=data.get('res.partner')['Fields']
print(type(fields))
print(fields[0])