"""Derived display assets only. Never modifies scientific pixels."""
import base64
import hashlib
import io
import math

from PIL import Image

VERSION='DSG_PIAI_DISPLAY_PREVIEW_V2'

def curve(median,target=.2):
    if type(median) not in (int,float) or not math.isfinite(median) or not 0<median<1:
        raise ValueError('PREVIEW_MEDIAN_REQUIRED')
    if type(target) not in (int,float) or not math.isfinite(target) or not .05<=target<=.5:
        raise ValueError('PREVIEW_TARGET')
    m=median*(target-1)/(2*target*median-target-median)
    return {'method':'MTF_DISPLAY_ONLY','black':0.,'white':1.,'midtones':m,
            'parentMedian':median,'displayTarget':target}

def validate_curve(value):
    if not isinstance(value,dict) or set(value)!={'method','black','white','midtones','parentMedian','displayTarget'}:
        raise ValueError('PREVIEW_CURVE_FIELDS')
    if not all(type(value[k]) in (int,float) and math.isfinite(value[k]) for k in
               ('black','white','midtones','parentMedian','displayTarget')) or value!=curve(value['parentMedian'],value['displayTarget']):raise ValueError('PREVIEW_CURVE_BINDING')
    return value

def render(samples,display_curve,region=None):
    """Array is H,W,C float, expected finite normalized scientific samples.

    Negative and overrange samples are clipped only in this display projection.
    Parent curve must be supplied unchanged for all comparison siblings.
    """
    import numpy as np  # Local renderer only; provider validation needs Pillow.
    c=validate_curve(display_curve)
    if samples.ndim!=3 or samples.shape[2] not in (1,3) or samples.dtype.kind!='f':raise ValueError('PREVIEW_ARRAY')
    h,w,channels=samples.shape
    if not 32<=w<=12000 or not 32<=h<=12000 or not np.isfinite(samples).all():raise ValueError('PREVIEW_GEOMETRY_OR_FINITE')
    if region is not None:
        if not isinstance(region,list) or len(region)!=4 or not all(type(v) is int for v in region):raise ValueError('PREVIEW_REGION')
        x0,y0,x1,y1=region
        if not 0<=x0<x1<=w or not 0<=y0<y1<=h or x1-x0>256 or y1-y0>256:raise ValueError('PREVIEW_REGION')
        selected=samples[y0:y1,x0:x1]; kind='NATIVE_PIXEL_CROP';resampling='NONE'
    else:
        selected=samples;kind='FULL_FIELD';resampling='BOX_AFTER_DISPLAY_CURVE'
    x=np.clip(selected,0,1);m=c['midtones']
    mapped=((m-1)*x)/((2*m-1)*x-m)
    pixels=np.rint(np.clip(mapped,0,1)*255).astype(np.uint8)
    im=Image.fromarray(pixels[:,:,0] if channels==1 else pixels)
    if region is None:
        scale=min(1,512/max(im.size));size=tuple(max(1,round(n*scale)) for n in im.size)
        if im.size!=size:im=im.resize(size,Image.Resampling.BOX)
    buffer=io.BytesIO();im.save(buffer,format='PNG',optimize=False)
    raw=buffer.getvalue()
    if len(raw)>1024*1024:raise ValueError('PREVIEW_SIZE')
    return raw,{'version':VERSION,'kind':kind,'sourceGeometry':[w,h,channels],
        'displayGeometry':list(im.size),'region':region,'displayCurve':dict(c),
        'resampling':resampling,'encoding':'PNG_UINT8','sha256':hashlib.sha256(raw).hexdigest(),
        'scientificPixelData':False,'acceptance':'NOT_ESTABLISHED'}

def provider_image(raw,expected_sha256,*,expected_geometry=None,expected_channels=None):
    """Re-encode bounded pixels to strip metadata before any provider request."""
    if not isinstance(raw,bytes) or not 0<len(raw)<=1024*1024 or hashlib.sha256(raw).hexdigest()!=expected_sha256:
        raise ValueError('PREVIEW_ASSET_BINDING')
    with Image.open(io.BytesIO(raw)) as im:
        if im.format!='PNG' or im.mode not in ('L','RGB') or getattr(im,'n_frames',1)!=1 or not all(1<=n<=512 for n in im.size):raise ValueError('PREVIEW_FORMAT')
        if expected_geometry is not None and (not isinstance(expected_geometry,(list,tuple)) or
                len(expected_geometry)!=2 or not all(type(v) is int for v in expected_geometry) or
                tuple(expected_geometry)!=im.size):raise ValueError('PREVIEW_GEOMETRY_BINDING')
        if expected_channels is not None and (type(expected_channels) is not int or
                expected_channels not in (1,3) or im.mode!=('L' if expected_channels==1 else 'RGB')):
            raise ValueError('PREVIEW_CHANNEL_BINDING')
        im.load();clean=Image.frombytes(im.mode,im.size,im.tobytes())
    out=io.BytesIO();clean.save(out,format='PNG')
    return {'type':'input_image','image_url':'data:image/png;base64,'+base64.b64encode(out.getvalue()).decode('ascii'),'detail':'low'}
