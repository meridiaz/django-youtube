from django.apps import AppConfig
import sys
from urllib.request import urlopen
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import urllib


class YoutubeHandler(ContentHandler):
    def meterBS(self):
        from .models import Video
        print("meter en la base de datos")
        v = Video(titulo = self.title, link = self.link)
        v.save()

    def __init__ (self):
        self.inEntry = False
        self.inContent = False
        self.content = ""
        self.title = ""
        self.link = ""

    def startElement (self, name, attrs):
        if name == 'entry':
            self.inEntry = True
        elif self.inEntry:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.link = attrs.get('href')#se puede poner eso cuando tengamos una
                #palabra clave href o title normalmente en naranja

    def endElement (self, name):
        global videos
        if name == 'entry':
            self.inEntry = False
            self.meterBS()
        elif self.inEntry:
            if name == 'title':
                self.title = self.content
                self.content = ""
                self.inContent = False

    def characters (self, chars):
        if self.inContent:
            self.content = self.content + chars

class CmsConfig(AppConfig):
    name = 'cms'
    def ready(self):
        from .models import Video
        print('runserver' in sys.argv and Video.objects.all().count()==0)
        if 'runserver' in sys.argv and Video.objects.all().count()==0:
            url = 'https://www.youtube.com/feeds/videos.xml?channel_id=' \
                + 'UC300utwSVAYOoRLEqmsprfg'
            #    + sys.argv[1]

            print("---------------------valor de url:"+url)
            xmlStream = urlopen(url)
            Parser = make_parser()
            Parser.setContentHandler(YoutubeHandler())
            Parser.parse(xmlStream)
