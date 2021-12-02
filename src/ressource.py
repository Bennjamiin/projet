import requests
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
from io import BytesIO
from requests_html import HTMLSession
from urllib.parse import urljoin
import pdfminer

class Ressource():

    def __init__(self, url):
        """
        Initialize the object with the url cause it will be reused
        Then it makes a request to the url to check object type

        If it's HTML, it justs update the object type
        If it's PDF, it saves object type, pdf filename and the content cause it will be reused
        """

        self.url = url

        r = requests.get(self.url)
        content_type = r.headers.get('content-type')

        if 'application/pdf' in content_type:
            self.obj_type = "PDF"
            self.pdf_name = self.url.split('/')[-1]
            self.pdf_content = r.content

        elif 'text/html' in content_type:
            self.obj_type = "HTML"
            
        else :
            self.obj_type = "Non supporté" 


    def type(self):
        """
        Used to return the object type
        """
        return self.obj_type
    
    
    def text(self):
        """
        Return string corresponding to the content of the object

        1. It checks the object type :
        2. If it's HTML it makes a request to get content, then remove all html tags and so on, and return plain text as string
        3. If it's PDF it first download the file, then juste extracts plain text and return it as string
        """

        if self.obj_type == "HTML" :
            r = requests.get(self.url)
            raw_html = r.text
            html_page = BeautifulSoup(raw_html, features="html.parser")

            for s in html_page.select('script'):
                s.extract()
            
            for s in html_page.select('style'):
                s.extract()
            
            return html_page.get_text()
        
        elif self.obj_type == "PDF" :

            pdf = BytesIO(self.pdf_content)
            return extract_text(pdf)
    
    def image(self):
        """
        Returns all image URLs on a single `url`
        """
    
        if self.obj_type == "HTML" :
    
            self.img_urls = []
            session = HTMLSession()
            
            response = session.get(self.url)
            
            response.html.render(timeout=20)
            
            soup = BeautifulSoup(response.html.html, "html.parser")
            
            for img in soup.find_all("img"):
                img_url = img.attrs.get("src") or img.attrs.get("data-src") or img.attrs.get("data-original")
                
                if not img_url:
                    continue

                img_url = urljoin(self.url, img_url)

                try:
                    pos = img_url.index("?")
                    img_url = img_url[:pos]
                except ValueError:
                    pass

                self.img_urls.append(img_url)

            session.close()
            return self.img_urls