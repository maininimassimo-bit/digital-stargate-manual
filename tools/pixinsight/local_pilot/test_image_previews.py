import hashlib
import unittest
import numpy as np
from .image_previews import curve,render,provider_image

class PreviewTests(unittest.TestCase):
    def test_curve_maps_parent_median_and_preserves_source(self):
        x=np.full((32,32,1),.05,dtype=np.float32);before=x.copy()
        raw,report=render(x,curve(.05,.2))
        from PIL import Image
        import io
        self.assertEqual(Image.open(io.BytesIO(raw)).getpixel((0,0)),51)
        np.testing.assert_array_equal(x,before);self.assertFalse(report['scientificPixelData'])
    def test_shared_curve_does_not_equalize_changed_checkpoint(self):
        parent=np.full((32,32,1),.05,dtype=np.float32)
        a,_=render(parent,curve(.05));b,_=render(parent*2,curve(.05))
        self.assertNotEqual(a,b)
    def test_native_crop_is_not_rescaled(self):
        raw,r=render(np.full((300,400,3),.1,dtype=np.float32),curve(.1),[10,20,210,220])
        self.assertEqual(r['displayGeometry'],[200,200]);self.assertEqual(r['resampling'],'NONE')
        self.assertEqual(provider_image(raw,hashlib.sha256(raw).hexdigest())['detail'],'low')
    def test_bad_curve_region_nonfinite_and_digest_fail(self):
        x=np.full((32,32,1),.1,dtype=np.float32)
        bad=curve(.1);bad['midtones']=.5
        with self.assertRaises(ValueError):render(x,bad)
        with self.assertRaises(ValueError):render(x,curve(.1),[0,0,33,32])
        x[0,0,0]=np.nan
        with self.assertRaises(ValueError):render(x,curve(.1))
        with self.assertRaises(ValueError):provider_image(b'not PNG','a'*64)

if __name__=='__main__':unittest.main()
