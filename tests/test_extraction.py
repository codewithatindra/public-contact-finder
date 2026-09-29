import tempfile
import unittest
from pathlib import Path
from contact_finder.__main__ import main
from contact_finder.core import LookupError, fields_from_html, emails_in
from contact_finder.registry import extractor_for


class ExtractionTests(unittest.TestCase):
    def test_email_from_text(self):
        self.assertEqual(emails_in('Work: Hi@Example.org'), ['hi@example.org'])

    def test_html_visible_text_and_metadata_not_scripts(self):
        html = '<meta name="description" content="Work: Hi@Example.org"><body><p>reach me@site.com</p><script>secret@no.test</script><a href="mailto:sales@site.com">Email</a></body>'
        fields = fields_from_html(html)
        result = extractor_for('https://www.instagram.com/demo/').extract('https://www.instagram.com/demo/', fields)
        self.assertEqual({x['email'] for x in result.contacts}, {'hi@example.org', 'me@site.com', 'sales@site.com'})

    def test_platform_adapters(self):
        urls = {'instagram': 'https://www.instagram.com/demo/',
                'x': 'https://x.com/demo', 'linkedin': 'https://www.linkedin.com/in/demo/',
                'facebook': 'https://www.facebook.com/demo',
                'youtube': 'https://www.youtube.com/@demo', 'reddit': 'https://www.reddit.com/user/demo/',
                'other': 'https://example.org/profile/demo'}
        for platform, url in urls.items():
            with self.subTest(platform=platform):
                result = extractor_for(url).extract(url, [('bio', 'contact@example.com')])
                self.assertEqual(result.platform, platform)
                self.assertEqual(result.contacts, [{'email': 'contact@example.com', 'field': 'bio'}])

    def test_non_https_rejected(self):
        with self.assertRaises(LookupError):
            extractor_for('http://example.org/person')

    def test_html_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'profile.html'
            path.write_text('<meta property="og:description" content="work@example.com">')
            self.assertEqual(main(['https://x.com/demo', '--html-file', str(path)]), 0)


if __name__ == '__main__':
    unittest.main()
