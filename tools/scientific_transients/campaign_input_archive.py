"""Private byte snapshots for campaign input witnesses; no scientific promotion.

The manifest's science states remain worker-reported declarations. Required
proof files are retained and byte-verified, not scientifically attested here.
No preliminary plan import, Owner decision, credential, network or native run.
"""
import copy
import uuid
from pathlib import Path

from tools.pixinsight.local_pilot.broker import ProtocolError, require, opaque
from tools.scientific_transients.attempt_journal import read_json, write_new, copy_verified
from tools.scientific_transients.local_registry import safe_path, relative, fingerprint
from tools.scientific_transients.queue import fields, digest
from tools.scientific_transients.confirmatory_campaign import validate_inputs, input_blockers

SOURCE_PROTOCOL='DSG_CAMPAIGN_INPUT_SOURCE_V1'
ARCHIVE_PROTOCOL='DSG_CAMPAIGN_INPUT_ARCHIVE_V1'
ROLES={'IMAGE','METADATA','BANDPASS','CALIBRATION_PROOF','UNCERTAINTY_PROOF','TIME_PROOF'}


def payload(source, manifest_sha):
    fields(source,{'protocol','witness','files'})
    require(source['protocol']==SOURCE_PROTOCOL and digest(manifest_sha),'CAMPAIGN_SOURCE_PROTOCOL')
    fields(source['witness'],{'witnessRef','purpose','correlationRef','frames'})
    result={'reportSha256':manifest_sha,**copy.deepcopy(source['witness'])}
    validate_inputs(result)
    frames={f['frameRef']:f for f in result['frames']}
    require(len(frames)==3,'CAMPAIGN_ARCHIVE_FRAME_IDENTITY')
    records=source['files']
    require(type(records) is list and 9<=len(records)<=18,'CAMPAIGN_ARCHIVE_FILE_COUNT')
    seen=set()
    for record in records:
        fields(record,{'role','frameRef','path','sha256','bytes'})
        require(type(record['role']) is str and record['role'] in ROLES and opaque(record['frameRef'])
                and record['frameRef'] in frames and digest(record['sha256'])
                and type(record['bytes']) is int and 0<record['bytes']<=2**53-1,'CAMPAIGN_ARCHIVE_FILE')
        relative(record['path']);identity=(record['frameRef'],record['role'])
        require(identity not in seen,'CAMPAIGN_ARCHIVE_DUPLICATE_ROLE');seen.add(identity)
        key={'IMAGE':'sha256','METADATA':'metadataSha256','BANDPASS':'bandpassSha256'}.get(record['role'])
        if key:require(record['sha256']==frames[record['frameRef']][key],'CAMPAIGN_ARCHIVE_FRAME_DIGEST')
    for ref,frame in frames.items():
        required={'IMAGE','METADATA','BANDPASS'}
        for state,complete,proof in [('calibration','VERIFIED_FOR_DECLARED_MODEL','CALIBRATION_PROOF'),
                ('uncertainty','COMPLETE_FOR_DECLARED_MODEL','UNCERTAINTY_PROOF'),
                ('timeStatus','ACQUIRED_VERIFIED','TIME_PROOF')]:
            if frame[state]==complete:required.add(proof)
        require(all((ref,role) in seen for role in required),'CAMPAIGN_ARCHIVE_REQUIRED_PROOF_MISSING')
    return result


def snapshot_name(index, record):
    suffix=Path(record['path']).suffix
    require(not suffix or (len(suffix)<=16 and suffix[1:].isascii() and suffix[1:].isalnum()),
            'CAMPAIGN_ARCHIVE_SUFFIX')
    return 'snapshot/'+str(index).zfill(3)+(suffix or '.dat')


