import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger1")
def http_trigger1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Parse input parameters
    name = req.params.get('name')
    hba1c = req.params.get('hba1c')
    if not name or not hba1c:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = {}
        name = name or req_body.get('name')
        hba1c = hba1c or req_body.get('hba1c')

    if not name or hba1c is None:
        return func.HttpResponse(
            "Please provide 'name' and 'hba1c' in the query string or request body.",
            status_code=400
        )

    try:
        hba1c_val = float(hba1c)
    except (TypeError, ValueError):
        return func.HttpResponse(
            "'hba1c' must be numeric.",
            status_code=400
        )

    status = "normal" if hba1c_val < 5.7 else "abnormal"

    response_message = f"Hi {name}, your hba1c value is {hba1c_val}, it is {status}"

    return func.HttpResponse(response_message, status_code=200)