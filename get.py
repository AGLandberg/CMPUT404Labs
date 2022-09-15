import requests

print(requests.get("http://www.google.com"))

response = requests.get("http://raw.githubusercontent.com/AGLandberg/CMPUT404Labs/main/get.py")

open("lab1file.py", "wb").write(response.content)

print(response.text)



