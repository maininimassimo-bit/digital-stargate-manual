"""Read-only source records and exact crop lineage, without guessed history.

Native history describes recorded operations on this view, not all upstream
exposures. Crop equality proves a pixel relationship, never detector linearity.
Explicit paths/indices/hashes come from local source selection, never the model.
"""
import hashlib
from pathlib import Path
import re
import struct
import xml.etree.ElementTree as ET

from .broker import require
from .image_analysis import fingerprint

VERSION = 'DSG_PIAI_SOURCE_PROVENANCE_V2'
UI_PARAMETERS = {'showImages', 'noGUIMessages', 'closePreviousImages'}
OUTPUT_FIELDS = {'imageData','integratedPixels','integrationImageId','numberOfChannels',
    'outputPixels','outputRangeHigh','outputRangeLow','totalData','totalRejectedHighB',
    'totalRejectedHighG','totalRejectedHighRK','totalRejectedLowB','totalRejectedLowG',
    'totalRejectedLowRK','weightImageId'}

def _hash(value):
    require(isinstance(value,str) and re.fullmatch('[a-f0-9]{64}',value),'SOURCE_PROVENANCE_HASH')

def _xml(raw,code):
    # XISF headers and XPSM are UTF-8. Check decoded text before ElementTree
    # can autodetect another encoding or resolve an internal entity.
    try:
        text=raw.decode('utf-8-sig') if isinstance(raw,bytes) else raw
    except UnicodeDecodeError:
        require(False,code)
    require('\x00' not in text and '<!DOCTYPE' not in text and '<!ENTITY' not in text,code)
    declaration=re.match(r'\s*<\?xml\s+[^?]*encoding=[\"\x27]([^\"\x27]+)',text)
    require(declaration is None or declaration.group(1).lower()=='utf-8',code)
    return ET.fromstring(text)

def _image(path,index):
    with path.open('rb') as stream:
        require(stream.read(8)==b'XISF0100','SOURCE_PROVENANCE_SIGNATURE')
        size=stream.read(8);require(len(size)==8,'SOURCE_PROVENANCE_HEADER')
        length,reserved=struct.unpack('<II',size)
        # Align with the source-inventory limit, without raising the separate
        # 1 MiB limit used by the active V1 pixel diagnostics.
        require(0<length<=4*1024*1024 and reserved==0,'SOURCE_PROVENANCE_HEADER_LIMIT')
        raw=stream.read(length)
    require(len(raw)==length,'SOURCE_PROVENANCE_XML')
    elements=[e for e in _xml(raw,'SOURCE_PROVENANCE_XML') if e.tag.split('}')[-1]=='Image']
    require(1<=len(elements)<=16 and type(index) is int and 0<=index<len(elements),'SOURCE_PROVENANCE_IMAGE_INDEX')
    element=elements[index]
    require(element.get('id') not in {'rejection_low','rejection_high','slope_map','weight_map','crop_mask','drizzle_weights'},
            'SOURCE_PROVENANCE_AUXILIARY_IMAGE')
    geometry=element.get('geometry','').split(':')
    require(len(geometry)==3 and all(re.fullmatch('[0-9]+',v) for v in geometry),'SOURCE_PROVENANCE_GEOMETRY')
    metadata=dict(zip(('width','height','channels'),map(int,geometry)),
                  sampleFormat=element.get('sampleFormat'),colorSpace=element.get('colorSpace'))
    require(0<metadata['width']<=12000 and 0<metadata['height']<=12000 and
            metadata['channels'] in (1,3) and metadata['sampleFormat']=='Float32' and
            metadata['colorSpace']==('Gray' if metadata['channels']==1 else 'RGB'),'SOURCE_PROVENANCE_FORMAT')
    require(not element.get('compression') and element.get('pixelStorage','planar')=='planar' and
            element.get('byteOrder','little')=='little','SOURCE_PROVENANCE_NATIVE_LAYOUT')
    location=element.get('location','').split(':')
    require(len(location)==3 and location[0]=='attachment' and all(re.fullmatch('[0-9]+',v) for v in location[1:]),
            'SOURCE_PROVENANCE_ATTACHMENT')
    offset,size=map(int,location[1:])
    require(offset>=16+length and size==metadata['width']*metadata['height']*metadata['channels']*4 and
            offset+size<=path.stat().st_size,'SOURCE_PROVENANCE_ATTACHMENT_BOUNDS')
    return metadata,element,offset

