"""Plan-bound preliminary flux comparison from sealed diagnostic journals.

Scale and covariance declarations are pinned, not inferred from equal filters,
exposure durations or a partial read-noise map. No detector or significance.
"""
import math
from tools.pixinsight.local_pilot.broker import require, opaque
from tools.scientific_transients.attempt_journal import AttemptJournal, read_json, write_new
from tools.scientific_transients.local_registry import safe_path
from tools.scientific_transients.local_report import inspect as inspect_report
from tools.scientific_transients.triplet_report import inspect_triplet
from tools.scientific_transients.astrometry_context import header, timestamp_seconds
from tools.scientific_transients.queue import fields, digest


def finite(v):return type(v) in {int,float} and math.isfinite(v)


def conditional_sigma(variances,covariances,gradient):
    """First-order propagation on a declared [left flux,right flux,scale] matrix."""
    require(type(gradient) is list and len(gradient)==3 and all(finite(v) for v in gradient),
            'MULTIEPOCH_GRADIENT')
    require(type(variances) is list and type(covariances) is list
        and len(variances)==len(covariances)==3
        and all(v is None or finite(v) and v>=0 for v in variances)
        and all(v is None or finite(v) for v in covariances),'MULTIEPOCH_BUDGET_NUMERIC')
    pairs=((0,1),(0,2),(1,2));std=[math.sqrt(v) if v is not None else None for v in variances]
    for c,(i,j) in zip(covariances,pairs):
        if c is None:continue
        require(not (variances[i]==0 or variances[j]==0) or c==0,'MULTIEPOCH_ZERO_VARIANCE_COVARIANCE')
        if std[i] is not None and std[j] is not None:
            require(abs(c)<=std[i]*std[j],'MULTIEPOCH_IMPOSSIBLE_COVARIANCE')
    if None in variances or None in covariances:return None
    corr=[[1. if i==j and std[i]>0 else 0. for j in range(3)] for i in range(3)]
    for c,(i,j) in zip(covariances,pairs):corr[i][j]=corr[j][i]=c/(std[i]*std[j]) if std[i]*std[j] else 0.
    lower=[[0.]*3 for _ in range(3)];tolerance=64*2.220446049250313e-16
    for i in range(3):
        for j in range(i+1):
            residual=corr[i][j]-math.fsum(lower[i][k]*lower[j][k] for k in range(j))
            if i==j:
                require(residual>=-tolerance,'MULTIEPOCH_NON_PSD_BUDGET');lower[i][j]=math.sqrt(max(0,residual))
            elif lower[j][j]==0:require(abs(residual)<=tolerance,'MULTIEPOCH_NON_PSD_BUDGET')
            else:lower[i][j]=residual/lower[j][j]
    weights=[g*s for g,s in zip(gradient,std)]
    require(all(finite(w) for w in weights),'MULTIEPOCH_OVERFLOW')
    sigma=math.hypot(*(math.fsum(weights[i]*lower[i][j] for i in range(3)) for j in range(3)))
    require(finite(sigma),'MULTIEPOCH_OVERFLOW');return sigma


