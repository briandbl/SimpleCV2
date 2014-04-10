from nose.tools import assert_equals, assert_almost_equals

from simplecv.features.blob import Blob
from simplecv.image import Image
from simplecv.color import Color
from simplecv.tests.utils import perform_diff, perform_diff_blobs

def test_setstate():
    b = Blob()
    #b_string = pickle.dumps(b)
    #b_new = pickle.loads(b_string)
    b.__setstate__({'m00':50, 'm01':100, 'm02__string':200, 'label__string':'empty'})
    assert_equals(b.m00, 50)
    assert_equals(b.m01, 100)
    assert_equals(b.m02, 200)
    assert_equals(b.label, 'empty')

def test_hull():
    img = Image(source="lenna")
    blobs = img.find_blobs()
    blob = blobs[-1]
    chull = blob.hull()

def test_blob_draw_rect():
    img = Image(source="lenna")
    blobs = img.find_blobs()
    blob = blobs[-1]
    blob.draw_rect(color=Color.BLUE, width=-1, alpha=128)

    img1 = Image(source="simplecv")
    blobs = img1.find_blobs()
    blob = blobs[-1]
    blob.draw_rect(color=Color.RED, width=2, alpha=255)

    imgs = [img, img1]
    name_stem = "test_blob_drawRect"
    perform_diff(imgs, name_stem, 0.0)

def test_blob_rectify_major_axis():
    img = Image(source="lenna")
    blobs = img.find_blobs()
    blobs_1 = blobs[-1]
    blobs_1.rectify_major_axis()
    blobs_2 = blobs[-2]
    blobs_2.rectify_major_axis(1)

    blobs1 = img.find_blobs()
    blobs1_1 = blobs1[-1]
    blobs1_1.rotate(blobs1_1.get_angle())
    blobs1_2 = blobs[-2]
    blobs1_2.rectify_major_axis(1)

    perform_diff_blobs(blobs_1, blobs1_1)
    perform_diff_blobs(blobs_2, blobs1_2)

def test_blob_draw_appx():
    nBlob = Blob()
    nBlob.draw_appx()

    img = Image(source="simplecv")
    blobs = img.find_blobs()
    blob = blobs[-1]
    blob.draw_appx(color=Color.GREEN, width=-1, alpha=128)

    img1 = Image(source="lenna")
    blobs1 = img1.find_blobs()
    blob1 = blobs1[-2]
    blob1.draw_appx(color=Color.RED, width=3, alpha=255)

    result = [img, img1]
    name_stem = "test_blob_draw_appx"
    
    perform_diff(result, name_stem, 0.0)

def test_blob_draw_outline():
    img = Image(source="simplecv")
    blobs = img.find_blobs()
    blob = blobs[-2]
    blob.draw_outline(color=Color.GREEN, width=3, alpha=128)

    img1 = Image(source="lenna")
    blobs1 = img1.find_blobs()
    blob1 = blobs1[-2]
    blob1.draw_outline(color=Color.RED, width=-1, alpha=255)

    result = [img, img1]
    name_stem = "test_blob_draw_outline"
    
    perform_diff(result, name_stem, 0.0)

def test_blob_draw_holes():
    img = Image(source="simplecv")
    blobs = img.find_blobs()
    blob = blobs[-1]
    blob.draw_holes(color=Color.YELLOW, width=-1, alpha=200)

    img1 = Image(source="lenna")
    blobs1 = img1.find_blobs()
    blob1 = blobs1[-1]
    blob1.draw_holes(color=Color.BLUE, width=5, alpha=255)

    result = [img, img1]
    name_stem = "test_blob_draw_holes"
    
    perform_diff(result, name_stem, 0.0)

def test_blob_draw_hull():
    img = Image(source="simplecv")
    blobs = img.find_blobs()
    blob = blobs[-1]
    blob.draw_hull(color=Color.AZURE, width=3, alpha=255)

    img1 = Image(source="lenna")
    blobs1 = img1.find_blobs()
    blob1 = blobs1[-1]
    blob1.draw_hull(color=Color.PLUM, width=-1, alpha=100)

    result = [img, img1]
    name_stem = "test_blob_draw_hull"
    
    perform_diff(result, name_stem, 0.0)

