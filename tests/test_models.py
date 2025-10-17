
from app.models import Sample

def test_sample_model():
    s = Sample(id="abc123", path="/tmp/foo.wav", name="pad_dreamscape_Am_88bpm.wav", bpm=88.0, key="Am", tags=["ambient","pad"])
    assert s.key == "AM"  # normalized to upper
    assert s.bpm == 88.0
