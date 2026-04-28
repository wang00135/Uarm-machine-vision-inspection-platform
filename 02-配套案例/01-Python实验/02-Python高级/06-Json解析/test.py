import json
data = {'name':'bkrc','age':10,'site':'beijing'}
js = json.dumps(data,sort_keys=True, indent=4, separators=(',', ': '))
print(js)


import json
js_data = '{"name":"bkrc","age":10,"site":"beijing"}'

text = json.loads(js_data)
print(text)
