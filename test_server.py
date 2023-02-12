import requests as rq

print(rq.get("http://127.0.0.1:8000/").json())
print("\n")
print(rq.get("http://127.0.0.1:8000/items?count=5").json())
print("\n")
print(rq.put("http://127.0.0.1:8000/items/1?name=BruhNah").json())
print("\n")
print(rq.get("http://127.0.0.1:8000/").json())
print("\n")
print(rq.delete("http://127.0.0.1:8000/items/1").json())
print("\n")
print(rq.get("http://127.0.0.1:8000/").json())
print("\n")