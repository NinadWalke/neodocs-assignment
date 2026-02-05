from http.server import HTTPServer, BaseHTTPRequestHandler
from app.config import SERVER_HOST, SERVER_PORT
from app.http_utils import parse_json_body, parse_query_params, send_json
from app.request_context import generate_request_id

# as per this version of the code, we have simply added GET and POST with no endpoint to handle them as of now

class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        request_id = generate_request_id()

        if self.path == "/tests":
            body = parse_json_body(self)
            if body is None:
                send_json(self, 400, {
                    "error": "Invalid or missing JSON body",
                    "request_id": request_id
                })
                return

            send_json(self, 501, {
                "error": "POST /tests not implemented yet",
                "request_id": request_id
            })
            return

        send_json(self, 404, {
            "error": "Not found",
            "request_id": request_id
        })

    def do_GET(self):
        request_id = generate_request_id()

        if self.path.startswith("/tests"):
            query_params = parse_query_params(self.path)

            send_json(self, 501, {
                "error": "GET /tests not implemented yet",
                "request_id": request_id,
                "query": query_params
            })
            return

        send_json(self, 404, {
            "error": "Not found",
            "request_id": request_id
        })

    def log_message(self, format, *args):
        return


def run_server():
    server = HTTPServer((SERVER_HOST, SERVER_PORT), RequestHandler)
    print(f"Server running on http://{SERVER_HOST}:{SERVER_PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
