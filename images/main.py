"""Receive an HTTP event and pass it to your image handler."""

import functions_framework
from handler import handler


@functions_framework.http
def scale_http(request):
    event = request.get_json(silent=True)
    if not isinstance(event, dict):
        return {"error": "JSON event required"}, 400
    try:
        response = handler(event, None)
    except (KeyError, ValueError, FileNotFoundError) as error:
        return {"error": str(error)}, 400
    return (
        response.get("body", ""),
        response.get("statusCode", 500),
        {"Content-Type": "application/json"},
    )
