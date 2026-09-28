"""A tiny AD/Kerberos simulator for training attack paths.

No real domain controller: this presents the enumeration and roasting workflow
as documented output so the learner walks the reasoning without needing a
Windows host on a Raspberry Pi.
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

USERS = [
  {"sAMAccountName":"svc_sql","spn":["MSSQLSvc/db01.woodland.local:1433"],"adminCount":0,"pwdLastSet":"2019-04-02","desc":"SQL service account"},
  {"sAMAccountName":"svc_backup","spn":["HOST/backup01.woodland.local"],"adminCount":0,"pwdLastSet":"2020-01-15","desc":"Backup service"},
  {"sAMAccountName":"svc_iis","spn":["HTTP/webserver.woodland.local"],"adminCount":0,"pwdLastSet":"2021-06-30","desc":"IIS app pool"},
  {"sAMAccountName":"a.smith","spn":[],"adminCount":0,"pwdLastSet":"2023-11-01","desc":"Helpdesk"},
  {"sAMAccountName":"d.jones","spn":[],"adminCount":1,"pwdLastSet":"2023-12-04","desc":"Domain Admin"},
]

# The crackable material. In a real lab these are real ticket blobs.
ROAST = {
  "svc_sql":    {"hashcat_mode":13100,"krb5tgs":"$krb5tgs$23$*svc_sql$WOODLAND.LOCAL$MSSQLSvc/db01*$<blob>","weak_password":"Summer2019!"},
  "svc_backup": {"hashcat_mode":13100,"krb5tgs":"$krb5tgs$23$*svc_backup$WOODLAND.LOCAL$HOST/backup01*$<blob>","weak_password":"Backup2020"},
  "svc_iis":    {"hashcat_mode":13100,"krb5tgs":"$krb5tgs$23$*svc_iis$WOODLAND.LOCAL$HTTP/webserver*$<blob>","weak_password":"IIS@2021"},
}

@app.route('/')
def home():
    return "WOODLAND.LOCAL - simulated directory service\nEndpoints: /enum/users /enum/spns /roast/<user> /acl /flag\n"

@app.route('/enum/users')
def users():
    return jsonify(USERS)

@app.route('/enum/spns')
def spns():
    return jsonify([u for u in USERS if u['spn']])

@app.route('/roast/<name>')
def roast(name):
    r = ROAST.get(name)
    if not r: return jsonify({"error":"no roastable account"}), 404
    return jsonify({"account":name, "type":"Kerberoastable", **r,
                    "note":"Request requires no special privileges. Crack offline."})

@app.route('/acl')
def acl():
    return jsonify({
      "svc_backup": {"localAdminOn":["backup01.woodland.local"], "sessions": ["d.jones"]},
      "backup01.woodland.local": {"unconstrainedDelegation": True},
      "a.smith": {"GenericWrite": ["svc_iis"], "note":"Can set an SPN on svc_iis"},
      "db01.woodland.local": {"MSSQLSvc": "svc_sql", "localAdminOn": ["db01"], "sessions": []},
      "d.jones": {"memberOf": ["Domain Admins", "Enterprise Admins"]},
    })

@app.route('/flag')
def flag():
    return jsonify({"flag": "LEARN{ad_path_traversed}"})

app.run('0.0.0.0', 88 if False else 8080)
