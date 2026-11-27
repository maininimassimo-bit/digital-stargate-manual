"""Deterministic synthetic FITS controls for a future, separately admitted ImageAnalysis run."""
from array import array
import hashlib
import json
import math
from pathlib import Path
import random
import statistics as st
import struct
import sys

SIDE = 192
LEVEL = 1200
STARS = [(18+30*i+(.25 if j%2 else .5),18+30*j+.25*(i%3),2200+160*(i+2*j))
         for j in range(6) for i in range(6)]
PALETTES = {
    'compact': [-42,-28,-14,-7,0,0,7,14,28,42],
    'tailed': [-112,-42,-8,-3,0,0,3,8,42,112],
}


def card(key, val):
    return (key.ljust(8) + '= ' + str(val).rjust(20)).ljust(80).encode('ascii')


def pad(raw, value):
    return raw + value*((-len(raw))%2880)


def fits(pixels):
    header = b''.join(card(key,val) for key,val in
        [('SIMPLE','T'),('BITPIX',16),('NAXIS',2),('NAXIS1',SIDE),('NAXIS2',SIDE),('BSCALE',1),('BZERO',32768)])
    raw = struct.pack('>'+'h'*len(pixels),*(sample-32768 for sample in pixels))
    return pad(header+b'END'.ljust(80),b' ') + pad(raw,b'\0')


def reread(raw):
    cards = [raw[offset:offset+80].decode('ascii') for offset in range(0,2880,80)]
    keys = {row[:8].strip():row[10:].strip() for row in cards if row[8:10]=='= '}
    expected = dict(SIMPLE='T',BITPIX='16',NAXIS='2',NAXIS1=str(SIDE),NAXIS2=str(SIDE),BSCALE='1',BZERO='32768')
    assert keys==expected and raw[560:563]==b'END' and len(raw)%2880==0
    words = array('h',raw[2880:2880+2*SIDE*SIDE])
    assert words.itemsize==2
    if sys.byteorder=='little':
        words.byteswap()
    assert len(words)==SIDE*SIDE
    return [x+32768 for x in words]


def star_field(sigma):
    values = [LEVEL]*(SIDE*SIDE)
    background = [True]*len(values)
    for x0,y0,amplitude in STARS:
        for y in range(math.floor(y0)-12, math.floor(y0)+13):
            for x in range(math.floor(x0)-12, math.floor(x0)+13):
                distance2 = (x-x0)**2+(y-y0)**2
                if distance2<=121:
                    index = y*SIDE+x
                    assert background[index]
                    background[index] = False
                    values[index] += round(amplitude*math.exp(-distance2/(2*sigma*sigma))*(1.4/sigma)**2)
    return values, background


def samples(indices,palette,correlated):
    pool = [palette[i%len(palette)] for i in range(len(indices))]
    if correlated:
        # The same multiset, ordered into ten vertical zones.
        return zip(sorted(indices,key=lambda i:(i%SIDE,i//SIDE)),sorted(pool))
    random.Random(46051).shuffle(pool)
    return zip(indices,pool)


def stats(pixels,indices):
    values=[pixels[i] for i in indices]
    mask=set(indices)
    diff=[pixels[i+1]-pixels[i] for i in indices if i%SIDE<SIDE-1 and i+1 in mask]
    median=st.median(values)
    absolute=[abs(x-median) for x in values]
    return dict(backgroundCount=len(values),median=median,sigmaPopulation=st.pstdev(values),
                medianAbsoluteDeviation=st.median(absolute),meanAbsoluteDeviation=st.mean(absolute),
                madGaussianScaled=st.median(absolute)/0.6744897501960817,
                horizontalPairSigma=st.pstdev(diff)/math.sqrt(2),
                histogramSha256=hashlib.sha256(struct.pack('>'+'H'*len(values),*sorted(values))).hexdigest())


def main(folder):
    folder.mkdir()
    records=[]
    cases=[('compact-shuffled',1.4,'compact',False),('compact-zones',1.4,'compact',True),
           ('tailed-shuffled',1.4,'tailed',False),('compact-wide-psf',2.05,'compact',False)]
    for name,sigma,palette,correlated in cases:
        pixels,mask=star_field(sigma)
        indices=[i for i,flag in enumerate(mask) if flag]
        for index,increment in samples(indices,PALETTES[palette],correlated):
            pixels[index]+=increment
        path=folder/(name+'.fits')
        path.write_bytes(fits(pixels))
        raw=path.read_bytes()
        readback=reread(raw)
        assert readback==pixels
        records.append(dict(name=path.name,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),
                            expectedStars=len(STARS),gaussianFwhmPixels=2*math.sqrt(2*math.log(2))*sigma,
                            fields=stats(readback,indices)))
    a,b,c,d=[record['fields'] for record in records]
    assert a['histogramSha256']==b['histogramSha256']==d['histogramSha256']
    assert a['horizontalPairSigma']>3*b['horizontalPairSigma']
    assert c['sigmaPopulation']>2*a['sigmaPopulation']
    assert c['medianAbsoluteDeviation']<a['medianAbsoluteDeviation']
    assert d['horizontalPairSigma']==a['horizontalPairSigma']
    summary=dict(schema='BKL046_IMAGEANALYSIS_CONTROL_INPUTS_V1',files=records,
                 pixelType='UInt16 through FITS BZERO=32768',newNativeRun=False,scientificClosures=0)
    (folder/'riscontro.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(summary))


if __name__=='__main__':
    main(Path(sys.argv[1]))
