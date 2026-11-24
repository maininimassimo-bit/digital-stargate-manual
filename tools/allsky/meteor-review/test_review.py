"""Synthetic regression tests. Never uses production images or destinations."""
import datetime as dt, json, os, tempfile, unittest
from pathlib import Path
import cv2, numpy as np
from review import Review

class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        for folder in ['candidates','public/thumbnails','state']:(self.root/folder).mkdir(parents=True, exist_ok=True)
        now = dt.datetime.now(dt.timezone.utc)
        self.cutoff = now-dt.timedelta(hours=1)
        self.stamp = (now-dt.timedelta(minutes=3)).astimezone(__import__('zoneinfo').ZoneInfo('Europe/Rome')).strftime('%Y%m%d%H%M%S')
        self.cfg = dict(candidates=str(self.root/'candidates'),public=str(self.root/'public'),state=str(self.root/'state'),new_after=self.cutoff.isoformat())
        self.gate = Review(self.cfg); self.make(self.stamp)
    def tearDown(self):self.gate.db.close();self.tmp.cleanup()
    def make(self, stamp):
        folder=self.root/'candidates'/stamp[:8]/'meteors';folder.mkdir(parents=True,exist_ok=True)
        image=folder/f'meteors-{stamp}.jpg';cv2.imwrite(str(image),np.zeros((100,200,3),np.uint8))
        image.with_suffix('.json').write_text(json.dumps([{'time':stamp,'p1':[20,30],'p2':[100,40]}]));return image
    def test_historic_excluded(self):
        stamp=(self.cutoff-dt.timedelta(hours=1)).astimezone(__import__('zoneinfo').ZoneInfo('Europe/Rome')).strftime('%Y%m%d%H%M%S');self.make(stamp)
        self.assertEqual(len(self.gate.pending()['pending']),1)
        with self.assertRaises(ValueError):self.gate.preview(stamp)
        with self.assertRaises(ValueError):self.gate.decide(stamp,'x','approve','test')
    def test_no_automatic_publication(self):
        self.gate.pending();self.gate.preview(self.stamp)
        self.assertEqual(list((self.root/'public').glob('*.jpg')),[])
    def test_explicit_approve_once(self):
        version=self.gate.preview(self.stamp)['version'];result=self.gate.decide(self.stamp,version,'approve','test')
        self.assertEqual(result['published'],f'meteors-{self.stamp}.jpg')
        self.assertTrue(self.gate.decide(self.stamp,version,'approve','test')['repeat'])
        self.assertEqual(len(list((self.root/'public').glob('*.jpg'))),1)
        self.assertEqual(self.gate.pending()['pending'],[])
    def test_reject_preserves_private(self):
        version=self.gate.preview(self.stamp)['version'];self.gate.decide(self.stamp,version,'reject','test')
        self.assertEqual(list((self.root/'public').glob('*.jpg')),[])
        self.assertTrue(self.make(self.stamp).exists())
    def test_changed_version_rejected(self):
        version=self.gate.preview(self.stamp)['version'];image=self.root/'candidates'/self.stamp[:8]/'meteors'/f'meteors-{self.stamp}.jpg'
        image.with_suffix('.json').write_text(json.dumps([{'time':self.stamp,'length':222}]))
        with self.assertRaises(ValueError):self.gate.decide(self.stamp,version,'approve','test')
    def test_existing_ordinary_image_not_replaced(self):
        target=self.root/'public'/f'meteors-{self.stamp}.jpg';target.write_bytes(b'ordinary-preserved')
        self.gate.decide(self.stamp,self.gate.preview(self.stamp)['version'],'approve','test')
        self.assertEqual(target.read_bytes(),b'ordinary-preserved')
    def test_path_traversal_and_old_file_rejected(self):
        with self.assertRaises(ValueError):self.gate.preview('../old')
        image=self.root/'candidates'/self.stamp[:8]/'meteors'/f'meteors-{self.stamp}.jpg';old=self.cutoff.timestamp()-1;os.utime(image,(old,old))
        with self.assertRaises(ValueError):self.gate.preview(self.stamp)
    def test_symlink_rejected(self):
        image=self.root/'candidates'/self.stamp[:8]/'meteors'/f'meteors-{self.stamp}.jpg';data=image.read_bytes();image.unlink();outside=self.root/'outside.jpg';outside.write_bytes(data);image.symlink_to(outside)
        with self.assertRaises(ValueError):self.gate.preview(self.stamp)
    def test_cutoff_cannot_be_widened_on_restart(self):
        cfg=dict(self.cfg);cfg['new_after']=(self.cutoff-dt.timedelta(days=10)).isoformat()
        with self.assertRaises(ValueError):Review(cfg)
    def test_invalid_action(self):
        with self.assertRaises(ValueError):self.gate.dispatch({'action':'publish-all','stamp':self.stamp})

if __name__=='__main__':unittest.main(verbosity=2)
