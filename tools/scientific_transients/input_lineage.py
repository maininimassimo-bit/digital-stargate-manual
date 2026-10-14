"""Import retained native metadata-copy receipts. Rehash bytes; never infer calibration validity."""
import hashlib
from pathlib import Path

from tools.pixinsight.local_pilot.broker import require
from tools.scientific_transients.attempt_journal import read_json, write_new
from tools.scientific_transients.local_registry import safe_path, fingerprint
from tools.scientific_transients.queue import digest, fields
from tools.scientific_transients.test_plan import validate_draft


def inspect_lineage(directory, receipt_sha256, draft_path, draft_sha256):
    require(digest(receipt_sha256) and digest(draft_sha256), 'LINEAGE_EXPECTED_HASH')
    directory=safe_path(directory)
    receipt,actual=read_json(directory/'receipt.json')
    require(actual==receipt_sha256, 'LINEAGE_RECEIPT_CHANGED')
    fields(receipt,{'terminal','parentHashesUnchanged','products'})
    require(receipt['parentHashesUnchanged'] is True and type(receipt['products']) is dict, 'LINEAGE_RECEIPT')
    products=receipt['products']
    require(all(type(k) is str and k not in {'','.','..'} and Path(k).name==k and ':' not in k and '/' not in k and '\\' not in k
                and digest(v) for k,v in products.items()),'LINEAGE_PRODUCT_RECORD')
    require({'manifest.json','terminal.json','entry.js'}<=set(products),'LINEAGE_EVIDENCE_MISSING')
    manifest,manifest_sha=read_json(directory/'manifest.json')
    terminal,terminal_sha=read_json(directory/'terminal.json')
    require(manifest_sha==products['manifest.json'] and terminal_sha==products['terminal.json']
            and terminal==receipt['terminal'],'LINEAGE_NATIVE_BINDING')
    fields(manifest,{'parents','entrySHA256','purpose','metadataPolicy'})
    require(manifest['entrySHA256']==products['entry.js']==fingerprint(directory/'entry.js')['sha256'], 'LINEAGE_SCRIPT_CHANGED')
    fields(terminal,{'status','scienceValidation','rows'})
    require(terminal['status']=='COMPLETED_METADATA_BOUND_SIGNED_PILOT'
            and terminal['scienceValidation']=='NOT_VALIDATED' and type(terminal['rows']) is list
            and 0<len(terminal['rows'])<=64 and type(manifest['parents']) is list
            and len(manifest['parents'])==2*len(terminal['rows']),'LINEAGE_NATIVE_SCOPE')
    parents={}
    for row in manifest['parents']:
        fields(row,{'path','sha256'})
        require(type(row['path']) is str and row['path'] not in parents and digest(row['sha256']), 'LINEAGE_PARENT')
        require(Path(row['path']).is_absolute(),'LINEAGE_ABSOLUTE_PATH');path=safe_path(row['path'])
        require(fingerprint(path)['sha256']==row['sha256'],'LINEAGE_PARENT_CHANGED')
        parents[row['path']]=row['sha256']
    draft,actual_draft_sha=read_json(draft_path)
    require(actual_draft_sha==draft_sha256,'LINEAGE_DRAFT_CHANGED');validate_draft(draft)
    candidate_hashes={f['sha256'] for c in draft['cases'] for f in c['frames']}
    rows=[];seen=set();seen_raw=set();used_parents=set()
    for row in terminal['rows']:
        fields(row,{'filter','parent','observationSource','path','copiedProperties','omittedProperties',
                    'keywordCount','maxAbsolutePixelDifference','scienceValidation'})
        require(row['filter'] in {'L-Pro','Red','Green','Blu'} and row['scienceValidation']=='NOT_VALIDATED'
                and type(row['maxAbsolutePixelDifference']) in {int,float} and row['maxAbsolutePixelDifference']==0
                and type(row['keywordCount']) is int and row['keywordCount']>=0,'LINEAGE_ROW')
        require(row['parent'] in parents and row['observationSource'] in parents
                and row['parent']!=row['observationSource'],'LINEAGE_ANCESTRY')
        require(type(row['path']) is str and Path(row['path']).is_absolute(),'LINEAGE_ABSOLUTE_PATH')
        output=safe_path(row['path'])
        require(output.parent==directory and output.name in products,'LINEAGE_OUTPUT_DIRECTORY')
        expected=products[output.name]
        require(expected not in seen and fingerprint(output)['sha256']==expected,'LINEAGE_OUTPUT_CHANGED')
        seen.add(expected);used_parents.update([row['parent'],row['observationSource']])
        raw_sha,cal_sha=parents[row['observationSource']],parents[row['parent']]
        require(len({raw_sha,cal_sha,expected})==3,'LINEAGE_IDENTITIES_NOT_DISTINCT')
        require(raw_sha not in seen_raw,'LINEAGE_DUPLICATE_ORIGINAL');seen_raw.add(raw_sha)
        rows.append({'inputRef':hashlib.sha256((raw_sha+expected).encode()).hexdigest()[:32],
                     'filter':row['filter'],'rawSha256':raw_sha,'calibratedSha256':cal_sha,'derivedSha256':expected,
                     'byteIntegrity':'RECHECKED_LOCAL_FILES','metadataCopy':'NATIVE_RECEIPT_REPORTED',
                     'pixelEquality':'REPORTED_ZERO_DIFFERENCE_NOT_REMEASURED',
                     'sampleMembership':'IN_CANDIDATE_MANIFEST' if raw_sha in candidate_hashes else 'OUTSIDE_CANDIDATE_MANIFEST'})
    require(used_parents==set(parents),'LINEAGE_UNUSED_PARENT')
    return {'schema':'BKL051_INPUT_LINEAGE_V1','scope':'RETAINED_METADATA_COPY_PILOT_ONLY',
            'receiptSha256':receipt_sha256,'manifestSha256':manifest_sha,'terminalSha256':terminal_sha,
            'candidateDraftSha256':draft_sha256,'candidatePlanRef':draft['planRef'],'inputs':rows,
            'calibrationSemantics':'NOT_ATTESTED_BY_THIS_IMPORT','scienceValidation':'NOT_VALIDATED',
            'completeUncertainty':None,'significance':None,'qualifiedControls':0,'executionAuthorized':False}


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('directory','receipt-sha256','draft','draft-sha256','output'):
        p.add_argument('--'+name,required=True)
    a=p.parse_args()
    print(write_new(Path(a.output),inspect_lineage(a.directory,a.receipt_sha256,Path(a.draft),a.draft_sha256)))


if __name__=='__main__':main()
