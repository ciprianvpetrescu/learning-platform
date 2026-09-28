#!/usr/bin/env python3
"""Generate a forensic disk image with recoverable deleted content.

The flag sits inside a password-protected zip in the recovered directory.
The password is planted in an allocated document block inside the image,
so the solve path is: examine image -> find password -> open archive -> flag.
"""
import os, sys, io, zipfile, struct, random, zlib

flag = sys.argv[1] if len(sys.argv) > 1 else "LEARN{dev_flag}"
os.makedirs('/home/analyst', exist_ok=True)
img = '/home/analyst/case.dd'
ZIP_PW = b'hunter2forensics'

def jpeg_like(tag):
    head = bytes([0xFF,0xD8,0xFF,0xE0,0x00,0x10]) + b'JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
    body = b'\xff\xdb' + bytes([0x00,0x43,0x00]) + bytes(range(1,65))
    comment = b'\xff\xfe' + struct.pack('>H', len(tag)+2) + tag
    return head + body + comment + b'\xff\xd9'

def png_like(tag):
    sig = bytes([0x89,0x50,0x4E,0x47,0x0D,0x0A,0x1A,0x0A])
    raw = struct.pack('>IIBBBBB', 64, 64, 8, 2, 0, 0, 0)
    ihdr = struct.pack('>I', len(raw)) + b'IHDR' + raw + struct.pack('>I', zlib.crc32(b'IHDR'+raw) & 0xFFFFFFFF)
    txt = b'tEXtComment\x00' + tag
    txtc = struct.pack('>I', len(txt)-4) + txt + struct.pack('>I', zlib.crc32(txt)&0xFFFFFFFF)
    idat = zlib.compress(b'\x00'*64*64*3)
    idatc = struct.pack('>I', len(idat)) + b'IDAT' + idat + struct.pack('>I', zlib.crc32(b'IDAT'+idat)&0xFFFFFFFF)
    iend = struct.pack('>I',0) + b'IEND' + struct.pack('>I', zlib.crc32(b'IEND')&0xFFFFFFFF)
    return sig + ihdr + txtc + idatc + iend

# password-protected archive. zipfile cannot write legacy encryption, so we
# shell out to the zip command when available, else write a plain zip and note it.
import subprocess, tempfile, shutil
os.makedirs('/home/analyst/recovered', exist_ok=True)
tmpd = tempfile.mkdtemp()
open(os.path.join(tmpd,'flag.txt'),'w').write(flag + '\n')
open(os.path.join(tmpd,'notes.txt'),'w').write('Acquisition meeting moved to Thursday.\n')
zpath = '/home/analyst/recovered/evidence.zip'
encrypted = False
if shutil.which('zip'):
    r = subprocess.run(['zip','-j','-P',ZIP_PW.decode(), zpath, os.path.join(tmpd,'flag.txt'), os.path.join(tmpd,'notes.txt')],
                       capture_output=True)
    encrypted = r.returncode == 0
if not encrypted:
    with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('flag.txt', flag + '\n')
        z.writestr('notes.txt', 'Acquisition meeting moved to Thursday.\n')

blocks = [
  ('ALLOC', jpeg_like(b'EXIF: DateTimeOriginal=2024:03:11 02:14:07; Make=Canon; Model=EOS 5D')),
  ('ALLOC', png_like(b'Screenshot of the payroll spreadsheet, taken 02:31')),
  ('FREE',  jpeg_like(b'EXIF: DateTimeOriginal=2024:03:11 02:47:55; Software=Photoshop; Warning: timestamp altered')),
  ('FREE',  jpeg_like(b'EXIF: DateTimeOriginal=2024:03:09 23:58:01; Comment=original backup photo')),
  ('ALLOC', b'OPERATIONS NOTE\nArchive password is: ' + ZIP_PW + b'\nStored here for the ops team. Do not share.\n'),
  ('FREE',  b'Deleted document fragment: Q3 projection, revenue, headcount, salaries\n'),
  ('FREE',  png_like(b'EXIF: hidden thumbnail; contains a partial QR of the vault reference')),
]

print('[make_evidence] zip encrypted:', encrypted)
with open(img,'wb') as f:
    f.write(b'\x00' * 4096)
    for state, data in blocks:
        f.write(data)
        f.write(bytes([random.randrange(256) for _ in range(2048)]))
    f.write(b'\x00' * 65536)
print('[make_evidence] wrote', img, os.path.getsize(img), 'bytes')
