"""Bind retained candidate WCS/timing evidence to an exact lineage input.

Read-only header/byte inspection and descriptive residual arithmetic; no
catalog requests, solving, resampling, validated astrometry or clock model.
"""
import datetime
from decimal import Decimal
import math
from pathlib import Path
import re
import struct
import xml.etree.ElementTree as ET
from tools.pixinsight.local_pilot.broker import require
from tools.scientific_transients.local_registry import safe_path, fingerprint
from tools.scientific_transients.calibration_context import pinned_json
from tools.scientific_transients.input_lineage import inspect_lineage


def header(path):
    path=safe_path(path);before=fingerprint(path)
    with path.open('rb') as stream:
        prefix=stream.read(16)
        require(len(prefix)==16 and prefix[:8]==b'XISF0100','ASTROMETRY_XISF_SIGNATURE')
        size=struct.unpack('<I',prefix[8:12])[0]
        require(0<size<=16*1024*1024 and size+16<=before['bytes'],'ASTROMETRY_HEADER_SIZE')
        raw=stream.read(size)
    require(len(raw)==size and b'\x00' not in raw,'ASTROMETRY_HEADER_ENCODING')
    text=raw.decode('utf-8')
    require('<!DOCTYPE' not in text.upper() and '<!ENTITY' not in text.upper(),'ASTROMETRY_XML_DECLARATION')
    root=ET.fromstring(text);images=[e for e in root.iter() if e.tag.split('}')[-1]=='Image']
    require(len(images)==1,'ASTROMETRY_SINGLE_IMAGE')
    image=images[0];geometry=image.attrib['geometry'].split(':')
    require(len(geometry)==3 and all(x.isdecimal() and int(x)>0 for x in geometry),'ASTROMETRY_GEOMETRY')
    keywords={};properties=set()
    for e in image:
        tag=e.tag.split('}')[-1]
        if tag=='FITSKeyword':
            name=e.attrib['name']
            if name in {'DATE-OBS','DATE-AVG','EXPTIME','FILTER','DATE-END','TIMESYS'}:
                require(name not in keywords,'ASTROMETRY_DUPLICATE_KEYWORD')
                keywords[name]=e.attrib['value'].strip().strip("'").strip()
        elif tag=='Property':properties.add(e.attrib['id'])
    require(fingerprint(path)==before,'ASTROMETRY_HEADER_CHANGED')
    return {'sha256':before['sha256'],'geometry':[int(x) for x in geometry],
            'keywords':keywords,'properties':properties}


def timestamp_seconds(value):
    require(type(value) is str and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,12})?Z?',value),
            'ASTROMETRY_TIMESTAMP_FORMAT')
    date,time=value.removesuffix('Z').split('T');hour,minute,second=time.split(':')
    day=datetime.date.fromisoformat(date);s=Decimal(second)
    require(0<=int(hour)<24 and 0<=int(minute)<60 and 0<=s<60,'ASTROMETRY_TIMESTAMP_RANGE')
    return Decimal(day.toordinal()*86400+int(hour)*3600+int(minute)*60)+s


def timing(original,derived):
    a,b=original['keywords'],derived['keywords']
    require(all(k in a and k in b for k in ('DATE-OBS','DATE-AVG','EXPTIME','FILTER')),'ASTROMETRY_TIMING_MISSING')
    exposure=Decimal(a['EXPTIME'])
    require(exposure.is_finite() and exposure>0 and exposure==Decimal(b['EXPTIME'])
            and a['FILTER']==b['FILTER'],'ASTROMETRY_TIMING_IDENTITY')
    start=timestamp_seconds(a['DATE-OBS']);avg=timestamp_seconds(a['DATE-AVG'])
    return {'sourceDateObs':a['DATE-OBS'],'sourceDateAvg':a['DATE-AVG'],
        'derivedDateObs':b['DATE-OBS'],'derivedDateAvg':b['DATE-AVG'],
        'exposureSeconds':str(exposure),'averageMinusStartHalfExposureSeconds':str(avg-start-exposure/2),
        'derivedStartMinusSourceSeconds':str(timestamp_seconds(b['DATE-OBS'])-start),
        'averagePreserved':a['DATE-AVG']==b['DATE-AVG'],
        'timeScale':'HEADER_DECLARATION_NOT_CLOCK_ATTESTATION',
        'clockShutterUncertainty':None,
        'endTimeOrigin':('DERIVED_METADATA_NOT_IN_SOURCE' if
            ('DATE-END' in b and 'DATE-END' not in a) or
            ('Observation:Time:End' in derived['properties'] and 'Observation:Time:End' not in original['properties'])
            else 'NOT_ESTABLISHED_BY_THIS_IMPORT')}


