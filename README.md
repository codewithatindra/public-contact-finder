# Public Contact Finder

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue) ![MIT](https://img.shields.io/badge/License-MIT-green)

Turn public profile bio text or saved HTML you already have into a clean, source-linked contact list. This is a local Python CLI: it never visits a profile URL, guesses an email address, logs in, or sends outreach.

## Quickstart

Python 3.10+; no runtime dependencies. Install from a clone (the package is ready to build but has **not** been published to PyPI):

```sh
git clone https://github.com/codewithatindra/public-contact-finder.git
cd public-contact-finder
python3 -m pip install .
public-contact-finder --csv examples/profiles.csv --json
```

The sample CSV contains three fictional profiles. The output deduplicates addresses across profiles while keeping each source:

```json
{
  "profiles_processed": 3,
  "contacts": [
    {
      "email": "hello@example.com",
      "sources": [
        {"platform": "instagram", "profile_url": "https://www.instagram.com/example/", "field": "supplied text"},
        {"platform": "x", "profile_url": "https://x.com/example", "field": "supplied text"},
        {"platform": "linkedin", "profile_url": "https://www.linkedin.com/in/example/", "field": "description metadata"}
      ]
    },
    {
      "email": "team@example.org",
      "sources": [
        {"platform": "x", "profile_url": "https://x.com/example", "field": "supplied text"}
      ]
    }
  ]
}
```

The examples use invented addresses and profiles. No network request is made when you run the CLI. Review every result and verify that the address belongs to the intended contact before outreach.

## Who it's for

Founders doing focused, relevant outreach can paste a prospective partner's published business contact text, or save a page they are allowed to process, then get one deduplicated list with a source for each address. This helps keep notes tidy; it is **not** a prospect scraper, mass-mailer, consent checker, or proof that an address belongs to a person.

## Use your own content

```sh
# One profile; the URL is a label, not a fetch target
public-contact-finder https://www.instagram.com/example/ --text 'Business inquiries: hello@example.com'

# One saved HTML page; parses readable text, mailto links and description metadata
public-contact-finder https://www.linkedin.com/in/example/ --html-file saved-profile.html --json

# Several saved bios: CSV columns profile_url,text,html_file
public-contact-finder --csv examples/profiles.csv --json

# Or UTF-8 tab-separated lines: profile_url<TAB>published bio text
public-contact-finder --list-file examples/profiles.tsv

public-contact-finder --version
python3 -m unittest discover -s tests -v
```

CSV requires `profile_url` and at least one of `text` or `html_file` as headers. Each row must contain exactly one nonempty source. Relative HTML paths are resolved relative to the CSV file. A list file uses a tab between the HTTPS profile URL and text; blank lines and lines beginning with `#` are ignored. CSV/list input is capped at 5 MB, and each HTML file at 1 MB. A malformed row stops the run with its row or line number and exit code 2; no partial output is printed. Plain-text bulk output prints each distinct address/source pair. JSON bulk output keeps one address with all distinct source citations.

Adapters label Instagram, X, LinkedIn, Facebook, YouTube and Reddit profiles; other HTTPS profile URLs are labeled `other`. These adapters only parse content you supply. Scripts, styles, templates and embedded data in saved HTML are skipped. A saved page can still include unrelated visible text or description metadata, so inspect matches.

## Why there is no auto-fetch

| Platform | Supplied-content parsing | Automated fetching |
| --- | --- | --- |
| Instagram, Facebook | Yes | Disabled: Meta restricts automated collection without permission |
| X | Yes | Disabled: X restricts crawling/scraping without permission |
| LinkedIn | Yes | Disabled: crawling requires express permission |
| YouTube | Yes | Disabled: automated access is restricted |
| Reddit | Yes | Disabled: API access requires approval and automated collection is limited |
| Other HTTPS pages | Yes | Disabled until a specific route is reviewed and permitted |

Public visibility is not permission to collect automatically. The CLI does not fetch URLs, use credentials, bypass controls or silently fall back to scraping. A future source-specific network adapter would require a documented permitted route, a current terms review and tests. No bulk discovery is included: bulk mode parses only your supplied records.

## Responsible use

Use only content you have a right to process, for relevant outreach where you have a lawful basis. Follow source terms, applicable privacy and anti-spam rules, notices, opt-outs, retention limits and requests to stop. Public display is not blanket consent to mass email or resale. The tool does not store results or send messages; you decide what to do with its output.

Platform references: [Instagram Terms](https://help.instagram.com/581066165581870/), [Meta automated collection](https://www.facebook.com/legal/automated_data_collection_terms), [LinkedIn crawling](https://www.linkedin.com/legal/crawling-terms), [YouTube Terms](https://www.youtube.com/static?gl=US&template=terms), [Reddit builder policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy).

## License

MIT.
