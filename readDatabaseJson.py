import json
file1 = open ('eventhorizonDatabaseJsonImportant.json', encoding="utf8")
result = json.load(file1)
print(len(result['values']))
for i in range(len(result['values'])):
    item = result['values'][i]
    to_print = f"{i+1}, id: {item[0]}, lang: {item[11]}"
    if item[7]:
        to_print += f", email: {item[7]}"
    if item[13]:
        to_print += f", line: {item[13]}"
    print(to_print)