def _property(element,name):
    rows=[e for e in element if e.tag.split('}')[-1]=='Property' and e.get('id')==name]
    require(len(rows)==1 and rows[0].get('type')=='String' and not list(rows[0]),'SOURCE_PROVENANCE_PROPERTY')
    value=rows[0].text or ''
    require(0<len(value.encode())<=1024*1024,'SOURCE_PROVENANCE_PROPERTY_LIMIT')
    return value

def _history(element):
    raw=_property(element,'PixInsight:ProcessingHistory')
    root=_xml(raw,'SOURCE_HISTORY_XML')
    require(root.tag=='ProcessingHistory' and root.get('version')=='1.0','SOURCE_HISTORY_VERSION')
    instances=list(root)
    require(1<=len(instances)<=256 and all(e.tag=='instance' and
            re.fullmatch('[A-Za-z][A-Za-z0-9_]{0,79}',e.get('class','')) for e in instances),'SOURCE_HISTORY_INSTANCES')
    return raw,instances

def inspect(path,*,expected_sha256,image_index):
    path=Path(path);_hash(expected_sha256)
    require(fingerprint(path)==expected_sha256,'SOURCE_PROVENANCE_CHANGED')
    metadata,element,_=_image(path,image_index)
    raw,instances=_history(element)
    require(fingerprint(path)==expected_sha256,'SOURCE_PROVENANCE_CHANGED')
    return {'version':VERSION,'sourceSha256':expected_sha256,'imageIndex':image_index,
        'geometry':metadata,'historySha256':hashlib.sha256(raw.encode()).hexdigest(),
        'recordedProcesses':[e.get('class') for e in instances],
        'historyCoverage':'RECORDED_VIEW_OPERATIONS_ONLY','upstreamHistory':'NOT_ESTABLISHED',
        'linearity':'NOT_ESTABLISHED','registration':'NOT_ESTABLISHED','acceptance':'NOT_ESTABLISHED'}

def verify_crop(child,parent,*,child_sha256,parent_sha256,child_index,parent_index):
    """All channel bytes must match the rectangle in the independently hashed parent."""
    child,parent=Path(child),Path(parent)
    for value in (child_sha256,parent_sha256):_hash(value)
    require(fingerprint(child)==child_sha256 and fingerprint(parent)==parent_sha256,'SOURCE_PROVENANCE_CHANGED')
    cm,ce,co=_image(child,child_index);pm,pe,po=_image(parent,parent_index)
    rows=[e for e in ce if e.tag.split('}')[-1]=='FITSKeyword' and e.get('name')=='WBPPCROP']
    require(len(rows)==1,'SOURCE_CROP_RECORD_REQUIRED')
    match=re.fullmatch(r"'\(([0-9]{1,5}),([0-9]{1,5})\)x\(([0-9]{1,5}),([0-9]{1,5})\)'",rows[0].get('value',''))
    require(match is not None,'SOURCE_CROP_RECORD')
    x0,y0,x1,y1=map(int,match.groups())
    require(cm['channels']==pm['channels'] and 0<=x0<x1<=pm['width'] and 0<=y0<y1<=pm['height'] and
            x1-x0==cm['width'] and y1-y0==cm['height'],'SOURCE_CROP_GEOMETRY')
    with child.open('rb') as cs,parent.open('rb') as ps:
        for channel in range(cm['channels']):
            for y in range(cm['height']):
                cs.seek(co+4*(channel*cm['width']*cm['height']+y*cm['width']))
                ps.seek(po+4*(channel*pm['width']*pm['height']+(y+y0)*pm['width']+x0))
                a,b=cs.read(4*cm['width']),ps.read(4*cm['width'])
                require(len(a)==4*cm['width'] and a==b,'SOURCE_CROP_PIXELS_DIFFER')
    ch,_=_history(ce);ph,_=_history(pe)
    require(ch==ph,'SOURCE_CROP_HISTORY_CHANGED')
    require(fingerprint(child)==child_sha256 and fingerprint(parent)==parent_sha256,'SOURCE_PROVENANCE_CHANGED')
    return {'version':VERSION,'childSha256':child_sha256,'parentSha256':parent_sha256,
        'childImageIndex':child_index,'parentImageIndex':parent_index,'crop':[x0,y0,x1,y1],
        'relationship':'PIXELS_BIT_IDENTICAL_RECTANGULAR_SUBSET','historyPreserved':True,
        'linearity':'NOT_ESTABLISHED','registration':'NOT_ESTABLISHED','acceptance':'NOT_ESTABLISHED'}

