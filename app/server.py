from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3

from app.config import SERVER_HOST, SERVER_PORT
from app.http_utils import parse_json_body, parse_query_params, send_json
from app.request_context import generate_request_id
from app.validation import validate_test_payload
from app.models import insert_test
from app.models import get_tests_by_clinic
from app.logger import log


class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        request_id = generate_request_id()

        if self.path != "/tests":
            send_json(self, 404, {
                "error": "Not found",
                "request_id": request_id
            })
            return

        payload = parse_json_body(self)
        if payload is None:
            send_json(self, 400, {
                "error": "Invalid or missing JSON body",
                "request_id": request_id
            })
            return

        valid, error = validate_test_payload(payload)
        if not valid:
            send_json(self, 400, {
                "error": error,
                "request_id": request_id
            })
            return

        try:
            insert_test(payload)
        except sqlite3.IntegrityError:
            log(
                level="warning",
                message="Duplicate test_id",
                endpoint="POST /tests",
                request_id=request_id,
                test_id=payload.get("test_id"),
            )
            send_json(self, 409, {
                "error": "test_id already exists",
                "request_id": request_id
            })
            return
        except Exception as exc:
            log(
                level="error",
                message="Database insert failed",
                endpoint="POST /tests",
                request_id=request_id,
                reason=str(exc),
            )
            send_json(self, 500, {
                "error": "Internal server error",
                "request_id": request_id
            })
            return

        log(
            level="info",
            message="Test created",
            endpoint="POST /tests",
            request_id=request_id,
            test_id=payload["test_id"],
        )

        send_json(self, 201, {
            "status": "success",
            "request_id": request_id
        })

    def do_GET(self):
        request_id = generate_request_id()

        if not self.path.startswith("/tests"):
            send_json(self, 404, {
                "error": "Not found",
                "request_id": request_id
            })
            return

        query_params = parse_query_params(self.path)
        clinic_id = query_params.get("clinic_id")

        if not clinic_id:
            send_json(self, 400, {
                "error": "Missing required query parameter: clinic_id",
                "request_id": request_id
            })
            return

        try:
            tests = get_tests_by_clinic(clinic_id)
        except Exception as exc:
            log(
                level="error",
                message="Database read failed",
                endpoint="GET /tests",
                request_id=request_id,
                clinic_id=clinic_id,
                reason=str(exc),
            )
            send_json(self, 500, {
                "error": "Internal server error",
                "request_id": request_id
            })
            return

        send_json(self, 200, {
            "clinic_id": clinic_id,
            "count": len(tests),
            "tests": tests,
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
