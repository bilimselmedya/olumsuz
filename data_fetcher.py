"""Veri indirme yardımcıları — URL'den eğitim verisi alır ve yükler.

Özellikler:
- HTTPS destekli (varsayılan TLS doğrulaması), opsiyonel `--insecure` ile doğrulamayı kapatma.
- Bearer token veya Basic auth desteği.
"""Minimal data fetcher utility.

This file provides a small, well-documented function to download a dataset
from a URL and return bytes. It intentionally keeps features minimal so it
is easy to test and extend.
"""
from typing import Optional
import requests


def fetch_bytes(url: str, timeout: int = 15, verify: bool = True, headers: Optional[dict] = None, auth: Optional[tuple] = None) -> bytes:
    """Download bytes from `url` and return content.

    Raises `requests.HTTPError` on non-200 responses.
    """
    session = requests.Session()
    if headers:
        session.headers.update(headers)
    resp = session.get(url, timeout=timeout, stream=True, verify=verify, auth=auth)
    resp.raise_for_status()
    # For reasonably sized files, .content is fine; callers may stream if needed.
    return resp.content

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
