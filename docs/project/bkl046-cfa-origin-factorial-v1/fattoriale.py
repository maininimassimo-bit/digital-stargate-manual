from hashlib import sha256
from itertools import combinations,product
import json
from pathlib import Path
import re
import sys

root, prior, controls, comparator, dependencies, output = map(Path,sys.argv[1:])
raw=(root/"protocollo.json").read_bytes()
pin=sha256(raw).hexdigest()
assert pin=="74a872c4d06b8447557519bde7c4064fb24d029a9f1fe38540c337e40f8ced5a"
p=json.loads(raw)
parent_report=(prior/"riscontro.json").read_bytes()
assert sha256(parent_report).hexdigest()==p["priorReport"]
program=prior/"margini.py"
program_raw=program.read_bytes()
assert sha256(program_raw).hexdigest()==p["priorProgram"]==json.loads(parent_report)["programSha256"]
prefix, boundary, _ = program_raw.decode().partition("\ngeometry={}\n")
assert boundary
namespace={"__file__":str(program)}
sys.argv=[str(program),*map(str,(prior,controls,comparator,dependencies,output/"riscontro.json"))]
exec(compile(prefix,str(program),"exec"),namespace)
render, source, compare, read, oracles, fits, np = (namespace[k] for k in (
    "render","source","difference","read","oracles","fits","np"))
output.mkdir()
samples=output/"xdrz"
samples.mkdir()
reference_dir=output/"oracoli"
reference_dir.mkdir()
matrices={m:[source(label,m) for label in "abc"] for m in p["matrixVariants"]}
maps={}
for matrix,origin in product(p["matrixVariants"],p["declaredOrigins"]):
    key=(matrix,origin)
    maps[key]=render([(M,(origin,origin),data) for M,_,data in matrices[matrix]],True)
    for label in "abc":
        raw_file=read(f"shear-{label}-{matrix}.xdrz")
        tag=f'<AlignmentOrigin x="{origin:.1f}" y="{origin:.1f}" />'.encode()
        crossed,count=re.subn(rb'<AlignmentOrigin x="[0-9.]+" y="[0-9.]+" />',tag,raw_file)
        assert count==1
        (samples/f"shear-{label}-{matrix}-origin{origin:.1f}.xdrz").write_bytes(crossed)

library={
    "baseline":oracles["shear"],
    "half-matrix-as-zero":maps[("edge05",0)],
    "zero-matrix-as-half":maps[("center0",.5)]
}
assert compare(maps[("center0",0)],library["baseline"])["acceptedByExactComparator"]
assert compare(maps[("edge05",.5)],library["baseline"])["acceptedByExactComparator"]
separation=[]
for left,right in combinations(library,2):
    stats=compare(library[left],library[right])
    assert not stats["acceptedByExactComparator"]
    separation.append({"left":left,"right":right,**stats})
for label,arrays in library.items():
    for kind,data in zip(("rgb","weight"),arrays,strict=True):
        fits.PrimaryHDU(data).writeto(reference_dir/f"{label}-{kind}.fits")

rows=[]
signatures={m:[] for m in p["hypotheses"]}
for matrix,declared in product(p["matrixVariants"],p["declaredOrigins"]):
    observations={}
    for name,applied in zip(p["hypotheses"],(declared,0,.5),strict=True):
        predicted=maps[(matrix,applied)]
        candidates=[n for n,reference in library.items() if compare(predicted,reference)["acceptedByExactComparator"]]
        assert len(candidates)==1
        observations[name]=candidates[0]
        signatures[name].append(candidates[0])
    rows.append({"matrix":matrix,"declaredOrigin":declared,"predictedMapClass":observations})
assert len({tuple(v) for v in signatures.values()})==len(signatures)
members={f.relative_to(output).as_posix():sha256(f.read_bytes()).hexdigest()
         for f in sorted(output.glob("*/*"))}
report={"schema":"BKL046_CFA_ORIGIN_FACTORIAL_V1","protocolSha256":pin,"rows":rows,
        "predictedSignatures":signatures,"mapClassSeparation":separation,"fixtureSha256":members,
        "programSha256":sha256(Path(__file__).read_bytes()).hexdigest(),
        "nativeExecutions":0,"scientificClosures":0,"frozenV4PlanModified":False}
(output/"riscontro.json").write_bytes((json.dumps(report,indent=2,sort_keys=True)+"\n").encode())
print(json.dumps(signatures))
