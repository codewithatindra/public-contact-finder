# Public Contact Finder

A Python CLI that finds email addresses explicitly published in a social profile's saved page or pasted public bio/contact text. You supply the page or text and its source profile URL. It reports the address and where it was found; it never guesses addresses, logs in, crawls profiles or sends messages.

## What works

- Saved HTML pages: parse readable page text, `mailto:` links and standard description metadata. Skip scripts, styles, templates and embedded data. A saved page may still contain unrelated text, so review each hit before use.
- Pasted text: parse the public bio/contact text you supply.
- One URL at a time, from Instagram, X, LinkedIn, Facebook, YouTube, Reddit, or another HTTPS profile. Separate platform adapters use one local parser interface; unknown sites use a generic adapter.
- Text or JSON output with email, platform, source URL and field; no storage or outreach automation.

## Install and run

Python 3.10+; no third-party dependencies.

```sh
python3 -m contact_finder https://www.instagram.com/example/ --text 'Business inquiries: hello@example.com'
python3 -m contact_finder https://www.linkedin.com/in/example/ --html-file saved-profile.html --json
python3 -m unittest discover -s tests -v
```

The examples use invented accounts and addresses. The CLI never fetches the URL. Only feed it content you are allowed to use. For a saved HTML page, the address may come from visible page text, a mailto link or the page's description metadata. It is not proof that the address belongs to the named person; verify before any outreach.

## Platform status and limitations

| Platform | Local supplied-page parser | Automated network fetching |
| --- | --- | --- |
| Instagram, Facebook | Yes | Disabled: Meta restricts automated collection without permission |
| X | Yes | Disabled: X restricts crawling/scraping without permission |
| LinkedIn | Yes | Disabled: crawling requires express permission |
| YouTube | Yes | Disabled: automated access is restricted |
| Reddit | Yes | Disabled: API access requires approval and automated collection is limited |
| Other HTTPS profile pages | Yes | Disabled until a specific source has a verified permitted route |

Public visibility does not make automated collection permitted. Major platforms restrict access, and their pages may hide email behind login, JavaScript or contact buttons. A future network extractor could be brittle or rate-limited and could violate a platform's terms if built without permission. This v1 does **not** auto-fetch anywhere: the architecture can add a permitted adapter later after review of source terms, access route and tests. It never handles credentials, bypasses protections or silently falls back to scraping.

## Compliance and ethics

Use only for legitimate, relevant outreach, with a lawful basis and where source terms allow processing. Check current platform Terms of Service and robots.txt where applicable; honor rate limits, opt-outs and requests to stop. Public display is not blanket consent to mass-email, resell or keep personal data forever. Follow applicable privacy and anti-spam rules, including India's DPDP Act and GDPR where they apply. Give required notices, limit retention and delete data when no longer needed. This tool does not store data or send mail.

Platform references: [Instagram Terms](https://help.instagram.com/581066165581870/), [Meta automated collection](https://www.facebook.com/legal/automated_data_collection_terms), [LinkedIn crawling](https://www.linkedin.com/legal/crawling-terms), [YouTube Terms](https://www.youtube.com/static?gl=US&template=terms), [Reddit builder policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy).

## Adding permitted auto-fetch

An adapter must use a documented permitted public route and fail closed on authentication requirements, 429s and access restrictions. Add source-specific tests and terms review before enabling network calls. No login flows, session cookies, CAPTCHA bypasses, guessed-email generation or bulk discovery.

## License

MIT.
