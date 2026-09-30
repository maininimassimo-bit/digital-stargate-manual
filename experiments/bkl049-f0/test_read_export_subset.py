"""Synthetic-only tests of the F0 nonexecuting subset reader."""
import json
import unittest
from read_export_subset import parse_export, safe_summary, Unsupported, MAX_BYTES

SAMPLE = r"""// Total time: 1 s
var Root = new ProcessContainer;
var Group = new ProcessContainer;
/* fake call inside a comment: executeGlobal(); */
var A = new PixelMath;
A.expression = "doNotExecute();\n" + "synthetic value";
A.amount = -0.120000;
A.table = [[true, 1e-7], [false, null]];
A.mode = PixelMath.SameAsTarget;
Group.add(A);
var B = new PixelMath;
B.expression = "$T";
Group.add(B);
Root.add(Group);
Root.setMask(0, "SYNTHETIC_PRIVATE_MASK");
Root.invertMask(0);
"""

class ReaderTests(unittest.TestCase):
    def reject(self, source, code=None):
        with self.assertRaises(Unsupported) as caught:
            parse_export(source)
        if code:
            self.assertEqual(caught.exception.code, code)

    def test_nested_repeated_types_and_order(self):
        r = parse_export(SAMPLE)
        self.assertEqual(r['instances']['Root']['children'], ['Group'])
        self.assertEqual(r['instances']['Group']['children'], ['A', 'B'])
        self.assertEqual(safe_summary(r)['processInstanceCount'], 2)

    def test_strings_are_data_not_code(self):
        r = parse_export(SAMPLE)
        self.assertEqual(r['instances']['A']['parameters']['expression'], 'doNotExecute();\nsynthetic value')
        self.assertEqual(r['executionEvidence'], 'NOT_ESTABLISHED')

    def test_preserves_numbers_arrays_enums(self):
        p = parse_export(SAMPLE)['instances']['A']['parameters']
        self.assertEqual(p['amount'], {'kind': 'number', 'literal': '-0.120000'})
        self.assertEqual(p['table'][0][1]['literal'], '1e-7')
        self.assertIsNone(p['table'][1][1])
        self.assertEqual(p['mode']['owner'], 'PixelMath')

    def test_mask_operations_preserve_local_index(self):
        commands = parse_export(SAMPLE)['instances']['Root']['maskCommands']
        self.assertEqual([c['operation'] for c in commands], ['setMask', 'invertMask'])
        self.assertEqual([c['index'] for c in commands], [0, 0])

    def test_summary_omits_values(self):
        s = json.dumps(safe_summary(parse_export(SAMPLE)))
        self.assertNotIn('SYNTHETIC_PRIVATE_MASK', s)
        self.assertNotIn('doNotExecute', s)
        self.assertEqual(json.loads(s)['workflowCompleteness'], 'UNAVAILABLE')

    def test_source_spans_cover_statements(self):
        r = parse_export(SAMPLE)
        for statement in r['statements']:
            start, end = statement['sourceSpan']
            self.assertTrue(SAMPLE[start:end].endswith(';'))
        self.assertEqual(len(r['commentSpans']), 2)

    def test_single_instance_and_empty_constructor(self):
        self.assertEqual(parse_export('var P = new Synthetic(); P.a = "";')['root'], 'P')

    def test_execution_call_rejected(self):
        self.reject('var P = new PixelMath; P.executeGlobal();', 'UNSUPPORTED_CALL')

    def test_statement_injection_rejected(self):
        self.reject('var P = new PixelMath; fetch("synthetic");')

    def test_loop_rejected(self):
        self.reject('while(true) {}')

    def test_arithmetic_outside_string_rejected(self):
        self.reject('var P = new PixelMath; P.value = 1 + 2;')

    def test_duplicate_declaration_rejected(self):
        self.reject('var P = new PixelMath; var P = new SCNR;', 'DUPLICATE_VARIABLE')

    def test_duplicate_parameter_rejected(self):
        self.reject('var P = new PixelMath; P.a=1; P.a=2;', 'DUPLICATE_PROPERTY')

    def test_unknown_child_rejected(self):
        self.reject('var P = new ProcessContainer; P.add(X);', 'UNKNOWN_CHILD')

    def test_cycle_rejected(self):
        self.reject('var P = new ProcessContainer; var Q = new ProcessContainer; P.add(Q); Q.add(P);')
        self.reject('var P = new ProcessContainer; P.add(P);', 'CONTAINER_CYCLE')

    def test_reuse_rejected(self):
        self.reject('var P = new ProcessContainer; var Q = new SCNR; P.add(Q); P.add(Q);', 'REUSED_INSTANCE')

    def test_index_rejected(self):
        self.reject('var P = new ProcessContainer; P.setMask(0,"x");', 'MASK_INDEX_RANGE')

    def test_post_attachment_mutation_rejected(self):
        self.reject('var P = new ProcessContainer; var Q = new X; P.add(Q); Q.a=1;', 'POST_ATTACHMENT_MUTATION')

    def test_large_mask_index_rejected(self):
        self.reject('var P = new ProcessContainer; P.invertMask('+ '9'*5000 +');', 'INVALID_INDEX')

    def test_instance_bound(self):
        self.reject(''.join(f'var P{i}=new X;' for i in range(513)), 'INSTANCE_LIMIT')

    def test_token_bound(self):
        self.reject('; '*200001, 'TOKEN_LIMIT')

    def test_container_depth_bound(self):
        source = ''.join(f'var P{i}=new ProcessContainer;' for i in range(35))
        source += ''.join(f'P{i}.add(P{i+1});' for i in range(33,-1,-1))
        self.reject(source, 'CONTAINER_DEPTH_LIMIT')

    def test_size_bound(self):
        self.reject(' '*(MAX_BYTES+1), 'SIZE_LIMIT')

    def test_value_depth_bound(self):
        self.reject('var P = new X; P.a='+'['*35+'0'+']'*35+';', 'VALUE_DEPTH_LIMIT')

    def test_unknown_escape_rejected(self):
        self.reject(r'var P = new X; P.a="\x41";', 'UNSUPPORTED_STRING_ESCAPE')

    def test_unclosed_string_or_comment_rejected(self):
        self.reject('var P = new X; P.a="unfinished')
        self.reject('var P = new X; /* unfinished')

    def test_ambiguous_roots_rejected(self):
        self.reject('var P = new X; var Q = new X;', 'ROOT_COUNT')

if __name__ == '__main__':
    unittest.main()
