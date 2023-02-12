import requests as rq

print(rq.get("http://127.0.0.1:8000/").json())
print(rq.get("http://127.0.0.1:8000/items?count=5").json())