def compare(plan,case_ref,journal_directories,budget_path,budget_sha):
    budget,actual=read_json(safe_path(budget_path))
    require(digest(budget_sha) and actual==budget_sha,'MULTIEPOCH_BUDGET_CHANGED')
    fields(budget,{'schema','planSha256','headSha256','caseRef','sourceRef','referenceFrameRef',
        'origin','pairs','omittedComponents','skyIncludesReadNoise','readNoiseAddedSeparately'})
    anchor=plan.read();events,head=plan.events()
    require(budget['schema']=='BKL051_MULTI_EPOCH_BUDGET_V1' and budget['planSha256']==plan.sha
        and budget['headSha256']==head and budget['caseRef']==case_ref and opaque(budget['sourceRef'])
        and budget['origin'] in {'SYNTHETIC_TEST','PRIVATE_DECLARATIONS'},'MULTIEPOCH_PLAN_BINDING')
    case=next((c for c in anchor['draft']['cases'] if c['caseRef']==case_ref),None)
    require(case is not None and budget['referenceFrameRef'] in {f['frameRef'] for f in case['frames']},'MULTIEPOCH_CASE')
    omissions=budget['omittedComponents']
    require(type(omissions) is list and 1<=len(omissions)<=7 and len(set(omissions))==len(omissions)
        and all(x in {'MASTER_CALIBRATION','RESAMPLING_COVARIANCE','SKY_ESTIMATOR','CROWDED_PSF',
                      'SCALE_ESTIMATION','PASSBAND_RESPONSE','UNKNOWN'} for x in omissions),'MULTIEPOCH_OMISSIONS')
    require(all(budget[k] is None or type(budget[k]) is bool for k in ('skyIncludesReadNoise','readNoiseAddedSeparately'))
        and not(budget['skyIncludesReadNoise'] is True and budget['readNoiseAddedSeparately'] is True),
        'MULTIEPOCH_DOUBLE_READ_NOISE')
    requested=budget['pairs'];others={f['frameRef'] for f in case['frames']} - {budget['referenceFrameRef']}
    require(type(requested) is list and len(requested)==2
        and {p['frameRef'] for p in requested}==others,'MULTIEPOCH_PAIR_COVERAGE')
    for p in requested:
        fields(p,{'frameRef','rightToReferenceScale','variances','covariances'})
        require(p['rightToReferenceScale'] is None or finite(p['rightToReferenceScale']) and p['rightToReferenceScale']>0,
                'MULTIEPOCH_SCALE')
        conditional_sigma(p['variances'],p['covariances'],[0,0,0])
    technical=inspect_triplet(plan,case_ref,journal_directories);rows=[]
    attempt_events=[e for e in events if e['kind']=='ATTEMPT' and e['caseRef']==case_ref]
    for event,verified in zip(attempt_events,technical['attempts']):
        data=event['data'];row={'journalHeadSha256':data['journalHeadSha256'],'frameRefs':verified['frameRefs'],
            'technicalState':data['technicalState'],'reportSha256':data['technicalReportSha256'],
            'selection':'UNAVAILABLE','flux':None,'band':None,'dateObs':None,'exposureSeconds':None,
            'apertureParameters':None,'background':None,'skySampleCount':None}
        if verified['verification']=='RECHECKED_TECHNICAL_REPORT':
            journal=AttemptJournal(safe_path(journal_directories[data['identity']['attemptId']]),data['identity'])
            report=inspect_report(journal,data['technicalReportSha256'])
            candidates=[(m,r) for m in report['measurements'] for r in m['rows'] if r['sourceRef']==budget['sourceRef']]
            if len(candidates)==1:
                m,r=candidates[0];require(m['unit']=='NORMALIZED_SAMPLE_SUM','MULTIEPOCH_UNIT')
                row['selection']='CLIPPED_OR_BACKGROUND_MISSING' if r['clipped'] or not r['backgroundAvailable'] else 'DIAGNOSTIC_ROW'
                row['apertureParameters']=m['parameters']
                row['background']=r['background'];row['skySampleCount']=r['skySampleCount']
                if row['selection']=='DIAGNOSTIC_ROW':row['flux']=r['fluxNormalizedSampleSum']
            else:row['selection']='SOURCE_MISSING_OR_AMBIGUOUS'
            snapshot=next(r for r in journal.anchor['snapshot'] if r['role']=='INPUT')
            try:
                h=header(journal.directory/snapshot['path']);k=h['keywords']
                require(k.get('FILTER') in {'Green','Red','Blu','L-Pro'},'MULTIEPOCH_HEADER_BAND')
                timestamp_seconds(k['DATE-OBS'])
                from decimal import Decimal
                exposure=Decimal(k['EXPTIME']);require(exposure.is_finite() and exposure>0,'MULTIEPOCH_EXPOSURE')
                row.update(band=k['FILTER'],dateObs=k['DATE-OBS'],exposureSeconds=str(exposure))
            except (OSError,ValueError,KeyError,TypeError):pass  # unknown metadata never supplied from the budget
        rows.append(row)
    reference=next((r for r in rows if r['frameRefs']==[budget['referenceFrameRef']]),None);comparisons=[]
    for p in requested:
        right=next((r for r in rows if r['frameRefs']==[p['frameRef']]),None);reasons=[]
        if technical['status']!='TECHNICAL_COVERAGE_COMPLETE':reasons.append('TRIPLET_TECHNICAL_COVERAGE_INCOMPLETE')
        if not reference or not right or reference['selection']!='DIAGNOSTIC_ROW' or right['selection']!='DIAGNOSTIC_ROW':
            reasons.append('MEASUREMENTS_UNAVAILABLE_OR_AMBIGUOUS')
        if reference and right:
            if reference['apertureParameters']!=right['apertureParameters']:reasons.append('APERTURE_PARAMETERS_DIFFER')
            if reference['band'] is None or right['band'] is None:reasons.append('BAND_UNKNOWN')
            elif reference['band']!=right['band']:reasons.append('FILTERS_INCOMPATIBLE')
            if reference['dateObs'] is None or right['dateObs'] is None:reasons.append('EPOCH_OR_EXPOSURE_UNKNOWN')
            elif timestamp_seconds(reference['dateObs'])==timestamp_seconds(right['dateObs']):reasons.append('SAME_RECORDED_EPOCH')
        scale=p['rightToReferenceScale']
        if scale is None:reasons.append('SCALE_UNKNOWN_NOT_REPLACED_WITH_ONE')
        difference=sigma=None
        if not reasons:
            difference=reference['flux']-scale*right['flux'];require(finite(difference),'MULTIEPOCH_OVERFLOW')
            sigma=conditional_sigma(p['variances'],p['covariances'],[1,-scale,-right['flux']])
        if None in p['variances']:reasons.append('UNKNOWN_VARIANCE_NOT_ZERO')
        if None in p['covariances']:reasons.append('UNKNOWN_COVARIANCE_NOT_ZERO')
        comparisons.append({'frameRef':p['frameRef'],'rightToReferenceScale':scale,
            'variances':p['variances'],'covariances':p['covariances'],
            'algebraicDifference':difference,'conditionalSigma':sigma,'blockers':reasons})
    require(plan.events()[1]==head and read_json(safe_path(budget_path))[1]==actual
        and inspect_triplet(plan,case_ref,journal_directories)==technical,'MULTIEPOCH_SOURCES_CHANGED')
    return {'schema':'BKL051_MULTI_EPOCH_COMPARISON_V1','planSha256':plan.sha,'headSha256':head,
        'caseRef':case_ref,'sourceRef':budget['sourceRef'],'referenceFrameRef':budget['referenceFrameRef'],
        'budgetSha256':budget_sha,'origin':budget['origin'],'unit':'NORMALIZED_SAMPLE_SUM',
        'technicalCoverage':technical['status'],'attempts':rows,'pairs':comparisons,
        'omittedComponents':omissions,'propagation':'FIRST_ORDER_DELTA_METHOD_PARTIAL_DECLARATIONS',
        'skyIncludesReadNoise':budget['skyIncludesReadNoise'],'readNoiseAddedSeparately':budget['readNoiseAddedSeparately'],
        'sourceAssociation':'OPAQUE_REF_NOT_PHYSICAL_CROSS_MATCH_ATTESTATION',
        'photometricComparability':'NOT_VALIDATED','scienceValidation':'NOT_VALIDATED',
        'fullVariance':None,'significance':None,'variabilityClassification':'NOT_EVALUATED',
        'qualifiedControls':0,'confirmatoryEligible':False}


def main():
    import argparse
    from pathlib import Path
    from tools.scientific_transients.test_plan import PlanVersion
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('plan','plan-sha','case','journals','budget','budget-sha','output'):p.add_argument('--'+n,required=True)
    a=p.parse_args();mapping,_=read_json(Path(a.journals))
    print(write_new(Path(a.output),compare(PlanVersion(a.plan,a.plan_sha),a.case,mapping,a.budget,a.budget_sha)))


if __name__=='__main__':main()
