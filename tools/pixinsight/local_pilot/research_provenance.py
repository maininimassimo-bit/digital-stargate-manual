"""Native SPCC evidence belongs to its exact ancestor, never to a later fit."""
import copy
from .broker import require
from .intake import sha
from . import research_contract as contract


def calibration_lineage(state):
    nodes=state['checkpoints'];key=state['selectedId'];chain=[];seen=set();calibration=None
    while key is not None:
        require(contract.checkpoint_id(key) and key in nodes and key not in seen and
                len(chain) <= contract.MAX_TRIALS, 'RESEARCH_LINEAGE_CHAIN')
        node=nodes[key]
        require(node['id'] == key and node.get('verified') is True, 'RESEARCH_LINEAGE_VERIFIED')
        seen.add(key)
        chain.append({k:copy.deepcopy(node[k]) for k in ('id','parentId','step','domain')})
        if node.get('step',{} ) and node['step']['process'] == 'SPCC':
            photo=node.get('photometry');digest=node.get('photometricReceiptSha256')
            require(calibration is None and isinstance(photo,dict) and contract.digest(digest) and
                    sha(photo) == digest and photo.get('status') == 'NATIVE_FIT_INSPECTABLE' and
                    photo.get('profileSha256') == state['instrument']['profileSha256'] and
                    photo.get('whiteReferenceInsideFitRange') ==
                        'INSIDE_EXPORTED_RANGE_FROM_ROUNDED_NATIVE_PRODUCTS', 'RESEARCH_LINEAGE_SPCC_RECEIPT')
            calibration={'checkpointId':key,'receiptSha256':digest,'nativeFit':copy.deepcopy(photo),
                         'scope':'RGB_LINEAR_AT_CALIBRATION_ANCESTOR'}
        key=node['parentId']
    require(chain and chain[-1]['id'] == 'CP000', 'RESEARCH_LINEAGE_ROOT')
    chain.reverse()
    return {'chain':chain,'calibration':calibration,
            'status':'VERIFIED_NATIVE_SPCC_ANCESTOR' if calibration else 'NO_NATIVE_SPCC_IN_SELECTED_ANCESTRY',
            'downstreamPhotometricValidity':'NOT_ESTABLISHED','scientificAcceptance':'NOT_ESTABLISHED',
            'interpretation':'A null local fit at a later checkpoint is not missing ancestral SPCC. '
                'Denoise, stretch, LRGB fusion and saturation do not rerun SPCC or certify preserved photometric ratios.'}