class CampaignInputArchive:
    @classmethod
    def prepare(cls, source_root, manifest_path, expected_sha, archive_root):
        source_root=safe_path(source_root);archive_root=safe_path(archive_root)
        require(source_root.is_dir() and archive_root.is_dir() and source_root!=archive_root
                and source_root not in archive_root.parents and archive_root not in source_root.parents,
                'CAMPAIGN_ARCHIVE_ROOT_OVERLAP')
        require(digest(expected_sha),'CAMPAIGN_ARCHIVE_EXPECTED_HASH')
        try:
            manifest_path=safe_path(manifest_path);source,actual=read_json(manifest_path)
            require(actual==expected_sha,'CAMPAIGN_ARCHIVE_MANIFEST_CHANGED');witness=payload(source,actual)
            for record in source['files']:
                require(fingerprint(source_root/relative(record['path']))==
                        {k:record[k] for k in ('sha256','bytes')},'CAMPAIGN_ARCHIVE_SOURCE_CHANGED')
            directory=archive_root/witness['witnessRef'];directory.mkdir();(directory/'snapshot').mkdir()
            manifest_size=fingerprint(manifest_path)['bytes']
            copy_verified(manifest_path,directory/'manifest.json',{'sha256':actual,'bytes':manifest_size})
            retained=[]
            for index,record in enumerate(source['files']):
                name=snapshot_name(index,record)
                copy_verified(source_root/relative(record['path']),directory/name,
                              {k:record[k] for k in ('sha256','bytes')})
                retained.append({**record,'snapshot':name})
            archive={'protocol':ARCHIVE_PROTOCOL,'sourceManifestSha256':actual,'witnessRef':witness['witnessRef'],
                     'files':retained,'scienceStatements':'WORKER_REPORTED_NOT_ATTESTED',
                     'scienceValidation':'NOT_VALIDATED','executionAuthorized':False}
            sha=write_new(directory/'archive.json',archive)
            result=cls(directory,sha);result.verify();return result
        except (ProtocolError,OSError) as error:
            write_new(archive_root/('failed-'+uuid.uuid4().hex+'.json'),
                {'operation':'ARCHIVE_CAMPAIGN_INPUT','sourceManifestSha256':expected_sha,'status':'FAILED',
                 'reason':str(error) if isinstance(error,ProtocolError) else 'LOCAL_IO_ERROR',
                 'scienceValidation':'NOT_VALIDATED','executionAuthorized':False})
            raise

    def __init__(self,directory,expected_sha):
        require(digest(expected_sha),'CAMPAIGN_ARCHIVE_EXPECTED_HASH')
        self.directory=safe_path(directory);self.sha=expected_sha

    def verify(self):
        archive,sha=read_json(self.directory/'archive.json')
        require(sha==self.sha,'CAMPAIGN_ARCHIVE_INDEX_CHANGED')
        fields(archive,{'protocol','sourceManifestSha256','witnessRef','files','scienceStatements',
                        'scienceValidation','executionAuthorized'})
        require(archive['protocol']==ARCHIVE_PROTOCOL and opaque(archive['witnessRef'])
                and self.directory.name==archive['witnessRef']
                and archive['scienceStatements']=='WORKER_REPORTED_NOT_ATTESTED'
                and archive['scienceValidation']=='NOT_VALIDATED' and archive['executionAuthorized'] is False,
                'CAMPAIGN_ARCHIVE_SCOPE')
        source,actual=read_json(self.directory/'manifest.json')
        require(actual==archive['sourceManifestSha256'],'CAMPAIGN_ARCHIVE_MANIFEST_CHANGED')
        witness=payload(source,actual)
        require(witness['witnessRef']==archive['witnessRef'] and type(archive['files']) is list
                and len(archive['files'])==len(source['files']),'CAMPAIGN_ARCHIVE_BINDING')
        for index,(source_record,record) in enumerate(zip(source['files'],archive['files'])):
            fields(record,{'role','frameRef','path','sha256','bytes','snapshot'})
            require({k:v for k,v in record.items() if k!='snapshot'}==source_record
                    and record['snapshot']==snapshot_name(index,source_record),'CAMPAIGN_ARCHIVE_SNAPSHOT_BINDING')
            require(fingerprint(self.directory/relative(record['snapshot']))==
                    {k:record[k] for k in ('sha256','bytes')},'CAMPAIGN_ARCHIVE_SNAPSHOT_CHANGED')
        return witness

    def inspect(self):
        witness=self.verify()
        return {'witness':witness,'archiveSha256':self.sha,'inputBlockers':input_blockers(witness),
                'byteIntegrity':'RECHECKED_RETAINED_SNAPSHOT','scienceStatements':'WORKER_REPORTED_NOT_ATTESTED',
                'scienceValidation':'NOT_VALIDATED','qualifiedControls':0,'executionAuthorized':False}

    def export(self,destination):
        """Minimized worker payload only; writing this file never transmits it."""
        witness=self.verify();return write_new(Path(destination),witness)


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);commands=parser.add_subparsers(dest='command',required=True)
    prepare=commands.add_parser('prepare')
    for name in ('source-root','manifest','sha256','archive-root'):prepare.add_argument('--'+name,required=True)
    export=commands.add_parser('export')
    for name in ('directory','sha256','output'):export.add_argument('--'+name,required=True)
    args=parser.parse_args()
    if args.command=='prepare':
        archive=CampaignInputArchive.prepare(args.source_root,args.manifest,args.sha256,args.archive_root)
        print(archive.sha)
    else:print(CampaignInputArchive(args.directory,args.sha256).export(args.output))


if __name__=='__main__':main()
