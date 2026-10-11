"""Strict native measurement projection; measurements never confer acceptance."""
import copy
import math
import re

VERSION = 'DSG_PIAI_NATIVE_MEASUREMENTS_V2'
def require(condition, code):
    if not condition:
        raise ValueError(code)
def number(value):
    return type(value) in (int, float) and math.isfinite(value)
def digest(value):
    return isinstance(value, str) and re.fullmatch('[a-f0-9]{64}', value) is not None

def validate(value, binding):
    """Binding must be built from independently verified local files, not AI output."""
    keys = {'version','width','height','channels','regions','noise','starSelection','detector','fits',
            'noiseUnits','noiseAssumption','backgroundValidity','linearity','registration','acceptance',
            'sourceSha256','imageIndex','adapterSha256','starDetectorSha256','coreVersion',
            'historyUnchanged','originalUnchanged','status'}
    require(isinstance(value,dict) and set(value)==keys, 'NATIVE_MEASUREMENT_FIELDS')
    require(set(binding)=={'sourceSha256','imageIndex','adapterSha256','starDetectorSha256','width','height','channels'},
            'NATIVE_MEASUREMENT_BINDING_FIELDS')
    require(all(value[k]==v for k,v in binding.items()), 'NATIVE_MEASUREMENT_BINDING')
    require(all(digest(value[k]) for k in ('sourceSha256','adapterSha256','starDetectorSha256')) and
            type(value['imageIndex']) is int and 0<=value['imageIndex']<16, 'NATIVE_MEASUREMENT_HASH')
    require(value['version']==VERSION and value['status']=='MEASURED' and
            value['historyUnchanged'] is True and value['originalUnchanged'] is True, 'NATIVE_READ_ONLY_RECEIPT')
    w,h,channels=value['width'],value['height'],value['channels']
    require(type(w) is int and type(h) is int and 32<=w<=12000 and 32<=h<=12000 and
            type(channels) is int and channels in (1,3), 'NATIVE_MEASUREMENT_GEOMETRY')
    require(value['noiseUnits']=='NORMALIZED_IMAGE_SAMPLES' and
            value['noiseAssumption']=='GAUSSIAN_COMPONENT_ESTIMATE' and
            all(value[k]=='NOT_ESTABLISHED' for k in ('backgroundValidity','linearity','registration','acceptance')),
            'NATIVE_UNSUPPORTED_ATTESTATION')
    core=value['coreVersion']
    require(isinstance(core,dict) and set(core)=={'major','minor','release','revision','build'} and
            all(type(v) is int and 0<=v<100000 for v in core.values()), 'NATIVE_CORE_VERSION')
    regions=value['regions']
    require(isinstance(regions,list) and len(regions)<=8, 'NATIVE_REGIONS')
    for r in regions:
        require(isinstance(r,list) and len(r)==4 and all(type(n) is int for n in r) and
                0<=r[0]<r[2]<=w and 0<=r[1]<r[3]<=h and r[2]-r[0]>=32 and r[3]-r[1]>=32,'NATIVE_REGION')
    noise=value['noise']
    require(isinstance(noise,list) and len(noise)==len(regions)*channels,'NATIVE_NOISE_COUNT')
    for row,(region,channel) in zip(noise,((r,c) for r in range(len(regions)) for c in range(channels))):
        require(isinstance(row,dict) and set(row)=={'region','channel','estimates'} and
                type(row['region']) is int and row['region']==region and
                type(row['channel']) is int and row['channel']==channel,'NATIVE_NOISE_SCOPE')
        estimates=row['estimates']; r=regions[region]; area=(r[2]-r[0])*(r[3]-r[1])
        require(isinstance(estimates,list) and len(estimates)==3,'NATIVE_NOISE_ESTIMATES')
        for e,layers in zip(estimates,(4,3,2)):
            require(isinstance(e,dict) and set(e)=={'method','layers','sigma','support'} and
                    e['method']=='MRS' and type(e['layers']) is int and e['layers']==layers and
                    number(e['sigma']) and e['sigma']>=0 and type(e['support']) is int and
                    0<=e['support']<=area,'NATIVE_NOISE_ESTIMATE')
    selection=value['starSelection']
    require(isinstance(selection,dict) and set(selection)=={'detected','selected','grid','method'} and
            type(selection['detected']) is int and 0<=selection['detected']<=w*h and
            type(selection['selected']) is int and 0<=selection['selected']<=min(256,selection['detected']) and
            type(selection['grid']) is int and selection['grid']==16 and
            selection['method']=='BRIGHTEST_ISOLATED_PER_CELL','NATIVE_STAR_SELECTION')
    expected_detector={'version':2.01,'structureLayers':5,'hotPixelFilterRadius':1,
            'noiseReductionFilterRadius':0,'sensitivity':.5,'peakResponse':.5,'upperLimit':1}
    require(isinstance(value['detector'],dict) and value['detector']==expected_detector and
            all(type(value['detector'][k]) is type(v) for k,v in expected_detector.items()),'NATIVE_DETECTOR')
    fits=value['fits']; seen=set()
    require(isinstance(fits,list) and len(fits)<=selection['selected']*channels,'NATIVE_FIT_COUNT')
    projected=[]
    for fit in fits:
        fields={'star','channel','model','background','amplitude','x','y','sx','sy','theta','residual'}
        require(isinstance(fit,dict) and set(fit)==fields and type(fit['star']) is int and
                0<=fit['star']<selection['selected'] and type(fit['channel']) is int and
                0<=fit['channel']<channels and fit['model']=='GAUSSIAN','NATIVE_PSF_SCOPE')
        identity=(fit['star'],fit['channel']);require(identity not in seen,'NATIVE_DUPLICATE_PSF');seen.add(identity)
        require(all(number(fit[k]) for k in fields-{'star','channel','model'}) and
                fit['amplitude']>0 and 0<=fit['x']<w and 0<=fit['y']<h and
                0<fit['sx']<=max(w,h) and 0<fit['sy']<=max(w,h) and fit['residual']>=0,'NATIVE_PSF_NUMBERS')
        major,minor=max(fit['sx'],fit['sy']),min(fit['sx'],fit['sy'])
        projected.append({**copy.deepcopy(fit),'fwhmMajorPixels':2*math.sqrt(2*math.log(2))*major,
            'fwhmMinorPixels':2*math.sqrt(2*math.log(2))*minor,'eccentricity':math.sqrt(1-(minor/major)**2)})
    return {**copy.deepcopy(value),'derivedGaussianFits':projected}
