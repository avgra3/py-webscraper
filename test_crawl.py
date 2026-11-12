import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html, extract_page_data, ExtractedPageData

class TestCrawl(unittest.TestCase):
    def test_normalize_url_base(self):
        inputs = ["https://www.boot.dev/blog/path", "http://www.boot.dev/blog/path", "http://www.boot.dev/blog/path", "www.boot.dev/blog/path"]
        actuals = list(map(normalize_url, inputs))
        expected = "www.boot.dev/blog/path"
        for item in actuals:
            self.assertEqual(item, expected)

    def test_normalize_url_long(self):
        inputs = "http://www.boot.dev/blog/path/this-is-a-really-long-path-for-some-reason/"
        actual = normalize_url(inputs)
        expected = "www.boot.dev/blog/path/this-is-a-really-long-path-for-some-reason/"
        self.assertEqual(actual, expected)

    def test_normalize_url_partial(self):
        inputs = "www.boot.dev/blog/path"
        actual = normalize_url(inputs)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)


    def test_get_heading_from_html(self):
        input_html_page = """<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""
        # if <h1> in text should return <h1>, else return the <h2>
        expected = "Welcome to Boot.dev"
        actual = get_heading_from_html(html=input_html_page)
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_no_h1(self):
        second_input_html_page = """<html>
  <body>
    <h2>Welcome to Boot.dev from H2</h2>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""

        # no <h1> in text should return the <h2>
        second_expected = "Welcome to Boot.dev from H2"
        second_actual = get_heading_from_html(html=second_input_html_page)
        self.assertEqual(second_actual, second_expected)

    def test_get_heading_from_html_both_h1_and_h2(self):
        # if both <h1> and <h2>, should show <h1> only!
        third_input_html_page = """<html>
  <body>
    <h1>Welcome to Boot.dev from H1</h1>
    <h2>Welcome to Boot.dev from H2</h2>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""
        third_expected = "Welcome to Boot.dev from H1"
        third_actual = get_heading_from_html(html=third_input_html_page)
        self.assertEqual(third_actual, third_expected)

    def test_get_heading_from_html_no_h1_or_h2(self):
        # no <h1> or <h2>, should return an empty string
        fourth_input_html_page = """<html>
  <body>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""
        fourth_expected = ""
        fourth_actual = get_heading_from_html(html=fourth_input_html_page)
        self.assertEqual(fourth_actual, fourth_expected)

    def test_get_first_paragraph_from_html(self):
        input_html_page = """<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <p>Outside paragraph.</p>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""
        expected = "Learn to code by building real projects."
        not_expected = "This is the second paragraph"
        actual = get_first_paragraph_from_html(html=input_html_page)
        self.assertEqual(actual, expected)
        self.assertNotEqual(actual, not_expected)

    def test_get_first_paragraph_from_html(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_many(self):
        second_input_url = "https://crawler-test.com"
        second_input_body = '<html><body><img src="/logo.png" alt="Logo"><img src="/second_logo.png" alt="Logo 2"></body></html>'
        second_actual = get_images_from_html(second_input_body, second_input_url)
        second_expected = ["https://crawler-test.com/logo.png", "https://crawler-test.com/second_logo.png"]
        self.assertEqual(second_actual, second_expected)

    def test_get_images_from_html_mixed(self):
        third_input_url = "https://crawler-test.com"
        third_input_body = '<html><body><img src="/logo.png" alt="Logo"><img src="/second_logo.png" alt="Logo 2"><img src="https://google.com/third_image.png" alt="Third image"></body></html>'
        third_actual = get_images_from_html(third_input_body, third_input_url)
        third_expected = ["https://crawler-test.com/logo.png", "https://crawler-test.com/second_logo.png", "https://google.com/third_image.png"]
        self.assertEqual(third_actual, third_expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_multiple_urls_from_html_relative(self):
        second_input_url = "https://crawler-test.com"
        second_input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a><a href="https://crawler-test2.com"><span>Boot2.dev</span></a><a href="https://crawler-test3.com"><span>Boot3.dev</span></a></body></html>'
        second_actual = get_urls_from_html(second_input_body, second_input_url)
        second_expected = ["https://crawler-test.com", "https://crawler-test2.com","https://crawler-test3.com"]
        self.assertEqual(second_actual, second_expected)

    def test_get_mix_urls_from_html_relative(self):
        third_input_url = "https://crawler-test.com"
        third_input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a><a href=""><span>Boots.dev</span></a></body></html>'
        third_actual = get_urls_from_html(third_input_body, third_input_url)
        third_expected = ["https://crawler-test.com", "https://crawler-test.com"]
        self.assertEqual(third_actual, third_expected)

    def test_extract_page_data(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
        <h1>Test Title</h1>
        <p>This is the first paragraph.</p>
        <a href="/link1">Link 1</a>
        <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected: ExtractedPageData = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
            }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_data(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected: ExtractedPageData = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
            }
        self.assertEqual(actual, expected)


    def test_extract_page_data_some_data(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><h1>This is the header</h1><body>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected: ExtractedPageData = {
            "url": "https://crawler-test.com",
            "heading": "This is the header",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
            }
        self.assertEqual(actual, expected)

    def test_extract_page_data_scant_data(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
        <img src="/image1.jpg" alt="Image 1">
        </body><p>Outside body tag</p></html>"""
        actual = extract_page_data(input_body, input_url)
        expected: ExtractedPageData = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "Outside body tag",
            "outgoing_links": [],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
            }
        self.assertEqual(actual, expected)




if __name__ == "__main__":
    unittest.main()
