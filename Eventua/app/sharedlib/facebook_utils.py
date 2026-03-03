import requests

APP_ID="1639560757401239"
APP_SECRET="46780fd4e9708935724d84633a9b41d9"
SHORT_LIVED_USER_TOKEN = "EAAXTKZCyIVpcBQrpsZBjnP3TWSBYHLEO5s7psTGOsrM6DY1WZBRKUhMfDLhKf66i8ZCGidLeGkoiYuyhicaC7NiMAm1SnWds4SnnB65ZA4jw3CqCZCksgiYSrlMY5Ba2hBYpn1Ec86jvTu48G0GLLZBAlpReilvpZAqSGuNDZCltjczN6aBvQwj3Y3XUkNxczAn30qCRBygxnJNwvdVpcAneJtBJ3HANfoImLHZAcN5LPOer0lhMNheS0RlZCWzxUziIKKS2RI7FbJb6IkhIvp7nbJVFwGUZAASo7TqV7hwZD" 

def get_long_lived_user_token():
    short_token = SHORT_LIVED_USER_TOKEN
    url = "https://graph.facebook.com/v19.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": short_token
    }
    r = requests.get(url, params=params)
    return r.json()

def get_page_accounts(user_token):
    url = "https://graph.facebook.com/v19.0/me/accounts"
    params = {
        "access_token": user_token
    }
    r = requests.get(url, params=params)
    return r.json()

def post_to_page(fb_url, payload):
    r = requests.post(url = fb_url, data=payload)
    return r.json()

# # Example usage
# long_token_data = get_long_lived_user_token(SHORT_LIVED_USER_TOKEN)
# print(long_token_data)

# long_lived_token = long_token_data.get("access_token")

# if not long_lived_token:
#     print("Error:", long_token_data)
#     exit()

# print(f"long_lived_token: {long_lived_token}")

# pages = get_page_accounts(long_lived_token)
# print(f"pages: {pages}")

# #--------------

# page_id = pages["data"][0]["id"]
# page_access_token = pages["data"][0]["access_token"]

# print("PAGE_ID:", page_id)
# print("PAGE_ACCESS_TOKEN:", page_access_token)

# #--------------

# result = post_to_page(page_id, page_access_token)
# print(result)