"""Local-content-only command-line entry point."""
import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .bulk import Entry, bulk_results, entries_from_file, extract_entry
from .core import LookupError


def main(argv=None):
    parser = argparse.ArgumentParser(description='Extract published emails from supplied profile text or saved pages; URLs are never fetched')
    parser.add_argument('profile_url', nargs='?', help='Source HTTPS profile URL for single-profile mode (never fetched)')
    source = parser.add_mutually_exclusive_group()
    source.add_argument('--text', help='Pasted public bio/contact or profile page text')
    source.add_argument('--html-file', type=Path, help='Saved public HTML page you are permitted to process')
    source.add_argument('--csv', type=Path, help='CSV with profile_url and text or html_file columns')
    source.add_argument('--list-file', type=Path, help='UTF-8 lines: profile_url<TAB>published bio text')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    parser.add_argument('--version', action='version', version=f'public-contact-finder {__version__}')
    args = parser.parse_args(argv)
    bulk = args.csv is not None or args.list_file is not None
    if bulk and args.profile_url:
        parser.error('Do not pass a positional profile URL with --csv or --list-file')
    if not bulk and (not args.profile_url or (args.text is None and args.html_file is None)):
        parser.error('Pass a profile URL with --text or --html-file, or use --csv/--list-file')
    try:
        if bulk:
            path = args.csv or args.list_file
            data = bulk_results(entries_from_file(path, 'csv' if args.csv else 'list'), path.parent)
            if args.json:
                print(json.dumps(data, indent=2))
            elif data['contacts']:
                for contact in data['contacts']:
                    for citation in contact['sources']:
                        print(f"{contact['email']}\t{citation['platform']}\t{citation['field']}\t{citation['profile_url']}")
            else:
                print(f"No published email found in {data['profiles_processed']} supplied profiles")
        else:
            result = extract_entry(Entry(args.profile_url, args.text or '', str(args.html_file) if args.html_file else ''), Path.cwd())
            if args.json:
                print(json.dumps(result.as_dict(), indent=2))
            elif result.contacts:
                for contact in result.contacts:
                    print(f"{contact['email']}\t{result.platform}\t{contact['field']}\t{result.profile_url}")
            else:
                print('No published email found in supplied content')
    except LookupError as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
