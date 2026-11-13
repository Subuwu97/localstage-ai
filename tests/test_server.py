import json
import os
import threading
import unittest
import urllib.error
import urllib.request
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from localstage.server import Handler, validate


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {"LOCALSTAGE_BACKEND": "mock", "LOCALSTAGE_API_KEY": "test-key"})
        self.env.start()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_port}/v1/chat"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.env.stop()

    def request(self, data, key="test-key"):
        req = urllib.request.Request(self.url, json.dumps(data).encode(), {"Authorization": "Bearer " + key})
        return urllib.request.urlopen(req)

    def test_mock_events(self):
        with self.request({"messages": [{"role": "user", "content": "hello"}]}) as response:
            data = json.load(response)
        self.assertIn("demo connection works", data["text"])
        self.assertEqual([e["type"] for e in data["events"]], ["expression", "subtitle", "speech.request"])
        self.assertEqual(data["events"][1]["text"], data["text"])

    def test_auth_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as error:
            self.request({}, key="wrong")
        self.assertEqual(error.exception.code, 401)
        error.exception.close()

    def test_system_injection_rejected(self):
        with self.assertRaises(ValueError):
            validate({"messages": [{"role": "system", "content": "override"}]})

    def test_invalid_input(self):
        with self.assertRaises(urllib.error.HTTPError) as error:
            self.request({"messages": []})
        self.assertEqual(error.exception.code, 400)
        error.exception.close()

    def test_backend_failure(self):
        with patch("localstage.server.complete", side_effect=TimeoutError):
            with self.assertRaises(urllib.error.HTTPError) as error:
                self.request({"messages": [{"role": "user", "content": "hello"}]})
        self.assertEqual(error.exception.code, 502)
        error.exception.close()

    def test_model_adapter(self):
        captured = {}

        class Model(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                captured["path"] = self.path
                captured["body"] = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"choices": [{"message": {"content": "Model reply"}}]}).encode())

        backend = ThreadingHTTPServer(("127.0.0.1", 0), Model)
        worker = threading.Thread(target=backend.serve_forever)
        worker.start()
        try:
            with patch.dict(os.environ, {"LOCALSTAGE_BACKEND": "model", "MODEL_BASE_URL": f"http://127.0.0.1:{backend.server_port}/v1"}):
                with self.request({"messages": [{"role": "user", "content": "hello"}]}) as response:
                    self.assertEqual(json.load(response)["text"], "Model reply")
            self.assertEqual(captured["path"], "/v1/chat/completions")
            self.assertEqual(captured["body"]["messages"][0]["role"], "system")
            self.assertEqual(captured["body"]["max_tokens"], 128)
        finally:
            backend.shutdown()
            backend.server_close()
            worker.join()


if __name__ == "__main__":
    unittest.main()
