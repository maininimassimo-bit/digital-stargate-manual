import json
import re
import unittest
from .scientific_knowledge import packet, instructions
from .adaptive_provider import AdaptiveProvider
from .checkpoint_provider import CheckpointProvider
from .test_adaptive_provider import inputs, response, CONSENTS
from . import test_checkpoint_provider as checkpoint


class ScientificKnowledgeTests(unittest.TestCase):
    def test_portable_guidance_contains_scientific_limits_without_private_paths(self):
        value, digest = packet()
        text, same = instructions(digest)
        self.assertEqual(digest, same)
        self.assertEqual(value['authority'], 'GUIDANCE_ONLY_NEVER_CAPABILITIES_FACTS_OR_ACCEPTANCE')
        self.assertIsNone(re.search(r'(?i)\b[a-z]:[\\/]|\\\\', text))
        for term in ('BlurXTerminator', 'SPCC', 'History', 'SNR', 'fotometrico', 'ritagli'):
            self.assertIn(term, text)
        self.assertLess(len(text), 32768)

    def test_initial_paid_payload_and_receipt_identify_the_pack(self):
        calls = []
        provider = AdaptiveProvider('mock', 'gpt-6-luna', send=lambda p: calls.append(p) or response())
        _, receipt = provider.generate_initial(*inputs(), **CONSENTS)
        self.assertEqual(receipt['scientificKnowledgeSha256'], packet()[1])
        self.assertIn('Non creare strutture astronomiche', calls[0]['instructions'])
        self.assertIn('do not enable them', calls[0]['instructions'])
        self.assertNotIn('sourceSha256', json.dumps(calls[0]))

    def test_checkpoint_gets_same_scientific_rules(self):
        calls = []
        provider = CheckpointProvider('mock', 'gpt-6-luna', send=lambda p: calls.append(p) or checkpoint.response())
        _, receipt = provider.generate_checkpoint(*checkpoint.inputs(), **CONSENTS,
                                                  scientific_knowledge_sha256=packet()[1])
        self.assertEqual(receipt['scientificKnowledgeSha256'], packet()[1])
        self.assertIn('Conservare anche tentativi falliti', calls[0]['instructions'])

    def test_changed_pack_blocks_send_and_old_checkpoint_remains_legacy(self):
        calls = []
        provider = CheckpointProvider('mock', 'gpt-6-luna', send=lambda p: calls.append(p) or checkpoint.response())
        with self.assertRaisesRegex(ValueError, 'KNOWLEDGE_VERSION_CHANGED'):
            provider.generate_checkpoint(*checkpoint.inputs(), **CONSENTS, scientific_knowledge_sha256='0'*64)
        self.assertEqual(calls, [])
        _, receipt = provider.generate_checkpoint(*checkpoint.inputs(), **CONSENTS)
        self.assertNotIn('scientificKnowledgeSha256', receipt)
        self.assertNotIn('Non creare strutture astronomiche', calls[0]['instructions'])


if __name__ == '__main__':
    unittest.main()
