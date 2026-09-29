"""Parse user-supplied profile records locally; never fetch a URL."""
import csv
from dataclasses import dataclass
from pathlib import Path

from .core import LookupError, fields_from_html
from .registry import extractor_for

MAX_INPUT_BYTES = 5_000_000
MAX_HTML_BYTES = 1_000_000


@dataclass(frozen=True)
class Entry:
    profile_url: str
    text: str = ''
    html_file: str = ''
    line: int = 0


def read_html(path):
    try:
        if path.stat().st_size > MAX_HTML_BYTES:
            raise LookupError(f'HTML file exceeds 1 MB: {path}')
        return fields_from_html(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeError) as exc:
        raise LookupError(f'Cannot read HTML file {path}: {exc}') from exc


def entries_from_file(path, kind):
    try:
        if path.stat().st_size > MAX_INPUT_BYTES:
            raise LookupError(f'Input file exceeds 5 MB: {path}')
        with path.open(encoding='utf-8-sig', newline='') as stream:
            if kind == 'csv':
                reader = csv.DictReader(stream)
                if not reader.fieldnames or 'profile_url' not in reader.fieldnames:
                    raise LookupError('CSV needs a profile_url header (plus text or html_file)')
                if not ({'text', 'html_file'} & set(reader.fieldnames)):
                    raise LookupError('CSV needs a text or html_file header')
                for row in reader:
                    line = reader.line_num
                    if None in row:
                        raise LookupError(f'CSV row {line}: too many columns')
                    yield Entry((row.get('profile_url') or '').strip(), row.get('text') or '',
                                row.get('html_file') or '', line)
            else:
                for line, raw in enumerate(stream, 1):
                    if not raw.strip() or raw.lstrip().startswith('#'):
                        continue
                    parts = raw.rstrip('\r\n').split('\t', 1)
                    if len(parts) != 2:
                        raise LookupError(f'List line {line}: use profile_url<TAB>published bio text')
                    yield Entry(parts[0].strip(), parts[1], '', line)
    except (OSError, UnicodeError, csv.Error) as exc:
        raise LookupError(f'Cannot read {kind} file {path}: {exc}') from exc


def extract_entry(entry, base_dir):
    label = f'row/line {entry.line}: ' if entry.line else ''
    if not entry.profile_url:
        raise LookupError(f'{label}profile_url is empty')
    if bool(entry.text.strip()) == bool(entry.html_file.strip()):
        raise LookupError(f'{label}provide exactly one of text or html_file')
    try:
        if entry.html_file.strip():
            file = Path(entry.html_file.strip())
            fields = read_html(file if file.is_absolute() else base_dir / file)
        else:
            fields = [('supplied text', entry.text)]
        return extractor_for(entry.profile_url).extract(entry.profile_url, fields)
    except LookupError as exc:
        raise LookupError(f'{label}{exc}') from exc


def bulk_results(entries, base_dir):
    """Deduplicate emails while retaining each distinct profile/field citation."""
    contacts = {}
    count = 0
    for entry in entries:
        result = extract_entry(entry, base_dir)
        count += 1
        for contact in result.contacts:
            source = {'platform': result.platform, 'profile_url': result.profile_url,
                      'field': contact['field']}
            sources = contacts.setdefault(contact['email'], [])
            if source not in sources:
                sources.append(source)
    return {'profiles_processed': count,
            'contacts': [{'email': email, 'sources': sources} for email, sources in contacts.items()]}
