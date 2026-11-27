"""File custody and message binding for the original ImageAnalysis trial parent."""
from contextlib import ExitStack
import hashlib
import json
import math
import os
from pathlib import Path
import re

from tools.scientific_transients.f06_staging_directories import hold_directory
from tools.scientific_transients.local_registry import safe_path
from tools.scientific_transients.native_read_locks import NativeReadLocks

_IDS=('compact-shuffled','compact-zones','tailed-shuffled','compact-wide-psf')
_METRICS={'fwhmPx','eccentricity','noise','stars','psfSignalWeight','psfSnr','snr','median','measurementSigma','mStar'}
_SOURCES={'runtime-config.json','entry.js','strict_passive_json.jsh','ImageAnalysis-controls.jsh','ImageAnalysis-adapter.jsh'}
_UUID4=r'[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}'


def need(value, reason):
    if not value:
        raise ValueError('IA_PARENT_'+reason)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _pairs(items):
    result={}
    for key,value in items:
        need(key not in result,'DUPLICATE_JSON_FIELD')
        result[key]=value
    return result


def _read(path):
    checked=safe_path(path)
    with checked.open('rb') as stream:
        raw=stream.read(65537)
    need(0<len(raw)<=65536,'RECORD_SIZE')
    return raw


def _decode(raw):
    result=json.loads(raw,object_pairs_hook=_pairs)
    need(type(result) is dict,'RECORD_TYPE')
    return result


def _pin(path, raw):
    return dict(path=path.as_posix(),sha256=digest(raw),byteLength=len(raw))