def residuals(terminal,split,centroids):
    require(type(split['training']) is list and type(split['heldOut']) is list
        and 0<len(split['training'])<=3000 and 0<len(split['heldOut'])<=3000,'ASTROMETRY_PARTITION')
    train=[r['SourceID'] for r in split['training']];held=[r['SourceID'] for r in split['heldOut']]
    require(all(type(x) is str and x.isdecimal() for x in train+held)
        and len(set(train))==len(train) and len(set(held))==len(held) and not set(train)&set(held),
        'ASTROMETRY_PARTITION_OVERLAP')
    rows=terminal['holdout']
    require(type(rows) is list and len(rows)==len(held)
        and {r['sourceId'] for r in rows}==set(held),'ASTROMETRY_HELDOUT_COVERAGE')
    require(type(centroids) is list and len(centroids)<=100000,'ASTROMETRY_CENTROIDS')
    require(all(type(c[k]) in {int,float} and math.isfinite(c[k]) for c in centroids for k in ('x','y')),
            'ASTROMETRY_CENTROID_NUMBER')
    values=[];used=set();counts={'UNIQUE_DIAGNOSTIC_MATCH':0,'NO_MATCH':0,'OUTSIDE_OR_UNPROJECTABLE':0}
    for row in rows:
        status=row['status'];require(status in counts,'ASTROMETRY_MATCH_STATE');counts[status]+=1
        if status!='UNIQUE_DIAGNOSTIC_MATCH':continue
        p,m=row['predicted'],row['measured']
        require(type(p) is list and type(m) is list and len(p)==len(m)==2
            and all(type(n) in {int,float} and math.isfinite(n) for n in p+m),'ASTROMETRY_COORDINATE')
        # Recheck the retained caller's square +/-3 pixel search, not a radial cut.
        candidates=[i for i,c in enumerate(centroids) if abs(c['x']-p[0])<=3 and abs(c['y']-p[1])<=3]
        require(len(candidates)==1 and candidates[0] not in used
            and [centroids[candidates[0]]['x'],centroids[candidates[0]]['y']]==m,'ASTROMETRY_MATCH_CHANGED')
        used.add(candidates[0]);dx,dy=m[0]-p[0],m[1]-p[1]
        require(math.isclose(dx,row['dx'],abs_tol=1e-12) and math.isclose(dy,row['dy'],abs_tol=1e-12),
                'ASTROMETRY_RESIDUAL_CHANGED')
        values.append(dx*dx+dy*dy)
    require(values,'ASTROMETRY_NO_MATCHED_RESIDUALS')
    total=math.fsum(values)
    require(math.isfinite(total),'ASTROMETRY_RESIDUAL_OVERFLOW')
    return {'trainingReferences':len(train),'heldOutReferences':len(held),'matched':len(values),
        'unmatched':counts['NO_MATCH'],'outsideOrUnprojectable':counts['OUTSIDE_OR_UNPROJECTABLE'],
        'radialRMSPixel':math.sqrt(total/len(values)),'largestResidualPixel':math.sqrt(max(values)),
        'largestSquaredResidualShare':max(values)/total if total>0 else None,
        'searchGeometry':'SQUARE_PLUS_MINUS_3_PIXELS_DIAGNOSTIC_ONLY',
        'partition':'DISJOINT_RECHECKED','centroidReuse':0,
        'unmatchedOutsideRecheck':'RETAINED_STATES_NOT_REMATCHED',
        'scope':'DESCRIPTIVE_SCATTER_NOT_WCS_OR_PER_SOURCE_UNCERTAINTY',
        'fullCovariance':None,'independentScientificValidation':False}


def retained(directory,receipt_sha,flag,status):
    directory=safe_path(directory);receipt=pinned_json(directory/'receipt.json',receipt_sha)
    require(receipt[flag] is True,'ASTROMETRY_RETAINED_PARENTS')
    products=receipt['products'];require(type(products) is dict and 1<=len(products)<=128,'ASTROMETRY_PRODUCTS')
    for name,sha in products.items():
        require(type(name) is str and Path(name).name==name and name not in {'.','..'},'ASTROMETRY_PRODUCT_PATH')
        require(fingerprint(directory/name)['sha256']==sha,'ASTROMETRY_PRODUCT_CHANGED')
    terminal=pinned_json(directory/'terminal.json',products['terminal.json'])
    require(terminal==receipt['terminal'] and terminal['status']==status
        and terminal['scienceValidation']=='NOT_VALIDATED' and type(terminal['pixelDifference']) in {int,float}
        and terminal['pixelDifference']==0,'ASTROMETRY_TERMINAL')
    return receipt,terminal,pinned_json(directory/'manifest.json',products['manifest.json'])


