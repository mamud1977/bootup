v_dict = {"name":"Mamud",
           "dob": "17/12/1977",
           "loc": "Kolkata"}

def my_function(my_dict):
    for key, value in my_dict.items():
        print(f"Key: {key}, Value: {value}")


    query_params = my_dict
    excluded_params = ["domain", "stage", "base_url", "auth_headers", "api_key_id"]
    params = {k: v for k, v in query_params.items() if k not in excluded_params}
    print(params)

my_function(v_dict)