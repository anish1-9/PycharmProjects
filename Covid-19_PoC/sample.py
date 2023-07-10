# 1.Collect 100 cat facts from the URL, make a list and save them to a json file
# https://catfact.ninja/fact

import json
import urllib.request

parsed_list = []
for i in range(1, 5):
    response = urllib.request.urlopen('https://catfact.ninja/fact')
    parsed_list = json.loads(response.read())
    print("Dumped object " + str(i) + " into JSON file")
with open('new_file2.json', 'w+') as f:
    json.dump(parsed_list, f, indent=5)
f.close()

"""

# 2.From the json file pick a random fact and display

"""

# with open('new_file2.json', 'r') as f:
#       for i in f:
#         print("fact"[i])
# f.close()


"""

#3. Read the JSON file, sort them according to "length" and save it back to the same JSON file

"""

# with open('new_file2.json', 'w+') as f:
#     for i in range(1,101):
#             response = urllib.request.urlopen('https://catfact.ninja/fact')
#             json_data=response.read()
#             parsed_list=json.loads(json_data)
#             json.dump(parsed_list, f,indent=5)
#             print("Dumped object "+str(i)+ " into JSON file")
# f.close()
