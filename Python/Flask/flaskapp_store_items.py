from flask import Flask, request

app = Flask(__name__)
print(f'app: {app}')

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "table", 
                "price": 12.0 
            },
            {
                "name": "Computer", 
                "price": 240.0 
            }

        ]
    }
]


@app.get("/store")   # http://127.0.0.1:5000/store
def get_all_stores():
    return {"Stores": stores}

@app.get("/store/<string:name>")   # # http://127.0.0.1:5000/store/Gopal Stores/Horlicks
def get_a_store(name):
    for store in stores:
        if store["name"] == name:
            return store, 201
    return 'Store not found', 404


@app.get("/store/<string:name>/item")   # # http://127.0.0.1:5000/store/Gopal Stores/Horlicks
def get_a_store_items(name):
    for store in stores:
        if store["name"] == name:
            return store["items"], 201
    return 'Store not found', 404



# Client sends data a JSON payload in the body.

@app.post("/store")   # http://127.0.0.1:5000/store
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items":[] }
    print(f'request_data: {request_data}')
    stores.append(new_store)
    return new_store, 201

# Client sends data with URL.

@app.post("/store/<string:name>/item")   # # http://127.0.0.1:5000/store/Gopal Stores/Horlicks
def create_item1(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"] , "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return 'Store not found', 404

@app.post("/store/<string:name>")   # # http://127.0.0.1:5000/store/Gopal Stores/Horlicks
def create_item2(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"] , "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return 'Store not found', 404