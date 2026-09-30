"""F0-only fixed synthetic identity experiment, not an AP-013/archive schema.
All files are generated under TemporaryDirectory. No real-file input is accepted.
"""
import copy
import hashlib
import json
import tempfile
from pathlib import Path

sha = lambda b: hashlib.sha256(b).hexdigest()

def anchor(packet):
    return sha(json.dumps(packet, sort_keys=True, separators=(',', ':')).encode())

def key(ref):
    return (ref['kind'], ref['id'], ref['version'])

def check(packet, payloads, expected_anchor):
    # Anchor must come from an independent trusted record; accepting a caller's
    # freshly recomputed anchor would not authenticate anything.
    if anchor(packet) != expected_anchor:
        raise ValueError('PACKET_ANCHOR_MISMATCH')
    objects = {}
    for item in packet['objects']:
        identity = key(item)
        if identity in objects:
            raise ValueError('DUPLICATE_TYPED_VERSION')
        if identity not in payloads:
            raise ValueError('MISSING_PAYLOAD')
        data = payloads[identity]
        if len(data) != item['bytes'] or sha(data) != item['sha256']:
            raise ValueError('CONTENT_MISMATCH')
        objects[identity] = item
    binding = packet['binding']
    export_key, image_key = key(binding['export']), key(binding['output'])
    if export_key not in objects or image_key not in objects:
        raise ValueError('UNRESOLVED_BINDING')
    if export_key[0] != 'export' or image_key[0] != 'image':
        raise ValueError('WRONG_ENTITY_KIND')
    gallery = packet['galleryCandidate']
    if key(gallery['image']) != image_key or gallery['sha256'] != objects[image_key]['sha256']:
        raise ValueError('GALLERY_VERSION_MISMATCH')
    return {'identityCheck': 'MATCHED_SYNTHETIC_PACKET', 'bindingEvidence': binding['evidenceClass'],
            'workflowCompleteness': 'PARTIAL', 'actionAuthority': 'NONE', 'acceptanceAuthority': False}

def main():
    results = []
    scratch = (Path(__file__).resolve().parent / '.identity-scratch').resolve()
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='bkl049-synthetic-', dir=scratch) as directory:
        folder = Path(directory).resolve()
        if folder.parent != scratch:
            raise RuntimeError('Unexpected temporary directory boundary')
        (folder/'image.bin').write_bytes(b'SYNTHETIC IMAGE VERSION ONE; NOT SCIENTIFIC PIXELS')
        (folder/'export.txt').write_bytes(b'SYNTHETIC HISTORY ARTIFACT; NOT EXECUTABLE')
        image = {'kind':'image', 'id':'SYNTHETIC-SHARED', 'version':'v1'}
        export = {'kind':'export', 'id':'SYNTHETIC-SHARED', 'version':'v1'}
        payloads = {key(image):(folder/'image.bin').read_bytes(), key(export):(folder/'export.txt').read_bytes()}
        packet = {'objects': [{**ref,'bytes':len(payloads[key(ref)]),'sha256':sha(payloads[key(ref)])} for ref in (image,export)],
                  'binding': {'export':export,'output':image,'evidenceClass':'DECLARED'},
                  'galleryCandidate': {'image':image,'sha256':sha(payloads[key(image)])}}
        trusted = anchor(packet)
        def expect_rejection(code, candidate, data, expected=trusted):
            try:
                check(candidate,data,expected)
            except ValueError as exc:
                assert str(exc)==code, (str(exc),code)
                return
            raise AssertionError('Expected rejection: '+code)
        def probe(name,description,fn):
            fn(); results.append({'id':name,'outcome':'REPRODUCED','finding':description})
        def good():
            r=check(packet,payloads,trusted)
            assert r['workflowCompleteness']=='PARTIAL' and r['bindingEvidence']=='DECLARED'
            assert r['actionAuthority']=='NONE' and not r['acceptanceAuthority']
        probe('I01','Typed image/export IDs can share text without aliasing; successful identity check retains DECLARED/PARTIAL.',good)
        def modified_file():
            (folder/'image.bin').write_bytes(b'SYNTHETIC IMAGE VERSION TWO; NOT SCIENTIFIC PIXELS')
            changed=dict(payloads);changed[key(image)]=(folder/'image.bin').read_bytes()
            expect_rejection('CONTENT_MISMATCH',packet,changed)
        probe('I02','Same file name and ID with changed bytes fails the original digest.',modified_file)
        def missing():
            changed=dict(payloads);del changed[key(export)]
            expect_rejection('MISSING_PAYLOAD',packet,changed)
        probe('I03','A missing source artifact prevents a verified packet association.',missing)
        def duplicate():
            changed=copy.deepcopy(packet);changed['objects'].append(copy.deepcopy(changed['objects'][0]))
            expect_rejection('DUPLICATE_TYPED_VERSION',changed,payloads,anchor(changed))
        probe('I04','Duplicate typed IDs/versions are rejected rather than selecting the last record.',duplicate)
        def stale_gallery():
            # Replace the gallery reference without changing the binding reference.
            changed=copy.deepcopy(packet);changed['galleryCandidate']['image']={**image,'version':'v2'}
            expect_rejection('GALLERY_VERSION_MISMATCH',changed,payloads,anchor(changed))
        probe('I05','A gallery reference to another version is rejected.',stale_gallery)
        def missing_link():
            changed=copy.deepcopy(packet);changed['binding']['output']={**image,'id':'SYNTHETIC-OTHER'}
            expect_rejection('UNRESOLVED_BINDING',changed,payloads,anchor(changed))
        probe('I06','A source-to-output link cannot point to an absent typed asset.',missing_link)
        def wrong_kind():
            changed=copy.deepcopy(packet);changed['binding']['export']=copy.deepcopy(image)
            expect_rejection('WRONG_ENTITY_KIND',changed,payloads,anchor(changed))
        probe('I07','Image and source-export namespaces are not interchangeable.',wrong_kind)
        def reseal():
            changed=copy.deepcopy(packet);changed['objects'][0]['sha256']='0'*64
            expect_rejection('PACKET_ANCHOR_MISMATCH',changed,payloads)
        probe('I08','A changed manifest fails the separately retained packet anchor.',reseal)
        def renamed():
            (folder/'export.txt').rename(folder/'renamed.txt')
            moved=dict(payloads);moved[key(export)]=(folder/'renamed.txt').read_bytes()
            assert check(packet,moved,trusted)['identityCheck']=='MATCHED_SYNTHETIC_PACKET'
        probe('I09','Renaming a file with unchanged bytes and explicit identity does not break this identity check.',renamed)
        def replaced_trust():
            changed=copy.deepcopy(packet);data=dict(payloads)
            data[key(image)]=b'REPLACEMENT SYNTHETIC CONTENT'
            changed['objects'][0]['bytes']=len(data[key(image)])
            changed['objects'][0]['sha256']=sha(data[key(image)])
            changed['galleryCandidate']['sha256']=sha(data[key(image)])
            assert check(changed,data,anchor(changed))['identityCheck']=='MATCHED_SYNTHETIC_PACKET'
        probe('I10','Replacing payload, metadata AND accepted anchor yields a match: hashes alone do not authenticate origin.',replaced_trust)
    print(json.dumps({'experiment':'BKL049-F0-SYNTHETIC-IDENTITY-PACKET',
                      'scope':'Original research verifier on fixed synthetic files; not AP-013, signed provenance, live gallery integration or production validation',
                      'results':results},indent=2))

if __name__=='__main__':
    main()
