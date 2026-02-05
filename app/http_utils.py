import json
from urllib.parse import urlparse, parse_qs


def parse_json_body(handler):
    content_length = handler.headers.get("Content-Length")
    if not content_length:
        return None

    try:
        length = int(content_length)
        raw_body = handler.rfile.read(length)
        return json.loads(raw_body.decode("utf-8"))
    except (ValueError, json.JSONDecodeError):
        return None


def parse_query_params(path: str) -> dict:
    parsed = urlparse(path)
    params = parse_qs(parsed.query)
    return {k: v[0] for k, v in params.items()}


def send_json(handler, status_code: int, payload: dict):
    response = json.dumps(payload).encode("utf-8")
    handler.send_response(status_code)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(response)))
    handler.end_headers()
    handler.wfile.write(response)
