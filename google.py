import json
import functions_framework

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Expects JSON with 'hba1c' (or a query param as fallback).
    Returns a JSON classification of HbA1c.
    Reference: ADA Standards of Care 2024 [web:1].
    """
    # Prefer JSON body; fall back to query parameter if needed
    data = request.get_json(silent=True) or {}
    args = request.args or {}

    hba1c = data.get("hba1c", args.get("hba1c"))

    # Presence check
    if hba1c is None:
        return (
            json.dumps({"error": "'hba1c' is required."}),
            400,
            {"Content-Type": "application/json"},
        )

    # Type/convert check
    try:
        hba1c_val = float(hba1c)
    except (TypeError, ValueError):
        return (
            json.dumps({"error": "'hba1c' must be a number."}),
            400,
            {"Content-Type": "application/json"},
        )

    status = "normal" if hba1c_val < 5.7 else "abnormal"
    category = "Normal (<5.7%)" if status == "normal" else "Abnormal (≥5.7%)"

    payload = {
        "hba1c": hba1c_val,
        "status": status,
        "category": category,
    }

    return json.dumps(payload), 200, {"Content-Type": "application/json"}