import requests


domain = "http://127.0.0.1:8000"
r = requests.request("GET", f"{domain}/word/guess")
print(r.status_code)
print(r.json())