def _canonical(element):
    return (element.tag.split('}')[-1],tuple(sorted(element.attrib.items())),
            (element.text or '').strip(),tuple(_canonical(e) for e in element))

def match_drizzle_container(path,container,*,source_sha256,container_sha256,image_index):
    """Record exact input/parameter correspondence; UI differences are explicit."""
    path,container=Path(path),Path(container)
    for value in (source_sha256,container_sha256):_hash(value)
    require(fingerprint(path)==source_sha256 and fingerprint(container)==container_sha256,'SOURCE_PROVENANCE_CHANGED')
    _,element,_=_image(path,image_index);_,instances=_history(element)
    require(len(instances)==1 and instances[0].get('class')=='DrizzleIntegration','SOURCE_DRIZZLE_HISTORY_REQUIRED')
    require(container.stat().st_size<=16*1024*1024,'SOURCE_CONTAINER_LIMIT')
    raw=container.read_bytes()
    tree=_xml(raw,'SOURCE_CONTAINER_XML')
    require(tree.tag=='{http://www.pixinsight.com/xpsm}xpsm','SOURCE_CONTAINER_ROOT')
    candidates=[e for e in tree.iter() if e.get('class')=='DrizzleIntegration']
    require(1<=len(candidates)<=16,'SOURCE_CONTAINER_COUNT')
    def fields(e):
        rows=[c for c in e if c.tag.split('}')[-1] in ('parameter','table')]
        require(len({r.get('id') for r in rows})==len(rows),'SOURCE_DUPLICATE_PARAMETER')
        return {r.get('id'):_canonical(r) for r in rows}
    history=fields(instances[0]); matches=[]
    for index,candidate in enumerate(candidates):
        saved=fields(candidate)
        # Both sides must expose the same pixel-affecting fields. Unknown fields
        # never silently disappear from the comparison.
        hs=set(history)-UI_PARAMETERS-OUTPUT_FIELDS; ss=set(saved)-UI_PARAMETERS
        if hs==ss and 'inputData' in hs and all(history[k]==saved[k] for k in hs):
            matches.append({'containerIndex':index,'pixelFieldCount':len(hs),
                'uiDifferences':sorted(k for k in UI_PARAMETERS if history.get(k)!=saved.get(k))})
    require(len(matches)==1,'SOURCE_CONTAINER_MATCH_REQUIRED')
    require(fingerprint(path)==source_sha256 and fingerprint(container)==container_sha256,'SOURCE_PROVENANCE_CHANGED')
    return {'version':VERSION,'sourceSha256':source_sha256,'containerSha256':container_sha256,
        'imageIndex':image_index,**matches[0],'correspondence':'RECORDED_DRIZZLE_INPUTS_AND_PARAMETERS',
        'executionReceipt':'NOT_ESTABLISHED','upstreamHistory':'NOT_ESTABLISHED',
        'linearity':'NOT_ESTABLISHED','registration':'NOT_ESTABLISHED','acceptance':'NOT_ESTABLISHED'}
