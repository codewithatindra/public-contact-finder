"""Local-content-only adapter interface. No outbound network capability."""
from urllib.parse import urlparse
from ..core import LookupError, Result, emails_in


class LocalProfileAdapter:
    platform = ''
    hosts = ()
    path_prefixes = ('/',)

    def extract(self, url, fields):
        parsed = urlparse(url)
        if (parsed.scheme != 'https' or not parsed.hostname or
                (self.hosts and parsed.hostname not in self.hosts) or
                parsed.username or parsed.password or parsed.port not in (None, 443) or
                parsed.query or parsed.fragment or not any(parsed.path.startswith(prefix) for prefix in self.path_prefixes)):
            raise LookupError(f'Expected an HTTPS {self.platform} profile URL')
        contacts, seen = [], set()
        for field, text in fields:
            for email in emails_in(text):
                if email not in seen:
                    seen.add(email)
                    contacts.append({'email': email, 'field': field})
        return Result(self.platform, url, contacts)
