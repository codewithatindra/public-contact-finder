from .base import LocalProfileAdapter


class Instagram(LocalProfileAdapter):
    platform = 'instagram'
    hosts = ('instagram.com', 'www.instagram.com')
    path_prefixes = ('/',)
