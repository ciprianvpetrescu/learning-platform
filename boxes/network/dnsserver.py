"""Lab DNS server. Answers A records and permits an unrestricted zone transfer.

Listens on UDP and TCP 53: AXFR is a TCP protocol, which is the detail that
trips people up in the lab.
"""
import socket, struct, threading

IPV4 = ['10.66.9.1','10.66.9.30','10.66.9.31','10.66.9.40','10.66.9.50','10.66.9.99']
NAMES = [b'router', b'fileserver', b'db', b'admin', b'vault', b'flag']
ZONE = list(zip(NAMES, IPV4))
TOKEN = b'lab-admin-7788'
FLAG = b'LEARN{network_lab_flag}'

def enc(name):
    out = b''
    for p in name.split(b'.'):
        out += bytes([len(p)]) + p
    return out + b'\x00'

def rr(name, rtype, rdata):
    return enc(name) + struct.pack('>HHIH', rtype, 1, 60, len(rdata)) + rdata

def build_axfr(tid, qname_raw):
    question = qname_raw + struct.pack('>HH', 252, 1)
    answers = b''
    n = 0
    for nm, ip in ZONE:
        full = nm + b'.lab.internal'
        if nm == b'flag':
            answers += rr(full, 16, bytes([len(FLAG)]) + FLAG); n += 1
            answers += rr(full, 16, bytes([len(TOKEN)]) + TOKEN); n += 1
        else:
            answers += rr(full, 1, socket.inet_aton(ip)); n += 1
    hdr = tid + struct.pack('>HHHHH', 0x8400, 1, n, 0, 0)
    return hdr + question + answers

def parse_qname(data, off):
    parts = []
    start = off
    while data[off]:
        l = data[off]; parts.append(data[off+1:off+1+l]); off += 1 + l
    return b'.'.join(parts).lower(), off + 1, data[start:off+1]

def handle_udp(data, addr, s):
    try:
        tid = data[:2]
        qname, off, raw = parse_qname(data, 12)
        qtype = struct.unpack('>H', data[off:off+2])[0]
        q = raw + struct.pack('>HH', qtype, 1)
        ans = b''
        full = qname
        for nm, ip in ZONE:
            if full == nm + b'.lab.internal' and qtype == 1:
                ans = b'\xc0\x0c' + struct.pack('>HHIH', 1, 1, 60, 4) + socket.inet_aton(ip)
        hdr = tid + struct.pack('>HHHHH', 0x8180, 1, 1 if ans else 0, 0, 0)
        s.sendto(hdr + q + ans, addr)
    except Exception:
        pass

def udp_loop():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 53))
    while True:
        try:
            d, a = s.recvfrom(1024)
            threading.Thread(target=handle_udp, args=(d, a, s), daemon=True).start()
        except Exception:
            pass

def handle_tcp(conn):
    try:
        ln = conn.recv(2)
        if len(ln) < 2: return
        n = struct.unpack('>H', ln)[0]
        data = b''
        while len(data) < n:
            c = conn.recv(n - len(data))
            if not c: break
            data += c
        tid = data[:2]
        qname, off, raw = parse_qname(data, 12)
        qtype = struct.unpack('>H', data[off:off+2])[0]
        if qtype == 252:
            resp = build_axfr(tid, raw)
        else:
            q = raw + struct.pack('>HH', qtype, 1)
            ans = b''
            for nm, ip in ZONE:
                if qname == nm + b'.lab.internal' and qtype == 1:
                    ans = b'\xc0\x0c' + struct.pack('>HHIH', 1, 1, 60, 4) + socket.inet_aton(ip)
            resp = tid + struct.pack('>HHHHH', 0x8180, 1, 1 if ans else 0, 0, 0) + q + ans
        conn.sendall(struct.pack('>H', len(resp)) + resp)
    except Exception:
        pass
    finally:
        conn.close()

def tcp_loop():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 53))
    s.listen(10)
    while True:
        try:
            c, _ = s.accept()
            threading.Thread(target=handle_tcp, args=(c,), daemon=True).start()
        except Exception:
            pass

threading.Thread(target=tcp_loop, daemon=True).start()
udp_loop()
