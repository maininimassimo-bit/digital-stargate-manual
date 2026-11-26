from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
from zipfile import ZipFile

parser=ArgumentParser()
for name in ("reference","integer","two_widths","fractional","output"):
    parser.add_argument(name,type=Path)
args=parser.parse_args()

pins=dict(batch="ca95eaa73b65ec000ba7008ee8cabd9cefa16b770da1e3ad881cef0fc9c0d107",
          test="a036b6f943ba21fb86bb4e1ef8163e956279f3ae59c2a8b9d388a66cd1087360",
          integer="677460604bd564285b0571a7149f22f7ae6ea7aed27e5badc1d71b42b0474a0f",
          widthOracle="8f8523fef29f27b9625b1e4208b50165ff22bbace63211516c4decffdb1e7ee5",
          fractional="56b5901a64468d8ec2d46f9380d925be231d625bb42536e57569e80814c34432",
          fractionalZip="e6c1a6c7c4a9199e9131f824153268a6ad64f90d0b33b6edc320c802c361c733")
old_root="O:/BKL046-CFA-XDRZ-valor-zero-tre-ingressi-v1/fixture/"
frac_root="O:/BKL046-CFA-XDRZ-testimone-larghezza-v1/input/"
run_name="BKL046-CFA-XDRZ-controllo-due-depositi-runs-v1"
previous_operation="BKL046_CFA_XDRZ_WEIGHT_WINDOW_DSG_SHARED_001"
operation="BKL046_CFA_XDRZ_TWO_DROP_CONTROL_DSG_SHARED_001"


def digest(raw):
    return sha256(raw).hexdigest()


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def read(path,key):
    raw=path.read_bytes()
    require(digest(raw)==pins[key],f"Changed {path.name}")
    return raw


def emit(name,raw):
    with (args.output/name).open("xb") as out:
        out.write(raw)
    return digest(raw)


