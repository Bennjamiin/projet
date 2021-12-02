import pathlib
import requests
import webbrowser
from wordcloud import WordCloud
from bs4 import BeautifulSoup

class Traitement():

    def load(self, array):
        self.array = array


    """
    Partie text
    """
    def run(self):
        self.wordcloud = []
        
        pathlib.Path('wc').mkdir(parents=False, exist_ok=True) 
        k=0
        for i in self.array:
            
            wc = WordCloud(max_font_size=72).generate(i)
            
            save_dir = f"wc/{k}.png"
            
            
            wc.to_file(save_dir)

            self.wordcloud.append(save_dir)

            k+=1
            
            
            
            
    
    def show(self):

        base = """
                <html>
                    <head>
        
                    </head>
                </html> 
                """
        
        soup = BeautifulSoup(base, features="html.parser")
        
        for i in self.wordcloud:
            new_image = soup.new_tag("img", src=i, style="display:block")
            soup.head.append(new_image)        
            soup.head.append(soup.new_tag('br'))

        with open("result.html", "w") as f:
            f.truncate(0)
            f.write(str(soup))
        
        webbrowser.open('result.html')


    """
    Partie image
    """

    def runimg(self):
        self.image=[]
        pathlib.Path('img').mkdir(parents=False, exist_ok=True) 
        k=0
        for site in self.array:
            for i in site:
                file_ext = i.split('.')[-1]
                with open(f'img/{k}.{file_ext}', 'wb') as f:
                    f.write(requests.get(i).content)

                self.image.append(f"img/{k}.{file_ext}")
                k+=1
                

    def showimg(self):
        base = """
                <html>
                    <head>
        
                    </head>
                </html> 
                """ 
        
        soup = BeautifulSoup(base, features="html.parser")

        for i in self.image:
            new_image = soup.new_tag("img", src=i, style="display:block")
            soup.head.append(new_image)        
            soup.head.append(soup.new_tag('br'))

        with open("result.html", "w") as f:
            f.truncate(0)
            f.write(str(soup))
        
        webbrowser.open('result.html')