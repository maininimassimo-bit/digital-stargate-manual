"""Explicit one-shot delivery of a locally reviewed refinement; no native launch."""
import argparse
import base64
import os
import re
from pathlib import Path

from .broker import decode, encode, require, opaque
from .transport import Transport
from .quality import inspect_pixels
from .worker import xisf_header, digest as file_digest


def prepare_payload(bundle):
    fields={'jobId','revisionId','parentReviewSha256','label','processingDate','original','preview','workflow','correlations','nonLinearConfirmed'}
    require(isinstance(bundle,dict) and set(bundle) == fields,'BUNDLE_FIELDS')
    require(opaque(bundle['revisionId']),'REVISION_ID')
    require(isinstance(bundle['jobId'],str) and re.fullmatch(r'PIAI_[a-f0-9]{32}',bundle['jobId']), 'JOB_ID_INVALID')
    require(isinstance(bundle['parentReviewSha256'],str) and re.fullmatch(r'[a-f0-9]{64}',bundle['parentReviewSha256']), 'PARENT_DIGEST_INVALID')
    require(bundle['nonLinearConfirmed'] is True,'NONLINEAR_DECLARATION_REQUIRED')
    original=Path(bundle['original']).resolve(strict=True)
    require(original.is_file() and original.suffix.lower() == '.xisf','XISF_SOURCE_REQUIRED')
    header=xisf_header(original)
    require(header['channels'] == 3 and header['sampleFormat'] == 'Float32','RGB_FLOAT32_REQUIRED')
    inspect_pixels(original)
    value={k:bundle[k] for k in ('parentReviewSha256','label','processingDate')}
    value['original']={'sha256':file_digest(original),'byteSize':original.stat().st_size,
                       'width':header['width'],'height':header['height'],'nonLinear':True}
    for role,maximum in [('preview',4*1024*1024),('workflow',2*1024*1024),('correlations',256*1024)]:
        path=Path(bundle[role]).resolve(strict=True)
        require(path.is_file() and 0 < path.stat().st_size <= maximum,'RESULT_SIZE')
        value[role+'Base64']=base64.b64encode(path.read_bytes()).decode()
    return value


def main():
    parser=argparse.ArgumentParser(description='Deliver an explicit private incremental refinement; no acceptance or publication.')
    parser.add_argument('--config',required=True)
    parser.add_argument('--bundle',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    require(Path(args.config).stat().st_size <= 65536 and Path(args.bundle).stat().st_size <= 65536,'CONFIG_SIZE')
    config=decode(Path(args.config).read_bytes())
    require(set(config) == {'serviceOrigin','workerId','workerRoot','registry'},'CONFIG_FIELDS')
    bundle=decode(Path(args.bundle).read_bytes())
    value=prepare_payload(bundle)
    transport=Transport(config['serviceOrigin'],os.environ['DSG_PIAI_WORKER_TOKEN'])
    response=transport.post(f"/v1/worker/science/{bundle['jobId']}/revisions/{bundle['revisionId']}/result",value)
    require(response.get('jobId') == bundle['jobId'] and response.get('revisionId') == bundle['revisionId'] and
            response.get('publication') == 'NONE','DELIVERY_RESPONSE_BINDING')
    raw=encode(response)
    output=Path(args.output)
    if output.exists():require(output.read_bytes() == raw,'LOCAL_RECEIPT_CONFLICT')
    else:
        with output.open('xb') as stream:stream.write(raw)
    print(encode(response).decode())


if __name__ == '__main__':main()
