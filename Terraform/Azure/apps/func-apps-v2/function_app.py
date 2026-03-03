from azure.functions import FunctionApp, HttpRequest, HttpResponse
import json

# Create the FunctionApp instance
app = FunctionApp(http_auth_level="anonymous")

# Define the function name and HTTP trigger route
@app.function_name(name="getCustnum")
@app.route(route="getCustnum", methods=["POST"])
def get_customer_num(req: HttpRequest) -> HttpResponse:
    try:
        return HttpResponse(f"Success", status_code=200)

    except Exception as e:
        return HttpResponse(f"Exception:{e}", status_code=400)
