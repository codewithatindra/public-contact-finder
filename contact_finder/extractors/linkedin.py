from .base import LocalProfileAdapter


class LinkedIn(LocalProfileAdapter):
    platform = 'linkedin'
    hosts = ('linkedin.com', 'www.linkedin.com')
    path_prefixes = ('/in/', '/company/')
