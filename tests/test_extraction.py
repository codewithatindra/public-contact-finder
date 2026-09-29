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

class BulkTests(unittest.TestCase):
    def test_csv_dedup_and_provenance(self):
        import contextlib
        import io
        import json
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'profile.html').write_text('<p>HELLO@example.com</p>', encoding='utf-8')
            (root / 'profiles.csv').write_text('profile_url,text,html_file\nhttps://x.com/a,hello@example.com,\nhttps://www.linkedin.com/in/b/,,profile.html\n', encoding='utf-8')
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main(['--csv', str(root / 'profiles.csv'), '--json']), 0)
            data = json.loads(out.getvalue())
            self.assertEqual(data['profiles_processed'], 2)
            self.assertEqual(len(data['contacts']), 1)
            self.assertEqual(len(data['contacts'][0]['sources']), 2)

    def test_list_and_bad_row(self):
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'profiles.tsv'
            path.write_text('https://x.com/a\tcontact@example.org\n', encoding='utf-8')
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main(['--list-file', str(path)]), 0)
            self.assertIn('contact@example.org', out.getvalue())
            path.write_text('https://x.com/a\tcontact@example.org\ninvalid line\n', encoding='utf-8')
            err = io.StringIO()
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(['--list-file', str(path)]), 2)
            self.assertIn('line 2', err.getvalue())

    def test_oversize_html_and_empty_row(self):
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'large.html').write_text('a' * 1000001)
            (root / 'profiles.csv').write_text('profile_url,text,html_file\nhttps://x.com/a,,large.html\n')
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                self.assertEqual(main(['--csv', str(root / 'profiles.csv')]), 2)
            self.assertIn('row/line 2', err.getvalue())
            self.assertIn('1 MB', err.getvalue())
