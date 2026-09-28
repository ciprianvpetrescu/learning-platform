# URL preview service. Has a hand-written blocklist. Of course it does.
from flask import Flask, request, Response
import requests, re
app = Flask(__name__)

BLOCKED = ["127.0.0.1", "localhost", "169.254.169.254", "0.0.0.0", "::1", "metadata"]

def blocked(url):
    low = url.lower()
    return any(b in low for b in BLOCKED)

@app.route("/")
def home():
    return Response('''<!doctype html><html><head><title>Fetcher - URL Preview</title>
<style>body{font-family:system-ui;background:#0d1117;color:#c9d1d9;max-width:760px;margin:40px auto;padding:20px}
input{background:#161b22;border:1px solid #30363d;color:#c9d1d9;padding:9px;width:70%;box-sizing:border-box}
.btn{background:#238636;border:0;color:#fff;padding:10px 16px;cursor:pointer}pre{background:#161b22;padding:14px;border-radius:6px;border:1px solid #30363d;overflow:auto;white-space:pre-wrap}
code{background:#161b22;padding:2px 5px;border-radius:3px}</style></head><body>
<h1>Fetcher</h1><p>Paste a URL and we will fetch it for you and show the response.</p>
<form method="post"><input name="url" placeholder="http://example.com" value="http://example.com">
<button class="btn">Fetch</button></form>
<p><small>Internal addresses are blocked: <code>127.0.0.1</code>, <code>localhost</code>, <code>169.254.169.254</code></small></p>
</body></html>''', mimetype="text/html")

@app.route("/", methods=["POST"])
def do_fetch():
    url = request.form.get("url", "")
    if not url:
        return "no url", 400
    if blocked(url):
        return Response(f"<html><body style='font-family:system-ui;background:#0d1117;color:#f85149;padding:40px'><h2>Blocked</h2><p>URL contains a blocked string: {url}</p><a style='color:#58a6ff' href='/'>back</a></body></html>", mimetype="text/html")
    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        body = r.text[:8000]
    except Exception as e:
        body = f"Error: {e}"
    return Response(f'''<html><head><title>Fetcher</title><style>body{{font-family:system-ui;background:#0d1117;color:#c9d1d9;max-width:860px;margin:40px auto;padding:20px}}pre{{background:#161b22;padding:14px;border-radius:6px;border:1px solid #30363d;overflow:auto;white-space:pre-wrap}}a{{color:#58a6ff}}</style></head><body>
<h1>Fetched</h1><p><b>URL:</b> {url}</p><pre>{body}</pre><a href="/">back</a></body></html>''', mimetype="text/html")

app.run(host="0.0.0.0", port=80)
