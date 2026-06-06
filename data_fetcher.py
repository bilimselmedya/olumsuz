"""Veri indirme yardımcıları — URL'den eğitim verisi alır ve yükler.

Özellikler:
- HTTPS destekli (varsayılan TLS doğrulaması), opsiyonel `--insecure` ile doğrulamayı kapatma.
- Bearer token veya Basic auth desteği.
- Yeniden deneme (retries) ve backoff desteği.
- Büyük ikili dosyaları akış (stream) ile indirip güvenli şekilde işler.

Desteklenen formatlar:
- .npz dosyası (içinde 'R', opsiyonel 'theta', 'b' dizileri)
- JSON: {'R': [[...],[...]], 'theta': [...], 'b': [...]} veya matris biçiminde liste
- CSV: yoğun matris (student x item) ya da uzun biçim (student,item,response)
"""
import io
import json
import gzip
import tempfile
import os
from typing import Tuple, Optional, Any

import numpy as np

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util import Retry
except Exception as e:
    raise ImportError("'requests' ve 'urllib3' kütüphaneleri gerekli. 'pip install requests' ile yükleyin.") from e


def _longform_to_dense(arr: np.ndarray) -> np.ndarray:
    ids_s = np.unique(arr[:, 0])
    ids_i = np.unique(arr[:, 1])
    s_map = {v: i for i, v in enumerate(ids_s)}
    i_map = {v: i for i, v in enumerate(ids_i)}
    R = np.zeros((len(ids_s), len(ids_i)), dtype=int)
    for r in arr:
        s = r[0]
        it = r[1]
        resp = int(r[2])
        R[s_map[s], i_map[it]] = resp
    return R


def _build_session(retries: int = 3, backoff_factor: float = 0.3, status_forcelist: Tuple[int, ...] = (429, 500, 502, 503, 504), headers: Optional[dict] = None, auth: Optional[Any] = None, verify: Any = True, cert: Optional[Any] = None) -> requests.Session:
    session = requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries, backoff_factor=backoff_factor, status_forcelist=list(status_forcelist), allowed_methods=frozenset(['GET', 'POST', 'PUT', 'HEAD']))
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    if headers:
        session.headers.update(headers)
    if auth:
        session.auth = auth
    session.verify = verify
    if cert:
        session.cert = cert
    return session


def load_dataset_from_url(url: str, timeout: int = 15, verify: Any = True, cert: Optional[Any] = None, auth: Optional[Any] = None, headers: Optional[dict] = None, retries: int = 3, stream_threshold: int = 10 * 1024 * 1024) -> Tuple[Optional[np.ndarray], Optional[np.ndarray], Optional[np.ndarray]]:
    """URL'den veri indirir ve (R, theta, b) döner.

    Parametreler:
    - verify: True/False veya CA bundle yolu
    - cert: client sertifika yolu veya (cert, key)
    - auth: requests uyumlu auth (ör: (user, pass))
    - headers: ek HTTP başlıkları (ör: Authorization)
    - retries: yeniden deneme sayısı
    - stream_threshold: bu boyuttan büyükse akışla indir
    """
    print(f"Veri indiriliyor: {url}")
    session = _build_session(retries=retries, headers=headers, auth=auth, verify=verify, cert=cert)
    resp = session.get(url, timeout=timeout, stream=True, allow_redirects=True)
    resp.raise_for_status()

    # İçerik uzunluğu kontrolü
    content_length = resp.headers.get('Content-Length')
    try:
        cl = int(content_length) if content_length is not None else None
    except Exception:
        cl = None

    need_stream = (cl is not None and cl > stream_threshold) or url.lower().endswith('.npz')

    if need_stream:
        # büyük dosya: diske yaz
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tmpname = tf.name
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    tf.write(chunk)
        with open(tmpname, 'rb') as f:
            content = f.read()
        # dosyayı kaldıralım; işlemler için geçici tutuldu ama bellek kullanımı olacak
        try:
            os.unlink(tmpname)
        except Exception:
            pass
    else:
        content = resp.content

    # Gzip kontrolü
    if len(content) >= 2 and content[:2] == b"\x1f\x8b":
        try:
            content = gzip.decompress(content)
        except Exception:
            pass

    # NPZ / ZIP kontrolü
    try:
        if url.lower().endswith('.npz') or (len(content) >= 4 and content[:4] == b'PK\x03\x04'):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.npz') as tf:
                tf.write(content)
                tmpname = tf.name
            try:
                npz = np.load(tmpname, allow_pickle=True)
                R = npz['R'] if 'R' in npz else None
                theta = npz['theta'] if 'theta' in npz else None
                b = npz['b'] if 'b' in npz else None
                if R is not None:
                    R = np.array(R)
                return (R, np.array(theta) if theta is not None else None, np.array(b) if b is not None else None)
            finally:
                try:
                    os.unlink(tmpname)
                except Exception:
                    pass
    except Exception:
        pass

    # Metin işleme
    text = None
    try:
        encoding = resp.encoding or 'utf-8'
        text = content.decode(encoding)
    except Exception:
        try:
            text = content.decode('utf-8', errors='replace')
        except Exception:
            text = None

    # JSON dene
    if text is not None:
        t = text.strip()
        if t.startswith('{') or t.startswith('['):
            try:
                obj = json.loads(text)
                if isinstance(obj, dict) and 'R' in obj:
                    R = np.array(obj['R'])
                    theta = np.array(obj['theta']) if 'theta' in obj else None
                    b = np.array(obj['b']) if 'b' in obj else None
                    return (R.astype(int), theta if theta is None else theta.astype(float), b if b is None else b.astype(float))
                if isinstance(obj, list):
                    arr = np.array(obj)
                    if arr.ndim == 2:
                        return (arr.astype(int), None, None)
            except Exception:
                pass

    # CSV / uzun biçim (student,item,response)
    if text is not None:
        try:
            first_line = text.splitlines()[0]
            delim = ',' if ',' in first_line else None
            arr = np.genfromtxt(io.StringIO(text), delimiter=delim)
            if arr.ndim == 1:
                arr = arr.reshape(1, -1)
            if arr.size == 0:
                raise ValueError('Boş veri alındı')
            if arr.shape[1] == 3:
                R = _longform_to_dense(arr)
                return (R.astype(int), None, None)
            else:
                return (arr.astype(int), None, None)
        except Exception:
            pass

    raise RuntimeError('Veri indirildi ancak format tanınmadı veya çözülemedi.')
