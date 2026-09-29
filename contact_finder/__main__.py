"""Local-content-only one-profile command-line entry point."""
import argparse
import json
import sys
from pathlib import Path
from .core import LookupError, fields_from_html
from .registry import extractor_for


def main(argv=None):
    parser = argparse.ArgumentParser(description='Extract published emails from supplied profile text or saved page')
    parser.add_argument('profile_url', help='Source profile URL (never fetched)')
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--text', help='Pasted public bio/contact or profile page text')
    source.add_argument('--html-file', type=Path, help='Saved public HTML page you are permitted to process')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args(argv)
    try:
        if args.html_file:
            if args.html_file.stat().st_size > 1_000_000:
                raise LookupError('HTML file too large (1 MB limit)')
            fields = fields_from_html(args.html_file.read_text(encoding='utf-8'))
        else:
            fields = [('supplied text', args.text)]
        result = extractor_for(args.profile_url).extract(args.profile_url, fields)
    except (LookupError, OSError, UnicodeError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result.as_dict(), indent=2))
    elif result.contacts:
        for contact in result.contacts:
            print(f"{contact['email']}\t{result.platform}\t{contact['field']}\t{result.profile_url}")
    else:
        print('No published email found in supplied content')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
