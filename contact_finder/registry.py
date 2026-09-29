"""Map known platform hostnames to adapters; other HTTPS profile URLs work locally."""
from urllib.parse import urlparse
from .core import LookupError
from .extractors.instagram import Instagram
from .extractors.x import X
from .extractors.linkedin import LinkedIn
from .extractors.facebook import Facebook
from .extractors.youtube import YouTube
from .extractors.reddit import Reddit
from .extractors.generic import Generic

ADAPTERS = [Instagram(), X(), LinkedIn(), Facebook(), YouTube(), Reddit()]


def extractor_for(url):
    parsed = urlparse(url)
    if parsed.scheme != 'https' or not parsed.hostname:
        raise LookupError('A source HTTPS profile URL is required')
    for adapter in ADAPTERS:
        if parsed.hostname in adapter.hosts:
            return adapter
    return Generic()
