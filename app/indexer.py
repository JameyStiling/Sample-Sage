
from __future__ import annotations
import os, re, hashlib
from typing import List, Dict
from .models import Sample

AUDIO_EXTS = {'.wav', '.aiff', '.aif', '.mp3', '.flac', '.ogg'}

FILENAME_RE = re.compile(
    r'(?P<name>.*?)'
    r'(?:[_\-](?P<key>[A-Ga-g][b#]?m?))?'
    r'(?:[_\-](?P<bpm>\d{2,3})bpm)?',
    re.IGNORECASE
)

def file_id(path: str) -> str:
    return hashlib.md5(path.encode('utf-8')).hexdigest()[:12]

def infer_metadata_from_name(filename: str) -> dict:
    m = FILENAME_RE.match(os.path.splitext(filename)[0])
    meta: Dict[str, str] = {}
    if m:
        if m.group('key'):
            meta['key'] = m.group('key')
        if m.group('bpm'):
            meta['bpm'] = float(m.group('bpm'))
    return meta

def scan_directory(root: str) -> List[Sample]:
    samples: List[Sample] = []
    for dirpath, _, files in os.walk(root):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext not in AUDIO_EXTS:
                continue
            path = os.path.join(dirpath, f)
            meta = infer_metadata_from_name(f)
            s = Sample(
                id=file_id(path),
                path=path,
                name=f,
                bpm=meta.get('bpm'),
                key=meta.get('key'),
                tags=[]
            )
            samples.append(s)
    return samples
