import requests
from bs4 import BeautifulSoup
from pytzen.tools.webscrap import Html
from pytzen.lab import Lab
from dataclasses import dataclass, field


@dataclass
class This(Lab):
    '''Gets the last quote to ruminate from the PYTZEN blog. It is a
    tribute to "import this" in Python.
    '''

    last_quote_link: str = None
    list_line: list = field(default_factory=list)


    def _get_links(self):
        '''Gets all links from the index page and separate the last
        post.
        '''

        html = Html(url=self.url_blog)
        list_link = html.get_links()
        list_link = [link for link in list_link if 'pytzen' in str(link)]
        self.last_quote_link = list_link[0]
    

    def _get_post(self):
        '''Gets the last post html doc and separate the blockquote.
        '''
        
        html_doc = requests.get(self.last_quote_link).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        last_quote = soup.find_all('blockquote')[0]
        list_line = last_quote.find_all('p')
        self.list_line = [line.text for line in list_line]


    def run(self):
        '''Prints the last quote from the PYTZEN blog.
        '''

        self._get_links()
        self._get_post()

        print('\n'.join(self.list_line))


this = This()
this.run()