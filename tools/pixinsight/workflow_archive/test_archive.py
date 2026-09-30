"""Synthetic-only boundary and integrity regression tests."""
import base64
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from . import export_parser as parser
from .archive import (ArchiveError, build_packet, digest, encode, main,
                      read_regular, verify_packet, write_packet)

RAW = b'var P = new PixelMath; P.expression = "doNotExecute();"; P.n = 0.250000;'
STAMP = '2026-09-30T18:00:00Z'


class ArchiveTests(unittest.TestCase):
    def packet(self, raw=RAW):
        return build_packet(raw, 'BKL049-SYNTHETIC', STAMP)

    def test_deterministic_private_packet_preserves_exact_bytes(self):
        source = b'\xef\xbb\xbf' + RAW + b'\r\n'
        p = self.packet(source)
        self.assertEqual(encode(p), encode(self.packet(source)))
        self.assertEqual(base64.b64decode(p['source']['originalBase64']), source)
        self.assertEqual(p['source']['sha256'], digest(source))
        self.assertEqual(p['archive']['instances']['P']['parameters']['n']['literal'], '0.250000')
        self.assertEqual(p['bindingState'], 'UNLINKED')
        self.assertEqual(p['executionEvidence'], 'NOT_ESTABLISHED')
        self.assertEqual(p['publicationState'], 'PRIVATE_NOT_APPROVED')

    def test_unsupported_call_retained_without_normalized_partial(self):
        p = self.packet(RAW + b' P.executeGlobal();')
        self.assertEqual(p['extractionState'], 'UNSUPPORTED')
        self.assertIsNone(p['archive'])
        self.assertEqual(p['diagnostic']['code'], 'UNSUPPORTED_CALL')
        self.assertEqual(base64.b64decode(p['source']['originalBase64']), RAW + b' P.executeGlobal();')

    def test_invalid_utf8_is_quarantined(self):
        self.assertEqual(self.packet(b'\xff')['diagnostic']['code'], 'UTF8_INVALID')

    def test_bad_receipt_context_rejected(self):
        for identity, stamp in [('private/path', STAMP), ('BKL049-test', '2026-02-30T00:00:00Z'),
                                ('BKL049-test', 'now'), ('BKL049-test', 42)]:
            with self.subTest(identity=identity, stamp=stamp), self.assertRaises(ArchiveError):
                build_packet(RAW, identity, stamp)

    def test_roundtrip_and_external_trust_anchor(self):
        p = self.packet()
        raw = encode(p)
        self.assertEqual(verify_packet(raw, digest(raw)), p)
        with self.assertRaisesRegex(ArchiveError, 'TRUST_ANCHOR_REQUIRED'):
            verify_packet(raw, None)
        altered = raw.replace(b'0.250000', b'0.750000')
        with self.assertRaisesRegex(ArchiveError, 'PACKET_INTEGRITY'):
            verify_packet(altered, digest(raw))
        with self.assertRaisesRegex(ArchiveError, 'PACKET_CONTENT_MISMATCH'):
            verify_packet(altered, digest(altered))

    def test_unknown_fields_and_authority_escalation_rejected(self):
        for field, value in [('extra', True), ('actionAuthority', 'EXECUTE'), ('importerVersion', '999')]:
            p = self.packet(); p[field] = value
            raw = encode(p)
            with self.subTest(field=field), self.assertRaises(ArchiveError):
                verify_packet(raw, digest(raw))

    def test_size_limits_before_read_and_normalization(self):
        with self.assertRaisesRegex(ArchiveError, 'SOURCE_SIZE_LIMIT'):
            build_packet(b'x' * (parser.MAX_BYTES + 1), 'BKL049-test', STAMP)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'source'; path.write_bytes(RAW)
            with self.assertRaisesRegex(ArchiveError, 'INPUT_SIZE_LIMIT'):
                read_regular(path, 4)

    def test_atomic_write_retry_and_conflict(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'packet.json'
            p = self.packet()
            self.assertEqual(write_packet(p, output), 'CREATED')
            original = output.read_bytes()
            self.assertEqual(write_packet(p, output), 'DUPLICATE_NOOP')
            with self.assertRaisesRegex(ArchiveError, 'RECEIPT_CONFLICT'):
                write_packet(self.packet(RAW.replace(b'0.250000', b'0.500000')), output)
            self.assertEqual(output.read_bytes(), original)
            self.assertEqual([x.name for x in Path(temp).iterdir()], ['packet.json'])

    def test_interrupted_commit_never_publishes_partial_packet(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'packet.json'
            with patch('os.link', side_effect=OSError('synthetic private diagnostic')):
                with self.assertRaisesRegex(ArchiveError, '^ATOMIC_COMMIT_UNAVAILABLE$'):
                    write_packet(self.packet(), output)
            self.assertFalse(output.exists())
            self.assertEqual(list(Path(temp).iterdir()), [])

    def test_committed_packet_survives_cleanup_failure_and_retry(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'packet.json'
            packet = self.packet()
            with patch.object(Path, 'unlink', side_effect=OSError('synthetic cleanup failure')):
                self.assertEqual(write_packet(packet, output), 'CREATED_CLEANUP_PENDING')
            self.assertEqual(verify_packet(output.read_bytes(), digest(encode(packet))), packet)
            self.assertEqual(write_packet(packet, output), 'DUPLICATE_NOOP')
            self.assertEqual(len(list(Path(temp).glob('.bkl049-*'))), 1)

    def test_failed_commit_cleanup_error_does_not_mask_original(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'packet.json'
            with patch('os.link', side_effect=OSError('synthetic commit failure')):
                with patch.object(Path, 'unlink', side_effect=OSError('synthetic cleanup failure')):
                    with self.assertRaisesRegex(ArchiveError, '^ATOMIC_COMMIT_UNAVAILABLE$'):
                        write_packet(self.packet(), output)
            self.assertFalse(output.exists())
            self.assertEqual(len(list(Path(temp).glob('.bkl049-*'))), 1)

    def test_existing_partial_packet_is_conflict_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'packet.json'; output.write_bytes(b'{')
            with self.assertRaisesRegex(ArchiveError, 'RECEIPT_CONFLICT'):
                write_packet(self.packet(), output)
            self.assertEqual(output.read_bytes(), b'{')

    def test_no_embedded_path_follow_and_no_source_mutation(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'source.js'
            source.write_bytes(b'var P=new Synthetic; P.file="Z:/not-present/private.bin";')
            original = source.read_bytes()
            p = self.packet(read_regular(source, parser.MAX_BYTES))
            write_packet(p, Path(temp) / 'packet.json')
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(p['extractionState'], 'PARSED_SUBSET')

    def test_nonregular_source_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ArchiveError, 'NOT_REGULAR_FILE'):
                read_regular(temp, parser.MAX_BYTES)

    def test_symlink_rejected_if_platform_permits_creation(self):
        with tempfile.TemporaryDirectory() as temp:
            original = Path(temp) / 'source.js'; original.write_bytes(RAW)
            link = Path(temp) / 'link.js'
            try:
                link.symlink_to(original)
            except OSError:
                self.skipTest('OS does not permit synthetic symlink creation')
            with self.assertRaisesRegex(ArchiveError, 'REPARSE_PATH'):
                read_regular(link, parser.MAX_BYTES)
            with self.assertRaisesRegex(ArchiveError, 'REPARSE_PATH'):
                write_packet(self.packet(), link)

    def test_versioned_long_literals_preserve_legacy_packets(self):
        source = ('var P=new Synthetic; P.x="' + 's'*9620 + '";').encode()
        old = build_packet(source, 'BKL049-LONG-OLD', '2026-09-30T18:00:00Z', importer_version='1.0')
        self.assertEqual(old['extractionState'], 'UNSUPPORTED')
        self.assertEqual(old['diagnostic']['code'], 'STRING_LIMIT')
        old_raw = encode(old)
        self.assertEqual(verify_packet(old_raw, digest(old_raw)), old)
        new = build_packet(source, 'BKL049-LONG-NEW', '2026-09-30T18:00:00Z')
        self.assertEqual(new['importerVersion'], '1.1')
        self.assertEqual(new['archive']['instances']['P']['parameters']['x'], 's'*9620)
        self.assertEqual(verify_packet(encode(new), digest(encode(new))), new)
        self.assertEqual(encode(old), old_raw)

    def test_profile_11_string_bound_includes_concatenation(self):
        for literal in ('"'+'x'*16385+'"', '"'+'x'*10000+'"+"'+'y'*6385+'"'):
            with self.assertRaises(parser.Unsupported) as caught:
                parser.parse_export('var P=new Synthetic;P.x='+literal+';', profile='1.1')
            self.assertEqual(caught.exception.code, 'STRING_LIMIT')
        accepted = parser.parse_export('var P=new Synthetic;P.x="'+'x'*16384+'";', profile='1.1')
        self.assertEqual(len(accepted['instances']['P']['parameters']['x']), 16384)

    def test_unknown_importer_profile_cannot_be_self_authenticated(self):
        for value in ('2.0', None, [], True):
            with self.subTest(value=value), self.assertRaises(ArchiveError):
                build_packet(b'var P=new Synthetic;', 'BKL049-INVALID', '2026-09-30T18:00:00Z', importer_version=value)
        packet = self.packet(); packet['importerVersion'] = '2.0'
        with self.assertRaises(ArchiveError):
            verify_packet(encode(packet), digest(encode(packet)))

    def test_new_limits_are_fail_closed(self):
        for source, code in [
            ('var P=new Synthetic; P.x="' + 'x'*4097 + '";', 'STRING_LIMIT'),
            ('var P=new Synthetic; P.x="' + 'x'*3000 + '"+"' + 'y'*2000 + '";', 'STRING_LIMIT'),
            ('var P=new ' + 'X'*129 + ';', 'IDENTIFIER_LIMIT'),
            ('var P=new Synthetic; P.x=' + '9'*129 + ';', 'NUMBER_LITERAL_LIMIT'),
            ('var P=new Synthetic; P.x=[' + ','.join(['0']*4097) + '];', 'ARRAY_LIMIT'),
            ('var P=new Synthetic;' + ''.join(f'P.x{i}=0;' for i in range(2049)), 'PARAMETER_LIMIT'),
            ('var P=new ProcessContainer;var A=new Synthetic;P.add(A);'+'P.invertMask(0);'*129, 'MASK_COMMAND_LIMIT')]:
            with self.subTest(code=code), self.assertRaises(parser.Unsupported) as caught:
                parser.parse_export(source)
            self.assertEqual(caught.exception.code, code)

    def test_positive_sign_and_exponent_are_lexically_preserved(self):
        result = parser.parse_export('var P=new Synthetic;P.x=+0.1200E-03;')
        self.assertEqual(result['instances']['P']['parameters']['x']['literal'], '+0.1200E-03')

    def test_source_change_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'source.js'; source.write_bytes(RAW)
            fstat = os.fstat
            calls = 0
            def changing_stat(fd):
                nonlocal calls
                info = fstat(fd)
                calls += 1
                if calls == 1:
                    source.write_bytes(b'changed')
                return info
            with patch('os.fstat', side_effect=changing_stat):
                with self.assertRaisesRegex(ArchiveError, 'SOURCE_CHANGED'):
                    read_regular(source, parser.MAX_BYTES)

    def test_reparse_attribute_is_rejected_on_every_platform(self):
        from types import SimpleNamespace
        info = SimpleNamespace(st_mode=0o100600, st_file_attributes=0x400)
        with patch.object(Path, 'lstat', return_value=info):
            with self.assertRaisesRegex(ArchiveError, 'REPARSE_PATH'):
                read_regular('synthetic', parser.MAX_BYTES)

    def test_missing_output_parent_does_not_create_directories(self):
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp) / 'missing'
            with self.assertRaisesRegex(ArchiveError, 'PATH_UNAVAILABLE'):
                write_packet(self.packet(), parent / 'packet.json')
            self.assertFalse(parent.exists())

    def test_concurrent_different_writer_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'packet.json'
            def race(*args):
                output.write_bytes(b'other writer')
                raise FileExistsError()
            with patch('os.link', side_effect=race):
                with self.assertRaisesRegex(ArchiveError, 'RECEIPT_CONFLICT'):
                    write_packet(self.packet(), output)
            self.assertEqual(output.read_bytes(), b'other writer')

    def test_cli_outputs_no_private_payload_or_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'private.js'; source.write_bytes(RAW)
            output = Path(temp) / 'private.json'
            argv = ['archive', str(source), str(output), '--receipt-id', 'BKL049-SYNTHETIC', '--imported-at', STAMP]
            stdout = io.StringIO()
            with patch('sys.argv', argv), contextlib.redirect_stdout(stdout):
                self.assertEqual(main(), 0)
            text = stdout.getvalue()
            self.assertNotIn(temp, text)
            self.assertNotIn('doNotExecute', text)
            self.assertNotIn(digest(RAW), text)
            self.assertEqual(json.loads(text)['bindingState'], 'UNLINKED')


if __name__ == '__main__':
    unittest.main()
