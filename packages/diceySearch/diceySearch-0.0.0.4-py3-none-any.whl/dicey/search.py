import requests
import json

def embedding_func(id, query, images=None):
    embedding_api = "http://43.200.239.247:8000/embedding/"
    if images:
      embed_data = {
          "images": images,
          "query": query,
          "id": str(id)
      }
    else:
      embed_data = {
          "images": [],
          "query": query,
          "id": str(id)
      }
    response = requests.post(embedding_api, data=json.dumps(embed_data), headers={"Content-Type": "application/json"},)
    res = tuple(response.json()["result"])
    return res

def data2vectordb(key_id, total_result=None):
  upsert_api = "http://52.79.176.35:8000/upsert/"
  if total_result is None:
    response = requests.get(upsert_api)
    raise Exception(response.json()['result'])    
  else:
    response = requests.post(upsert_api, data=json.dumps({"key_id": key_id, "result": total_result}), headers={"Content-Type": "application/json"},)
  return "Done"

def search_func(key_id, query, top_k, debug=False):
    search_api = "http://52.79.176.35:8000/search/"
    search_data = {
    "key_id": key_id,
    "query": query,
    "top_k": top_k,
    'debug': debug
    }
    response = requests.post(search_api, data=json.dumps(search_data), headers={"Content-Type": "application/json"},)
    res = response.json()
    return res['result'], res['score'], res['meta']