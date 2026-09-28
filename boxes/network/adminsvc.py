# Internal admin service, only on the internal segment.
from flask import Flask, request
app = Flask(__name__)
FLAG = 'LEARN{network_lab_flag}'
@app.route('/')
def h(): return 'INTERNAL ADMIN\n'
@app.route('/flag')
def f():
    t = request.args.get('token','')
    if t == 'lab-admin-7788': return FLAG
    return 'token required\n', 403
app.run('0.0.0.0', 8080)
