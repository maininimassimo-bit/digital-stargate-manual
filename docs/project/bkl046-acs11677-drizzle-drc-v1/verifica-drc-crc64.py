from argparse import ArgumentParser
from base64 import b64encode
from hashlib import md5, sha256
import json
from pathlib import Path
from urllib.request import Request,urlopen

url='https://stpubdata.s3.amazonaws.com/hst/public/jb6v/jb6v01010/jb6v01010_drc.fits?versionId=eyRFQuBCB6xUKZKiurmXjNyL3XNhLaOG'
pin={'content-length':'245940480','x-amz-checksum-crc64nvme':'99QkyGHMZ9A=','x-amz-checksum-type':'FULL_OBJECT',
     'x-amz-version-id':'eyRFQuBCB6xUKZKiurmXjNyL3XNhLaOG','etag':'"e6f860cb296d67cd50f8cf517bca145e"'}
prefix='156866aaa417b20cda5263a8a2806aba6d784e0222a71e538c9b94c67ab76c72'
poly_reflected=0x9A6C9329AC4BC9B5
word_mask=(1<<64)-1

def require(ok,message):
    if not ok:raise ValueError(message)

def build_table():
    result=[]
    for i in range(256):
        n=i
        for bit in range(8):
            n=(n>>1)^(poly_reflected if n&1 else 0)
        result.append(n)
    return tuple(result)

table=build_table()

def update(state,data):
    for b in data:
        state=table[(state^b)&255]^(state>>8)
    return state

def main():
    parser=ArgumentParser()
    parser.add_argument('file',type=Path)
    parser.add_argument('receipt',type=Path)
    args=parser.parse_args()
    require((update(word_mask,b'123456789')^word_mask)==0xAE8B14860A799888,'CRC64/NVME check vector mismatch')
    with urlopen(Request(url,method='HEAD',headers={'x-amz-checksum-mode':'ENABLED'}),timeout=16) as response:
        observed={key:response.headers.get(key) for key in pin}
        require(response.status==200 and observed==pin,'Registry metadata changed')
    require(args.file.stat().st_size==int(pin['content-length']),'File has unexpected length')
    a,b=sha256(),md5(usedforsecurity=False)
    state=word_mask
    with args.file.open('rb') as payload:
        require(sha256(payload.read(57600)).hexdigest()==prefix,'Official MAST FITS prefix differs')
        payload.seek(0)
        while data:=payload.read(1048576):
            a.update(data)
            b.update(data)
            state=update(state,data)
    crc=b64encode((state^word_mask).to_bytes(8,'big')).decode('ascii')
    require(crc==pin['x-amz-checksum-crc64nvme'],'Whole-object CRC64/NVME differs')
    require(b.hexdigest()==pin['etag'].strip('"'),'MD5 differs from the immutable object ETag')
    body=dict(scienceObjectVersionUrl=url,http=observed,sha256=a.hexdigest(),md5=b.hexdigest(),
              crc64nvme=crc,bytes=args.file.stat().st_size,mastPrefixSha256=prefix)
    with args.receipt.open('x',encoding='utf-8',newline='\n') as out:
        json.dump(body,out,indent=2,sort_keys=True)
        out.write('\n')
    print(json.dumps(body),flush=True)

if __name__=='__main__':
    main()
