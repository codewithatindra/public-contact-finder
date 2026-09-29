from .base import LocalProfileAdapter


class Facebook(LocalProfileAdapter):
    platform = 'facebook'
    hosts = ('facebook.com', 'www.facebook.com')
    path_prefixes = ('/',)
