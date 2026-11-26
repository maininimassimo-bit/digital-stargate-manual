"""Measure ACS ratio sensitivity to sampling of the same Gaia XP spectra."""
from contextlib import redirect_stdout,redirect_stderr
from hashlib import sha256
import io,json
from pathlib import Path
import runpy
from statistics import mean
import sys

PIN="a0ae44dcb5d1fb4d1fa3a41d99b46029fd65198b1ed90667c957355036ae8660"


def require(ok,label):
    if not ok:
        raise ValueError(label)


def pinned(path,pin):
    raw=path.read_bytes()
    require(sha256(raw).hexdigest()==pin,"Pinned input differs")
    return raw


def main():
    spec, runtime, wheels_manifest, continuo, sampled_path, photometry, acs_path, gd71, gd153, out=map(Path,sys.argv[1:])
    plan=json.loads(pinned(spec,PIN))
    pinned(wheels_manifest,plan["wheelsSha256"])
    sys.path.insert(0,str(runtime))
    events=[]
    def offline(event,args):
        if event in {"socket.connect","socket.getaddrinfo","socket.gethostbyname","socket.sendto"}:
            events.append(event)
            raise RuntimeError("The numerical run forbids network requests")
    sys.addaudithook(offline)
    import numpy as np
    import gaiaxpy
    from astropy.io import fits
    from gaiaxpy import calibrate
    require(gaiaxpy.__version__==plan["packageVersion"] and
            Path(gaiaxpy.__file__).resolve().is_relative_to(runtime.resolve()),"Wrong GaiaXPy runtime")
    sampled=json.loads(pinned(sampled_path,plan["sampledSha256"]))
    pplan=json.loads(pinned(photometry/"protocollo.json",plan["photometryProtocolSha256"]))
    prev=json.loads(pinned(photometry/"riscontro.json",plan["photometryReceiptSha256"]))
    env={"__name__":"pinned_acs_integral"}
    exec(compile(pinned(photometry/"verifica.py",plan["integrationRunnerSha256"]),"pinned_acs_integral.py","exec"),env)
    integral=env["integral"]
    acs=json.loads(pinned(acs_path,pplan["acsProtocolSha256"]))
    helper=Path(acs["helper"])
    pinned(helper,acs["helperSha256"])
    throughput=runpy.run_path(str(helper))["throughput"]
    capture=Path(acs["capture"])
    verified=json.loads(pinned(capture,acs["captureSha256"]))
    require(verified["routes"]==acs["routes"],"ACS chain differs")
    for name in {n for band in acs["routes"].values() for n in band}:
        pinned(capture.parent/name,verified["components"][name]["sha256"])
    payload={}
    for star, exposures in (("GD71",gd71),("GD153",gd153)):
        path=continuo/(star+"-continuous-row.csv")
        pinned(path,plan["continuousRows"][star])
        records=json.loads(pinned(exposures,pplan["targets"][star]["exposures"]))["rows"]
        require(len(records)==6,"Missing ACS exposure")
        expected=sampled["spectra"][star]
        archived=np.array(expected["flux"])
        spectra={"published2nm":(np.array(sampled["gridNm"],dtype=float),archived)}
        errors={}
        low,high=plan["boundsNm"]
        for step in (None,*plan["fineStepsNm"]):
            grid=None if step is None else np.arange(low,high+step/2,step)
            with redirect_stdout(io.StringIO()),redirect_stderr(io.StringIO()):
                values,out_grid=calibrate(path,sampling=grid,truncation=False,save_file=False,with_correlation=False,
                                          release="dr3",disable_info=True)
            label="runtimeDefault2nm" if step is None else f"custom{step:g}nm"
            require(len(values)==1 and str(values["source_id"].iloc[0])==expected["sourceId"],"Spectrum identity differs")
            out_flux=np.array(values["flux"].iloc[0])
            out_error=np.array(values["flux_error"].iloc[0])
            require(out_flux.shape==out_error.shape==out_grid.shape and np.isfinite(out_flux).all()
                    and np.isfinite(out_error).all() and (out_error>0).all(),"Invalid runtime spectrum")
            if step is None:
                require(np.array_equal(out_grid,spectra["published2nm"][0]),"Default grid differs")
                errors={key:float(np.max(abs(values/np.array(expected[field])-1)))
                        for key,values,field in (("flux",out_flux,"flux"),("error",out_error,"fluxError"))}
                require(max(errors.values())<=plan["defaultReplayTolerance"],f"Default replay exceeds tolerance {errors}")
            else:
                require(np.array_equal(out_grid,grid),"Custom grid differs")
            spectra[label]= (out_grid,out_flux)
        measures={}
        for row in records:
            throughput.__globals__["EPOCH"]=row["startMjd"]
            path=acs["routes"][row["band"].lower()]
            chain=[throughput(np,fits,item) for item in path]
            fresh={}
            for label,(grid,flux) in spectra.items():
                values=[integral(chain,grid*10,[flux*pplan["gaiaToFlamFactor"]],order)[0][0]
                        for order in pplan["quadratureOrders"]]
                np.testing.assert_allclose(*values,rtol=1e-9,atol=0)
                fresh[label]=values[0]
            measures.setdefault(row["band"],[]).append(fresh)
        require(set(measures)==set(pplan["bands"]) and all(len(items)==2 for items in measures.values()),"Unexpected bands")
        means={name:{label:float(mean(row[label] for row in items)) for label in spectra}
               for name,items in measures.items()}
        comparison={}
        for ratio in pplan["ratios"]:
            a,b=ratio.split("/")
            observed=prev["comparisons"][star]["ratios"][ratio]
            computed={label:means[a][label]/means[b][label] for label in spectra}
            anchor=computed["published2nm"]
            np.testing.assert_allclose(anchor,observed["gaiaFullGridRate"],rtol=1e-10,atol=0)
            finest=computed["custom0.25nm"]
            comparison[ratio]=dict(ratios=computed, finestToPublishedRatio=finest/anchor-1,
                                   stepQuarterToHalfRatio=finest/computed["custom0.5nm"]-1,
                                   acsApertureToFinest=observed["observedApertureRate"]/finest-1,
                                   calspecFullToFinest=observed["calspecFullRate"]/finest-1)
        payload[star]=dict(defaultReplayMaximumRelative=errors,ratios=comparison)
    require(not events,"Library attempted network access")
    report=dict(schema="BKL046_GAIAXP_ACS_DENSE_SAMPLING_RESULT_V1",protocolSha256=PIN,targets=payload,
                gaiaxpyVersion=gaiaxpy.__version__,modelOfPhysicalLineSpreadFunctionExecuted=False,
                pythonNetworkConnectionAuditEvents=0,scientificClosures=0,nativeExecutions=0)
    with out.open("x",encoding="utf-8",newline="\n") as output:
        json.dump(report,output,indent=2,sort_keys=True,allow_nan=False)
        output.write("\n")


if __name__=="__main__":
    main()
