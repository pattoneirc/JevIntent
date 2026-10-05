# -*- coding: utf-8 -*-
"""mock_jev.py —— test_prekey.bsh 用的本机假 Jev 端点（127.0.0.1:8901）

只做一件事：任何 POST 都回一份带 emotion/intent 答案的 JSON，
让预判链路（prefetchStart → httpPost → prefetchTake）能在 PC 上完整跑通，不花真钱。

跑法：python mock_jev.py   （停掉：Ctrl-C；端口被占就改下面 PORT，同步改 test_prekey.bsh）
"""
import http.server
import json

PORT = 8901

BODY = json.dumps({
    "answers": {
        "emotion": {"type": "choice", "choice": "平静", "probabilities": {"平静": 0.9, "客套": 0.1}},
        "intent": {"type": "choice", "choice": "闲聊"},
        "urgency": {"type": "score", "score": 0.5},
        "reply_style": {"type": "choice", "choice": "正常"},
        "advice": {"type": "choice", "choice": "正常交流"},
    }
}, ensure_ascii=True).encode("ascii")


class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        self.rfile.read(n)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(BODY)))
        self.end_headers()
        self.wfile.write(BODY)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"mock Jev 端点已起：http://127.0.0.1:{PORT}/  （Ctrl-C 停）")
    http.server.HTTPServer(("127.0.0.1", PORT), H).serve_forever()
