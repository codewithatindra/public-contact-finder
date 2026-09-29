from .base import LocalProfileAdapter


class YouTube(LocalProfileAdapter):
    platform = 'youtube'
    hosts = ('youtube.com', 'www.youtube.com')
    path_prefixes = ('/@', '/channel/', '/c/', '/user/')
