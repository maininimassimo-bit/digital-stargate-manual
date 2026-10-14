"""Score frozen exploratory injections without calling detector flux photometry.

Baseline probes are not qualified astronomical null controls. No independent
trial count, false-positive bound, significance or scientific acceptance.
"""
import math
from pathlib import Path
from tools.pixinsight.local_pilot.broker import require,opaque
from tools.scientific_transients.attempt_journal import read_json,write_new
from tools.scientific_transients.local_registry import safe_path,fingerprint,relative
from tools.scientific_transients.queue import fields,digest

def finite(v):return type(v) in {int,float} and math.isfinite(v)
def pinned(path,sha):
    require(digest(sha),'RECOVERY_PIN');value,actual=read_json(safe_path(path))
    require(actual==sha,'RECOVERY_CHANGED');return value

def evaluate(targets,baseline,after,radius,group_ref,*,available=True):
    require(type(available) is bool and opaque(group_ref) and finite(radius) and radius>0
        and type(targets) is list and 1<=len(targets)<=10000,'RECOVERY_ARGUMENTS')
    seen=set()
    for t in targets:
        fields(t,{'targetRef','x','y','fluxNormalizedSampleSum'})
        require(opaque(t['targetRef']) and t['targetRef'] not in seen and all(finite(t[k]) for k in ('x','y','fluxNormalizedSampleSum'))
            and t['fluxNormalizedSampleSum']>0,'RECOVERY_TARGET');seen.add(t['targetRef'])
    for sources in (baseline,after):
        require(type(sources) is list and len(sources)<=100000,'RECOVERY_SOURCES')
        ids=set()
        for r in sources:
            fields(r,{'sourceIndex','x','y'});require(type(r['sourceIndex']) is int and r['sourceIndex']>=0
                and r['sourceIndex'] not in ids and finite(r['x']) and finite(r['y']),'RECOVERY_SOURCE')
            ids.add(r['sourceIndex'])
    rows=[];usable=available and len(baseline)>0
    associations=[];after_uses={}
    for t in targets:
        b=[r['sourceIndex'] for r in baseline if math.hypot(r['x']-t['x'],r['y']-t['y'])<=radius] if usable else []
        a=[r['sourceIndex'] for r in after if math.hypot(r['x']-t['x'],r['y']-t['y'])<=radius] if usable else []
        associations.append((t,b,a))
        for index in a:after_uses[index]=after_uses.get(index,0)+1
    for t,b,a in associations:
        shared=any(after_uses[index]>1 for index in a)
        status='MISSING' if not usable else 'AMBIGUOUS' if b or len(a)>1 or shared else 'EVALUATED'
        rows.append({'targetRef':t['targetRef'],'groupRef':group_ref,'truthAddedFlux':t['fluxNormalizedSampleSum'],
            'injectionStatus':status,'recovered':len(a)==1 if status=='EVALUATED' else None,
            'baselineMatches':b,'afterMatches':a,'baselineProbeFlag':bool(b) if usable else None,
            'measuredAddedFlux':None,'fullFluxVariance':None,'significance':None})
    return {'rows':rows,'injectionDenominator':len(targets),'recoveredInjections':sum(r['recovered'] is True for r in rows),
        'evaluatedInjections':sum(r['injectionStatus']=='EVALUATED' for r in rows),
        'ambiguousInjections':sum(r['injectionStatus']=='AMBIGUOUS' for r in rows),
        'missingInjections':sum(r['injectionStatus']=='MISSING' for r in rows),
        'baselineProbeDenominator':len(targets),'baselineProbesWithSources':sum(r['baselineProbeFlag'] is True for r in rows),
        'independentTrialCount':None,'qualifiedNullControls':0,'falsePositiveConfidenceBound':None,
        'measuredFluxBias':None,'measuredFluxErrorRMS':None,
        'status':'DIAGNOSTIC_POSITION_SCORING_ONLY' if usable else 'REFERENCE_DETECTOR_UNAVAILABLE_OR_ZERO_REQUIRES_REVIEW'}

