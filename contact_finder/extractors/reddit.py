from .base import LocalProfileAdapter


class Reddit(LocalProfileAdapter):
    platform = 'reddit'
    hosts = ('reddit.com', 'www.reddit.com')
    path_prefixes = ('/user/', '/u/')
