"""Compare corrections learned on one GRW70 UVIS chip against the other."""
import argparse
from hashlib import file_digest, sha256
import json
from math import isclose, isfinite
from pathlib import Path
from statistics import median
from zipfile import ZipFile

PIN = "9b77a430b55aea1dea07dcc556ccf2d7d7899e4d6ba65fb34963b73d8553643f"


def need(ok, why):
    if not ok:
        raise ValueError(why)


def key(row):
    return row["batch"],row["chip"]


def terms(row):
    colors=row["colors"]
    change={c:v-colors["5"][c] for c,v in colors["10"].items()}
    need(set(change)==set(row["apertureChangeMillimag"]) and len(change)==3
         and all(isfinite(value) and isclose(value,row["apertureChangeMillimag"][c],abs_tol=1e-9)
                 for c,value in change.items()), "Archived changes differ")
    return change


def fit_test(train, evaluation, minimum):
    need(len(train)>=minimum and bool(evaluation) and
         {r["visit"] for r in train}.isdisjoint({r["visit"] for r in evaluation}),"Visit split differs")
    train_chips={r["chip"] for r in train}
    test_chips={r["chip"] for r in evaluation}
    need(len(train_chips)==len(test_chips)==1, "Chip identity ambiguous")
    profiles=[terms(row) for row in train]
    correction={c:median(row[c] for row in profiles) for c in profiles[0]}
    envelope={c:[min(row[c] for row in profiles),max(row[c] for row in profiles)] for c in correction}
    records=[]
    for row in evaluation:
        observed=terms(row)
        need(set(observed)==set(correction),"Color identity differs")
        records.append(dict(visit=row["visit"], observed=observed,
                            errorWithoutCorrection=observed,
                            errorWithCorrection={c:v-correction[c] for c,v in observed.items()},
                            insideTrainingEnvelope={c:lo <= observed[c] <= hi for c,(lo,hi) in envelope.items()}))
    aggregate={}
    for color in correction:
        before=[abs(r["errorWithoutCorrection"][color]) for r in records]
        after=[abs(r["errorWithCorrection"][color]) for r in records]
        aggregate[color]=dict(medianWithout=median(before),medianWith=median(after),maximumWith=max(after),
                              improved=sum(b<a for a,b in zip(before,after,strict=True)),
                              insideTrainingEnvelope=sum(r["insideTrainingEnvelope"][color] for r in records))
    return dict(trainingChip=train_chips.pop(),testChip=test_chips.pop(),
                trainingVisits=[row["visit"] for row in train],trainingMedian=correction,
                trainingEnvelope=envelope,tests=records,summary=aggregate)


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    for arg in ("protocol","archive","report"):
        cli.add_argument(arg,type=Path)
    a=cli.parse_args()
    raw=a.protocol.read_bytes()
    need(sha256(raw).hexdigest()==PIN,"Protocol changed")
    p=json.loads(raw)
    pin,name,sub=p["input"]
    with a.archive.open("rb") as stream:
        need(file_digest(stream,"sha256").hexdigest()==pin,"Source ZIP changed")
        with ZipFile(stream) as zipfile:
            need(zipfile.namelist().count(name)==1,"Report member differs")
            raw=zipfile.read(name)
    need(sha256(raw).hexdigest()==sub,"Archived result changed")
    prior=json.loads(raw)
    visits=prior["acceptedCombinedVisits"]
    need(len(visits)==len({r["visit"] for r in visits})==7,"Visit coverage differs")
    need(not prior["astrometricFieldTieVerified"] and prior["scientificClosures"]==prior["nativeExecutions"]==0,
         "Source scope differs")
    train2=[r for r in visits if key(r)==(p["training2"],2)]
    reserve2=[r for r in visits if key(r)==(p["evaluation"],2)]
    reserve1=[r for r in visits if key(r)==(p["evaluation"],1)]
    need((len(train2),len(reserve2),len(reserve1))==(2,3,2),"Batch coverage differs")
    n=p["trainCountMinimum"]
    checks=dict(sameChipReference=fit_test(train2,reserve2,n),
                transferUVIS2ToUVIS1=fit_test(train2,reserve1,n),
                reverseSensitivity=fit_test(reserve1,reserve2,n))
    for c,row in checks["sameChipReference"]["summary"].items():
        known=prior["reservedSummary"][c]
        need(isclose(row["medianWith"],known["medianAbsoluteError"],abs_tol=1e-10)
             and isclose(row["medianWithout"],known["medianAbsoluteUncorrected"],abs_tol=1e-10)
             and row["improved"]==known["improved"],"Same-chip comparison differs from archive")
    output=dict(schema=p["schema"]+"_RESULT",programSha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                protocolSha256=PIN,results=checks,distinctVisits=len(visits),distinctStars=1,
                causalChipEffectVerified=False,scientificClosures=0,nativeExecutions=0)
    with a.report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(output,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()