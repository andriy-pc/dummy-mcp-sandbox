import json
import sys

def handle(request):
    method = request.get("method")
    params = request.get("params", [])
    rid = request.get("id")

    # Route methods
    if method == "add":
        result = params[0] + params[1]
    elif method == "greet":
        result = f"Hello, {params[0]}!"
    else:
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}

    # Notifications (no id) get no response
    if rid is None:
        return None

    return {"jsonrpc": "2.0", "id": rid, "result": result}


for line in sys.stdin:
    request = json.loads(line)
    response = handle(request)
    if response:
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()