def test_blob_is_square():
    img = Image((400,400))
    nparray = img.get_ndarray()
    nparray[100:300, 100:300] = (255, 255, 255)

    blobs = img.find_blobs()
    blob = blobs[0]
    assert_equals(blob.is_square(), True)

    img1 = Image((400,400))
    nparray1 = img1.get_ndarray()
    nparray1[50:350, 100:300] = (255, 255, 255)
    blobs1 = img1.find_blobs()
    blob1 = blobs1[0]
    assert_equals(blob1.is_square(), False)

def test_blob_centroid():
    img = Image((400,400))
    nparray = img.get_ndarray()
    nparray[100:300, 100:300] = (255, 255, 255)

    blobs = img.find_blobs()
    blob = blobs[0]

    assert_equals(blob.centroid(), (199.5, 199.5))

def test_blob_radius():
    img = Image((400,400))
    nparray = img.get_ndarray()
    nparray[100:300, 100:300] = (255, 255, 255)

    blobs = img.find_blobs()
    blob = blobs[0]

    assert_equals(int(blob.radius()), 140)

def test_blob_hull_radius():
    img = Image((400,400))
    nparray = img.get_ndarray()
    nparray[100:300, 100:300] = (255, 255, 255)

    blobs = img.find_blobs()
    blob = blobs[0]

    assert_equals(int(blob.hull_radius()), 140)

def test_blob_match():
    img = Image((400,400))
    nparray = img.get_ndarray()
    nparray[50:150, 50:150] = (255, 255, 255)
    nparray[100:150, 150:250] = (255, 255, 255)
    nparray[200:300, 50:150] = (255, 255, 255)
    nparray[250:300, 150:250] = (255, 255, 255)

    blobs = img.find_blobs()
    blob = blobs[0]
    blob1 = blobs[1]

    if (blob.match(blob1) > 6e-10):
        assert False

def test_blob_repr():
    img = Image((400,400))
    nparray = img.get_ndarray()
    nparray[50:150, 50:150] = (255, 255, 255)
    nparray[100:150, 150:250] = (255, 255, 255)

    blobs = img.find_blobs()
    blob = blobs[0]

    bstr = "simplecv.features.blob.Blob object at (150, 100) with " \
            "area 14701"

    assert_equals(blob.__repr__(), bstr)

def test_blob_get_sc_descriptors():
    img = Image((400,400))
    nparray = img.get_ndarray()
    nparray[50:150, 50:150] = (255, 255, 255)
    nparray[250:350, 150:250] = (255, 255, 255)

    blobs = img.find_blobs()
    blob0 = blobs[0]
    blob1 = blobs[1]

    scd0, cc0 = blob0.get_sc_descriptors()
    scd1, cc1 = blob1.get_sc_descriptors()

    assert_equals(len(scd0), len(scd1))
    assert_equals(len(cc0), len(cc1))

    if (cc0[0][0] > cc1[0][0]):
        for index in range(len(cc0)):
            assert_almost_equals(cc0[index][0]-100, cc1[index][0], 5)
            assert_almost_equals(cc0[index][1]-200, cc1[index][1], 5)
            #cc2.append((ccp[0]-100, ccp[1]-200))
    else:
        for index in range(len(cc0)):
            assert_almost_equals(cc0[index][0]+100, cc1[index][0], 5)
            assert_almost_equals(cc0[index][1]+200, cc1[index][1], 5)

    for index in range(len(scd0)):
        assert_equals(scd0[index].data, scd1[index].data)

# broken utility
"""
def test_blob_show_correspondence():
    img = Image((400,400))
    nparray = img.get_ndarray()
    nparray[50:150, 50:150] = (255, 255, 255)
    nparray[250:350, 150:250] = (255, 255, 255)

    blobs = img.find_blobs()
    blob0 = blobs[0]
    blob1 = blobs[1]
"""

def test_get_shape_context():
    img = Image((400,400))
    nparray = img.get_ndarray()
    nparray[50:150, 50:150] = (255, 255, 255)
    nparray[250:350, 150:250] = (255, 255, 255)

    blobs = img.find_blobs()
    blob0 = blobs[0]
    blob0.get_shape_context()
















