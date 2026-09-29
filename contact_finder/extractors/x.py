from .base import LocalProfileAdapter


class X(LocalProfileAdapter):
    platform = 'x'
    hosts = ('x.com', 'www.x.com', 'twitter.com', 'www.twitter.com')
    path_prefixes = ('/',)