def inspect(directory,prelaunch_sha,seal_path,seal_sha):
    root=safe_path(directory);pre=pinned(root/'prelaunch.json',prelaunch_sha);pre_sha=prelaunch_sha
    seal=pinned(seal_path,seal_sha)
    require(seal['schema']=='BKL051_POST_RUN_RECOVERY_ARCHIVE_SEAL_V1'
        and seal['scope']=='POST_RUN_AFTER_INITIAL_SCORE_NOT_PRETRUTH_PROOF'
        and seal['prelaunchSha256']==pre_sha,'RECOVERY_ARCHIVE_SEAL')
    for r in seal['files']:
        require(fingerprint(root/relative(r['path']))=={k:r[k] for k in ('sha256','bytes')},'RECOVERY_ARCHIVE_CHANGED')
    protocol=pinned(root/'private/protocol.json',pre['protocolSha256'])
    require(pre['schema']=='BKL051_RECOVERY_PRELAUNCH_V1'
        and protocol['schema']=='BKL051_CONTROLLED_RECOVERY_PROTOCOL_V1'
        and protocol['sourceShotNoiseAdded'] is False and protocol['scientificValidation']=='NOT_VALIDATED'
        and protocol['confirmatoryEligible'] is False,'RECOVERY_SCOPE')
    source,_=read_json(root/'private/source.json')
    require(fingerprint(source['source'])['sha256']==source['sha256']==pre['sourceSha256']==protocol['sourceSha256'],'RECOVERY_ORIGINAL_CHANGED')
    generator=worker=None;terminal_hashes={}
    for stage in ('generator','worker'):
        require(fingerprint(root/stage/'entry.js')['sha256']==pre[stage+'ScriptSha256'],'RECOVERY_SCRIPT_CHANGED')
        verification,_=read_json(root/stage/'verification.json');stopped,_=read_json(root/stage/'owned-process-stopped.json')
        terminal=pinned(root/stage/'terminal.json',verification['terminalSha256'])
        require(terminal['state']=='COMPLETED' and stopped['ownedHandleStopped'] is True
            and stopped['terminalSha256']==verification['terminalSha256'],'RECOVERY_STAGE_UNCONFIRMED')
        terminal_hashes[stage]=verification['terminalSha256']
        if stage=='generator':generator=terminal
        else:worker=terminal
    require(generator['sourceSha256']==pre['sourceSha256'] and abs(generator['expectedAdded']-generator['totalAdded'])<1e-10
        and abs(generator['expectedAdded']-math.fsum(t['fluxNormalizedSampleSum'] for t in protocol['targets']))<1e-12
        and worker['truthPositionsPassedToDetector'] is False,'RECOVERY_GENERATOR_OR_TRUTH_BOUNDARY')
    manifest,manifest_sha=read_json(root/'worker/images.json')
    require(read_json(root/'generator/worker-images.json')[1]==manifest_sha,'RECOVERY_WORKER_MANIFEST_CHANGED')
    roles,_=read_json(root/'private/image-roles.json');catalogs={};image_records=[]
    require(len(manifest['images'])==len(worker['rows'])==2,'RECOVERY_IMAGE_COUNT')
    for image in manifest['images']:
        require(opaque(image['imageRef']) and fingerprint(image['path'])['sha256']==image['sha256'],'RECOVERY_IMAGE_CHANGED')
        c,sha=read_json(root/'worker'/(image['imageRef']+'-sources.json'))
        row=next(r for r in worker['rows'] if r['imageRef']==image['imageRef'])
        config=row['detectorParameters']
        require(config['fitPSF']==protocol['detector']['fitPSF']
            and config['minStructureSize']==protocol['detector']['minStructureSize']
            and math.isclose(config['sensitivity'],protocol['detector']['sensitivity'],rel_tol=1e-6),
            'RECOVERY_DETECTOR_CONFIG_CHANGED')
        require(c['schema']=='BKL051_RECOVERY_DETECTOR_SOURCES_V1'
            and c['inputSha256']==row['inputSha256']==image['sha256'] and row['changedPixels']==0
            and len(c['sources'])==row['sourceCount'] and c['coordinateConvention']=='SAMPLE_INDEX_ZERO','RECOVERY_CATALOG_BINDING')
        catalogs[image['imageRef']]=c['sources'];image_records.append({'imageRef':image['imageRef'],'imageSha256':image['sha256'],'catalogSha256':sha,'sources':row['sourceCount']})
    require(roles['baselineImageRef']!=roles['injectedImageRef'] and set(roles.values())==set(catalogs),'RECOVERY_ROLE_BINDING')
    require(worker['rows'][0]['detectorParameters']==worker['rows'][1]['detectorParameters'],'RECOVERY_DIFFERENT_DETECTOR_CONFIGS')
    # Structural property only; it does not attest an adversarial/double-blind study.
    worker_text=(root/'worker/entry.js').read_text();worker_payload=(root/'worker/images.json').read_text()
    require(all(t['targetRef'] not in worker_text and t['targetRef'] not in worker_payload for t in protocol['targets']),'RECOVERY_TRUTH_LEAK')
    result=evaluate(protocol['targets'],catalogs[roles['baselineImageRef']],catalogs[roles['injectedImageRef']],protocol['matchingRadiusPixels'],pre['sourceSha256'][:32])
    return {'schema':'BKL051_CONTROLLED_RECOVERY_RESULT_V1','origin':'SYNTHETIC_ADDITION_ON_REAL_M27_BACKGROUND',
        'prelaunchSha256':pre_sha,'protocolSha256':pre['protocolSha256'],'sourceSha256':pre['sourceSha256'],'archiveSealSha256':seal_sha,
        'terminalSha256':terminal_hashes,'images':image_records,'matchingRadiusPixels':protocol['matchingRadiusPixels'],
        'gaussianSigmaPixels':protocol['gaussianSigmaPixels'],'sourceShotNoiseAdded':False,
        'truthSeparation':'STRUCTURAL_WORKER_PAYLOAD_CHECK_ONLY_NOT_INDEPENDENT_BLIND_ATTESTATION',
        'positionsPassedToDetector':False,'scientificValidation':'NOT_VALIDATED','scientificAcceptance':False,
        'archiveSealTiming':'POST_RUN_AFTER_INITIAL_SCORE_NOT_PRETRUTH_PROOF',
        'badPixelQuality':'ALL_PIXELS_ADMITTED_NOT_SCIENTIFIC_BAD_PIXEL_VALIDATION',
        'parameterPolicyAccepted':False,'submissionAuthorized':False,'completeDependencyArchive':False,**result}

def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('directory','prelaunch-sha','seal','seal-sha','output'):p.add_argument('--'+n,required=True)
    a=p.parse_args();print(write_new(Path(a.output),inspect(a.directory,a.prelaunch_sha,a.seal,a.seal_sha)))

if __name__=='__main__':main()