def coordinate_copy_checks(terminal,geometry):
    """Check retained native copy probes, not absolute astrometric accuracy.

    PJSR imageToCelestial returns a Point. Older callers that indexed it like
    an array compared undefined values and serialized empty objects. A success
    status and zero pixel difference do not repair that missing evidence.
    """
    rows=terminal.get('coordinateChecks')
    width,height,_=geometry
    probes=[[0.5,0.5],[width/2,height/2],[width-0.5,height-0.5]]
    require(type(rows) is list and len(rows)==len(probes),'ASTROMETRY_COORDINATE_COPY_PROBES')
    for row,probe in zip(rows,probes):
        require(type(row) is dict and type(row.get('pixel')) is list
            and len(row['pixel'])==2 and all(type(n) in {int,float} and math.isfinite(n)
                for n in row['pixel']) and row['pixel']==probe,'ASTROMETRY_COORDINATE_COPY_PROBES')
        reference,derived=row.get('reference'),row.get('derived')
        require(type(reference) is list and type(derived) is list and len(reference)==len(derived)==2
            and all(type(n) in {int,float} and math.isfinite(n) for n in reference+derived),
            'ASTROMETRY_COORDINATE_COPY_MISSING')
        require(0<=reference[0]<360 and -90<=reference[1]<=90
            and reference==derived,'ASTROMETRY_COORDINATE_COPY_MISMATCH')


def inspect_context(lineage_directory,lineage_sha,draft_path,draft_sha,solver_directory,solver_sha,wcs_directory,wcs_sha):
    lineage=inspect_lineage(lineage_directory,lineage_sha,draft_path,draft_sha)
    sr,st,sm=retained(solver_directory,solver_sha,'inputHashUnchanged','COMPLETED_CANDIDATE_WCS_WITH_HELD_OUT_REFERENCES')
    wr,wt,wm=retained(wcs_directory,wcs_sha,'parentHashesUnchanged','COMPLETED_SIGNED_GREEN_WITH_CANDIDATE_WCS')
    require(type(sm['source']) is str and sm['source'].startswith('CDS VizieR Gaia DR3 I/355/gaiadr3;')
        and re.search(r'Reference catalog\s*\.+\s*Gaia DR3\s*\n',st['solutionSummary']) is not None,
        'ASTROMETRY_CATALOG_VERSION')
    source=header(sm['input']);require(source['sha256']==sm['inputSHA256'],'ASTROMETRY_ORIGINAL_CHANGED')
    row=next((r for r in lineage['inputs'] if r['rawSha256']==source['sha256']),None)
    require(row is not None and source['keywords'].get('FILTER')==row['filter'],'ASTROMETRY_LINEAGE_INPUT')
    parents={p['sha256']:p['path'] for p in wm['parents']}
    solver_path=safe_path(st['output']);wcs_path=safe_path(wt['output'])
    require(solver_path.parent==safe_path(solver_directory) and wcs_path.parent==safe_path(wcs_directory)
        and sr['products'][solver_path.name] in parents and row['derivedSha256'] in parents
        and len(wm['parents'])==len(parents)==2,'ASTROMETRY_WCS_PARENTS')
    for sha,path in parents.items():require(fingerprint(path)['sha256']==sha,'ASTROMETRY_WCS_PARENT_CHANGED')
    derived=header(wcs_path);pre_wcs=header(parents[row['derivedSha256']])
    require(pre_wcs['geometry']==source['geometry']==derived['geometry']
        and all(pre_wcs['keywords'].get(k)==source['keywords'].get(k)
                for k in ('DATE-OBS','DATE-AVG','EXPTIME','FILTER')),'ASTROMETRY_GEOMETRY_OR_TIMING_PARENT')
    coordinate_copy_checks(wt,source['geometry'])
    require(fingerprint(Path(solver_directory)/'entry.js')['sha256']==sm['entrySHA256']
        and fingerprint(Path(wcs_directory)/'entry.js')['sha256']==wm['scriptSHA256'],'ASTROMETRY_SCRIPT')
    split=pinned_json(Path(solver_directory)/'catalog-split.json',sr['products']['catalog-split.json'])
    centers=pinned_json(Path(solver_directory)/'retained-centroids.json',sr['products']['retained-centroids.json'])
    return {'schema':'BKL051_ASTROMETRY_CONTEXT_V1','lineageReceiptSha256':lineage_sha,
        'candidateDraftSha256':draft_sha,'candidatePlanRef':lineage['candidatePlanRef'],
        'solverReceiptSha256':solver_sha,'wcsReceiptSha256':wcs_sha,
        'inputRef':row['inputRef'],'rawSha256':row['rawSha256'],'parentDerivedSha256':row['derivedSha256'],
        'wcsDerivedSha256':derived['sha256'],'filter':row['filter'],'geometry':source['geometry'],
        'solutionState':'CANDIDATE_NOT_VALIDATED','catalog':'Gaia DR3',
        'catalogEpochPropagation':'RETAINED_NATIVE_CONDITIONAL_NO_FULL_COVARIANCE',
        'pixelConvention':'PI_NATIVE_GEOMETRIC_RETAINED_CALLER',
        'pixelEquality':'RETAINED_NATIVE_ZERO_DIFFERENCE_NOT_REMEASURED',
        'holdout':residuals(st,split,centers),'timing':timing(source,derived),
        'byteIntegrity':'RECHECKED_LOCAL_FILES','scienceValidation':'NOT_VALIDATED',
        'significance':None,'qualifiedControls':0,'executionAuthorized':False}