def encoded(obj):
    return (json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()


def replace(source,anchor,value):
    require(source.count(anchor)==1,f"Changed source anchor: {anchor}")
    return source.replace(anchor,value)


integer=json.loads(read(args.integer/"riscontro.json","integer"))
width=json.loads(read(args.two_widths/"riscontro.json","widthOracle"))
fractional=json.loads(read(args.fractional/"riscontro.json","fractional"))
read(args.fractional/"testimone.zip","fractionalZip")
require(fractional["archiveSha256"]==pins["fractionalZip"] and len(width["cases"])==24
        and len(fractional["floatingFitsChecks"])==6,"Invalid source coverage")
integer_inputs=[(row["id"],row["xdrz"],row["rejection"]) for row in integer["arms"]]
with ZipFile(args.fractional/"testimone.zip") as archive:
    require(archive.testzip() is None and all(digest(archive.read(n))==h
            for n,h in fractional["sourceFiles"].items()),"Changed width witness inputs")
fractional_files=integer_inputs[0][1]
require(all(n in fractional["sourceFiles"] for n in fractional_files),"Missing fractional descriptor")
cases=[]
for tag,drop in (("070",.7),("100",1.)):
    for name,filenames,rejection in integer_inputs+[("fractional",fractional_files,False)]:
        root,group=(frac_root,"fractional") if name=="fractional" else (old_root,"integer")
        source=integer["outputs"] if group=="integer" else fractional["sourceFiles"]
        for filename in filenames:
            if group=="integer":
                require(digest((args.integer/filename).read_bytes())==source[filename],"Changed integer descriptor")
        cases.append(dict(id=tag+"-"+name,files=filenames,root=root,drop=drop,rejection=rejection,
                          group=group,xdrzSha256=[source[f] for f in filenames]))
plan_sha=emit("piano.json",encoded(dict(schema="BKL046_CFA_XDRZ_TWO_DROP_PLAN_CANDIDATE_V1",
           operation=operation,cases=cases,
           integerInputPins=integer["outputs"],fractionalInputPins=fractional["sourceFiles"],
           integerReceiptSha256=pins["integer"],integerOracleReportSha256=pins["widthOracle"],
           fractionalReceiptSha256=pins["fractional"],fractionalArchiveSha256=pins["fractionalZip"],
           scope="BATCH_COMPONENT_OFFLINE",nativeAdmissionRequested=False)))
contract_sha=emit("contratto.json",encoded(dict(schema="BKL046_CFA_TWO_DROP_BATCH_CONTRACT_V1",
                 planSha256=plan_sha,operation=operation,weightOutput="NATIVE_WEIGHT_WINDOW_UNCLASSIFIED",
                 exportsPerCase=["parameter transcript","RGB FITS","weight FITS"],caseCount=12,
                 qualification="requires width-specific numerical evidence, custody and native admission")))

batch=read(args.reference/"batch-cfa.js","batch").decode()
start=batch.index("var CFA_CONTROL_CASES")
end=batch.index("function cfaRequire")
definition={case["id"]:{k:case[k] for k in ("files","root","drop","rejection","group")} for case in cases}
batch=batch[:start]+"var CFA_CONTROL_CASES = "+json.dumps(definition,indent=2)+";\n\n"+batch[end:]
batch=batch.replace("BKL046-CFA-XDRZ-weight-window-runs-v1",run_name).replace(previous_operation,operation)
for before,after in (
    ("CFA_FIXTURE + name","scene.root + name"),
    ("dropShrink: 0.70","dropShrink: scene.drop"),
    ('   var ids = [p.integrationImageId, p.weightImageId];',
     '   cfaRequire(p.dropShrink === scene.drop, "Post-execution drop differs");\n'
     '   var ids = [p.integrationImageId, p.weightImageId];'),
    ('      weightWindowId: ids[1], weightMeaning:',
     '      effectiveDropShrink: p.dropShrink, geometryGroup: scene.group,\n'
     '      weightWindowId: ids[1], weightMeaning:'),
    ('ids.length === 5','ids.length === 12'),
    (pins["integer"],plan_sha),
    ("d71f3a4dfc2ae411f4a7da212ef3fb37e4f04149c6b70f426e32f9ed3a20a9a2",contract_sha),
    ("BKL046_CFA_XDRZ_BATCH_OUTPUT_MARKER_V1","BKL046_CFA_XDRZ_TWO_DROP_MARKER_CANDIDATE_V1"),
):
    batch=replace(batch,before,after)
emit("batch-cfa.js",batch.encode())

test=read(args.reference/"collaudo-export.cjs","test").decode()
test=test.replace("BKL046-CFA-XDRZ-weight-window-runs-v1",run_name).replace(previous_operation,operation)
for before,after in (
    ("assert.equal(contract.fixtureReceiptSha256,pin(planRaw));","assert.equal(contract.planSha256,pin(planRaw));"),
    ("const cases=JSON.parse(planRaw).arms;","const cases=JSON.parse(planRaw).cases;"),
    ("root+'/zero-reference-weight.fits'","root+'/100-zero-reference-weight.fits'"),
    ("this.inputData.map(row=>path.basename(row[1]))","this.inputData.map(row=>row[1])"),
    ("         this.integrationImageId='rgb_'+stats.calls;",
     "         if(mode==='changed-drop-after-execute') this.dropShrink=.9;\n         this.integrationImageId='rgb_'+stats.calls;"),
    ("return 'fixed effective state';","return 'effective drop '+this.dropShrink;"),
    ("fs.existsSync(path.join(path.dirname(planPath),path.basename(f)))",
     "cases.some(c=>c.files.some(name=>c.root+name===f))"),
    ("assert.equal(positive.stats.calls,5);","assert.equal(positive.stats.calls,12);"),
    ("positive.stats.removed.length,10","positive.stats.removed.length,24"),
    ("cases.map(c=>c.xdrz)","cases.map(c=>c.files.map(name=>c.root+name))"),
    ("positive.stats.lines.length,18","positive.stats.lines.length,39"),
    ('startsWith("DSG_CFA_NATIVE_")).length,7','startsWith("DSG_CFA_NATIVE_")).length,14'),
    ("assert.equal(declarations.length,5);","assert.equal(declarations.length,12);\n"
     "assert.deepEqual(declarations.map(d=>d.effectiveDropShrink),cases.map(c=>c.drop));\n"
     "assert.deepEqual(declarations.map(d=>d.geometryGroup),cases.map(c=>c.group));\n"
     "const parameters=events.filter(line=>line.startsWith('DSG_CFA_PARAMETERS ')).map(line=>JSON.parse(line.slice(19)));\n"
     "assert.deepEqual(parameters.map(p=>p.settings.dropShrink),cases.map(c=>c.drop));\n"
     "assert.deepEqual(parameters.map(p=>p.source),cases.map(c=>'effective drop '+c.drop));"),
    ("'damaged-transcript':5","'damaged-transcript':12,'changed-drop-after-execute':1"),
    ("BKL046_CFA_XDRZ_BATCH_CANDIDATE_MOCK_TEST_V1","BKL046_CFA_XDRZ_TWO_DROP_BATCH_TEST_V1"),
    ("caseEventCount:events.length","effectiveDropByCase:declarations.map(x=>x.effectiveDropShrink),caseEventCount:events.length"),
):
    test=replace(test,before,after)
emit("collaudo.cjs",test.encode())