def _encode(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode('ascii')


class ImageAnalysisFiles:
    def __init__(self, root, *, operation, request_nonce, files, assert_live):
        self.root=safe_path(root)
        need(type(operation) is str and re.fullmatch('[a-f0-9]{32}',operation) is not None
             and self.root.name==operation and type(request_nonce) is str
             and re.fullmatch('[a-f0-9]{32}',request_nonce) is not None,'SCOPE')
        self.operation,self.nonce,self._live=operation,request_nonce,assert_live
        self._dirs=ExitStack()
        self._messages=[]
        self._static=None
        self._ack_attempted=False
        self._retention_attempted=False
        self._ack=self._result=None
        self._released=False
        expected={self.root/name for name in _SOURCES}
        expected|={self.root/'inputs'/(name+'.fits') for name in _IDS}
        need(type(files) is list and len(files)==len(expected)
             and {Path(rec['path']) for rec in files}==expected,'LOCK_SCOPE')
        try:
            for path in (self.root.parent,self.root,self.root/'inputs'):
                safe_path(path)
                self._dirs.enter_context(hold_directory(path))
            self._static=NativeReadLocks(files,guard=self._guard)
            self._files={Path(row['path']).name:dict(row) for row in files}
            cfg=_decode(_read(self.root/'runtime-config.json'))
            plan=cfg.get('plan')
            need(type(plan) is dict and cfg.get('protocol')=='BKL046_IMAGEANALYSIS_PJSR_CONFIG_V1'
                 and cfg.get('operationRef')==self.operation and cfg.get('requestNonce')==self.nonce
                 and plan.get('operationRef')==self.operation
                 and plan.get('inputRoot')==(self.root/'inputs').as_posix(),'CONFIG_BINDING')
            inputs=[]
            for name in _IDS:
                row=self._files[name+'.fits']
                need(row['byteLength']==77760,'INPUT_LENGTH')
                inputs.append(dict(row,id=name))
            need(plan.get('inputs')==inputs,'CONFIG_INPUT_PINS')
        except BaseException:
            if self._static is not None:
                self._static.release()
            self._dirs.close()
            raise

    def _guard(self):
        need(not self._released and self._live() is True,'SCOPE_NOT_LIVE')

    def _hold(self,path,raw):
        self._messages.append(NativeReadLocks([_pin(path,raw)],guard=self._guard))

    def acknowledge(self, reservation_check):
        need(not self._ack_attempted,'ACK_REPLAY')
        self._ack_attempted=True
        self._static.verify()
        reservation=reservation_check(self.operation)
        need(type(reservation) is str and re.fullmatch(_UUID4,reservation) is not None,'RESERVATION')
        request=self.root/'start-request.json'
        raw=_read(request)
        expected=dict(protocol='BKL046_IMAGEANALYSIS_START_REQUEST_V1', operationRef=self.operation,
            requestNonce=self.nonce, configSha256=self._files['runtime-config.json']['sha256'],
            entrySha256=self._files['entry.js']['sha256'])
        need(_decode(raw)==expected,'REQUEST_BINDING')
        self._hold(request,raw)
        self._static.verify()
        need(reservation_check(self.operation)==reservation,'RESERVATION_CHANGED')
        message=_encode(dict(protocol='BKL046_IMAGEANALYSIS_START_ACK_V1',operationRef=self.operation,
            requestNonce=self.nonce,requestSha256=digest(raw),reservation=reservation,decision='ADMITTED'))
        temporary=self.root/'start-ack.pending'
        output=self.root/'start-ack.json'
        with temporary.open('xb') as stream:
            need(stream.write(message)==len(message),'ACK_SHORT_WRITE')
            stream.flush()
            os.fsync(stream.fileno())
        self._guard()
        # Windows rename fails if a final file already exists.
        os.rename(temporary,output)
        self._hold(output,message)
        need(reservation_check(self.operation)==reservation,'RESERVATION_CHANGED')
        self._ack=(reservation,digest(message))
        return self._ack[1]

    def retain(self, reservation_check):
        need(self._ack is not None and not self._retention_attempted,'RETENTION_FENCED')
        self._retention_attempted=True
        self._static.verify()
        reservation,ack_sha=self._ack
        need(reservation_check(self.operation)==reservation,'RESERVATION_CHANGED')
        receipt_path=self.root/'return.json'
        result_path=self.root/'measurements.json'
        receipt_raw,result_raw=_read(receipt_path),_read(result_path)
        receipt=_decode(receipt_raw)
        expected=dict(protocol='BKL046_IMAGEANALYSIS_RETURN_V1',operationRef=self.operation,
            requestNonce=self.nonce,reservation=reservation,entrySha256=self._files['entry.js']['sha256'],
            configSha256=self._files['runtime-config.json']['sha256'],startAckSha256=ack_sha,
            resultSha256=digest(result_raw),producerReturned=True,scientificAcceptance=False)
        need(receipt==expected and receipt['producerReturned'] is True
             and receipt['scientificAcceptance'] is False,'RETURN_BINDING')
        self._verify_result(_decode(result_raw))
        self._hold(result_path,result_raw)
        self._hold(receipt_path,receipt_raw)
        for lock in self._messages:
            lock.verify()
        need(reservation_check(self.operation)==reservation,'RESERVATION_CHANGED')
        self._result=(digest(result_raw),digest(receipt_raw))
        return self._result

    def _verify_result(self,result):
        need(set(result)=={'protocol','operationRef','version','cache','extendedMeasurements','forward',
                          'reverse','deltas','scientificAcceptance'} and
             result['protocol']=='BKL046_IMAGEANALYSIS_CONTROL_RESULT_V1' and result['operationRef']==self.operation
             and result['version']=='1.9.6 build 1719' and result['cache'] is False
             and result['extendedMeasurements'] is False and result['scientificAcceptance'] is False,'RESULT_SCHEMA')
        runs=[]
        for key,order in [('forward',_IDS),('reverse',_IDS[::-1])]:
            run=result[key]
            need(type(run) is dict and set(run)=={'inputOrder','records'} and run['inputOrder']==list(order)
                 and type(run['records']) is list and len(run['records'])==len(_IDS),'RESULT_ORDER')
            for row,name in zip(run['records'],_IDS):
                need(type(row) is dict and set(row)=={'id','values'} and row['id']==name
                     and type(row['values']) is dict and set(row['values'])==_METRICS
                     and all(type(v) in (int,float) and math.isfinite(v) for v in row['values'].values()),
                     'RESULT_METRICS')
            runs.append(run['records'])
        need(type(result['deltas']) is list and len(result['deltas'])==len(_IDS),'DELTA_SCHEMA')
        for i,(row,name) in enumerate(zip(result['deltas'],_IDS)):
            need(type(row) is dict and set(row)=={'id','byMetric'} and row['id']==name
                 and type(row['byMetric']) is dict and set(row['byMetric'])==_METRICS,'DELTA_SCHEMA')
            for key, value in row['byMetric'].items():
                actual=runs[1][i]['values'][key]-runs[0][i]['values'][key]
                need(type(value) in (int,float) and math.isfinite(value) and value==actual,'DELTA_MISMATCH')

    def release_after_proven_exit(self, prove_original_exit):
        self._guard()
        need(self._result is not None and prove_original_exit() is True,'ORIGINAL_EXIT_NOT_PROVEN')
        self._static.verify()
        for lock in self._messages:
            lock.verify()
        need(prove_original_exit() is True,'ORIGINAL_EXIT_NOT_PROVEN')
        for lock in reversed(self._messages):
            lock.release()
        self._static.release()
        self._dirs.close()
        self._released=True
