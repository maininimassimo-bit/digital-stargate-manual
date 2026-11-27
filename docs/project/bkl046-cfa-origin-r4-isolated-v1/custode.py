from hashlib import sha256
import os
from pathlib import Path
import sys

base=Path(sys.argv[1]).resolve()
state=Path(os.environ["DSG_ORIGIN_TEST_STATE"]).resolve()
if state.parent!=base or not state.name.startswith("reg-"):
    raise ValueError("registry outside scratch")
operation="BKL046_CFA_XDRZ_ORIGIN_FACTORIAL_001"
if sys.argv[2:]!=["--milestone","BKL-046","--operation",operation,"--guardian","--identity-v2"]:
    raise ValueError("unexpected fixture command")
canonical=Path("K:/DigitalStarGate/pixinsight-coordination-20261114-r1/coordinator.py")
raw=canonical.read_bytes()
if sha256(raw).hexdigest()!="d09aab4e9e1d20841503dbd6f4a520b7a2d4b738eeb06adecd339f7cf59b2335":
    raise ValueError("guardian bytes changed")
scope={"__file__":str(canonical),"__name__":"fixture_guardian"}
exec(compile(raw,str(canonical),"exec"),scope)
with scope["original_caller"]() as live:
    sys.exit(scope["serve_bound"]("BKL-046",operation,state,lambda:[],live))
