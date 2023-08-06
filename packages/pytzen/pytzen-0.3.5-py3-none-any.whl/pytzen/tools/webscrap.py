from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup


@dataclass
class Html:
    '''Works with HTML parsing methods.
    '''

    url: str = None
    link_type: str = 'href'


    def get_links(self):
        '''Gets the links list from a URL.
        '''
        
        html_doc = requests.get(self.url).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        list_link = [link.get(self.link_type) for link in soup.find_all('a')]
        
        return list_link