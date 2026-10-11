import copy
import unittest
from . import adaptive_catalog as catalog

def facts():
    return {'domain':'LINEAR_ATTESTED','sourceSha256':'a'*64,'recordSha256':'b'*64,
        **{key:'VERIFIED' for key in ('runtime','registration','backgroundROI','stellarPSF')},
        'mask':'NOT_ESTABLISHED'}

def graph():
    return {'catalog':catalog.VERSION,'catalogSha256':catalog.fingerprint(),'branch':'DIRECT','workingSampling':'ORIGINAL',
        'steps':[{'process':'STRETCH','parameters':{'targetBackground':.08}},
                 {'process':'MASK_BUILD','parameters':{'maskLow':.1,'maskHigh':.6}},
                 {'process':'LOCAL_CONTRAST','parameters':{'contrastLarge':.2,'contrastSmall':.2}}],
        'rationale':'Proteggere il fondo dopo lo stretch','limitations':'Verificare realmente la maschera'}

def decision(action='CONTINUE',step=None):
    return {'action':action,'bindingSha256':'c'*64,'nextStep':step,
            'rationale':'Confronto conservativo','limitations':'Nessuna accettazione scientifica automatica'}

class CheckpointControlTests(unittest.TestCase):
    def test_planned_mask_does_not_promote_physical_facts(self):
        initial=facts();before=copy.deepcopy(initial)
        catalog.validate_graph(graph(),'LRGB',initial);self.assertEqual(initial,before)
        current={**initial,'domain':'NONLINEAR_ATTESTED'}
        with self.assertRaisesRegex(ValueError,'PHYSICAL_FACT'):catalog.validate_dispatch(graph()['steps'][2],'LRGB',current)
        current['mask']='VERIFIED';catalog.validate_dispatch(graph()['steps'][2],'LRGB',current)
    def test_mask_build_requires_nonlinear_domain_and_valid_range(self):
        with self.assertRaisesRegex(ValueError,'DOMAIN'):catalog.validate_dispatch(graph()['steps'][1],'LRGB',facts())
        invalid=copy.deepcopy(graph()['steps'][1]);invalid['parameters']['maskHigh']=.12
        with self.assertRaisesRegex(ValueError,'MASK_RANGE'):catalog.validate_step(invalid)
    def test_only_next_step_parameters_can_be_adjusted(self):
        current={**facts(),'domain':'NONLINEAR_ATTESTED'}
        step=copy.deepcopy(graph()['steps'][1]);step['parameters']['maskLow']=.08
        result=catalog.validate_next_decision(decision(step=step),'c'*64,graph(),'LRGB',facts(),current,1)
        self.assertEqual(result['nextStep']['parameters']['maskLow'],.08)
        with self.assertRaisesRegex(ValueError,'NEXT_STEP_ONLY'):
            catalog.validate_next_decision(decision(step=graph()['steps'][0]),'c'*64,graph(),'LRGB',facts(),current,1)
    def test_stale_binding_source_change_and_invalid_prefix_rejected(self):
        current={**facts(),'domain':'NONLINEAR_ATTESTED'}
        variants=[('d'*64,current,1),('c'*64,{**current,'sourceSha256':'d'*64},1),('c'*64,current,True),('c'*64,current,0)]
        for binding,modified,completed in variants:
            with self.subTest(completed=completed),self.assertRaises(ValueError):
                catalog.validate_next_decision(decision(step=graph()['steps'][1]),binding,graph(),'LRGB',facts(),modified,completed)
    def test_completion_requires_full_prefix_and_runtime(self):
        current={**facts(),'domain':'NONLINEAR_ATTESTED','mask':'VERIFIED'}
        value=decision('COMPLETE_FOR_REVIEW')
        catalog.validate_next_decision(value,'c'*64,graph(),'LRGB',facts(),current,3)
        for completed,modified in ((2,current),(3,{**current,'runtime':'NOT_ESTABLISHED'}),(3,facts())):
            with self.subTest(completed=completed),self.assertRaises(ValueError):
                catalog.validate_next_decision(value,'c'*64,graph(),'LRGB',facts(),modified,completed)
    def test_unknown_domain_can_stop_but_cannot_continue(self):
        current={**facts(),'domain':'NOT_ESTABLISHED'}
        catalog.validate_next_decision(decision('STOP_FOR_REVIEW'),'c'*64,graph(),'LRGB',facts(),current,1)
        with self.assertRaises(ValueError):
            catalog.validate_next_decision(decision(step=graph()['steps'][1]),'c'*64,graph(),'LRGB',facts(),current,1)
    def test_optical_correction_requires_linear_psf_and_precedes_color(self):
        value=graph();value['steps']=[{'process':'OPTICAL_CORRECT','parameters':{}},{'process':'COLOR','parameters':{}}]
        catalog.validate_graph(value,'LRGB',facts())
        value['steps'].reverse()
        with self.assertRaisesRegex(ValueError,'ORDER'):catalog.validate_graph(value,'LRGB',facts())
        with self.assertRaisesRegex(ValueError,'PHYSICAL_FACT'):
            catalog.validate_dispatch({'process':'OPTICAL_CORRECT','parameters':{}},'LRGB',{**facts(),'stellarPSF':'NOT_ESTABLISHED'})

if __name__=='__main__':unittest.main()
