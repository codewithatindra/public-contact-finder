"""Shared result model and local text/HTML parser (no network)."""
from dataclasses import asdict, dataclass
from html import unescape
from html.parser import HTMLParser
import re

EMAIL = re.compile(r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])", re.I)


class LookupError(Exception):
    """The supplied profile information is not usable."""


class PublicPageParser(HTMLParser):
    """Collect readable page text and description metadata, not scripts or hidden data."""
    def __init__(self):
        super().__init__()
        self.text = []
        self.descriptions = []
        self.ignored = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs = dict(attrs)
        if tag in {'script', 'style', 'template', 'noscript', 'svg'}:
            self.ignored += 1
        if tag == 'meta':
            kind = attrs.get('name', '').lower() or attrs.get('property', '').lower()
            if kind in {'description', 'og:description'}:
                self.descriptions.append(attrs.get('content', ''))
        if tag == 'a' and not self.ignored and attrs.get('href', '').lower().startswith('mailto:'):
            # Mailto only if explicitly part of the supplied page, never linked-page crawling.
            self.text.append(attrs['href'][7:].split('?', 1)[0])

    def handle_endtag(self, tag):
        if tag.lower() in {'script', 'style', 'template', 'noscript', 'svg'} and self.ignored:
            self.ignored -= 1

    def handle_data(self, data):
        if not self.ignored:
            self.text.append(data)


def fields_from_html(html):
    parser = PublicPageParser()
    parser.feed(html)
    return [('description metadata', ' '.join(parser.descriptions)), ('page text', ' '.join(parser.text))]


def emails_in(text):
    return sorted({m.group(0).lower() for m in EMAIL.finditer(unescape(text))})


@dataclass(frozen=True)
class Result:
    platform: str
    profile_url: str
    contacts: list[dict[str, str]]

    def as_dict(self):
        return asdict(self)
