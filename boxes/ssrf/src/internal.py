# Internal admin service. Binds loopback only. Not reachable from outside.
from flask import Flask, request
import os
app = Flask(__name__)
TOKEN = "internal-admin-token-9f3a"

@app.route("/")
def home():
    return "INTERNAL ADMIN SERVICE\n"

@app.route("/admin/flag")
def flag():
    if request.remote_addr not in ("127.0.0.1", "::1", "localhost"):
        return "forbidden: internal only\n", 403
    try:
        return open("/var/www/flag.txt").read()
    except Exception as e:
        return str(e), 500

@app.route("/admin/token")
def token():
    return TOKEN + "\n"

app.run(host="127.0.0.1", port=8080)
