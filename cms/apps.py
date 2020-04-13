from django.apps import AppConfig
import sys
from urllib.request import urlopen
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

seguir = True


def deleteDB():
    from .models import Video, CanalYT
    if Video.objects.count() != 0:
        CanalYT.objects.all().delete()


class YoutubeHandler(ContentHandler):
    def meterBSVideo(self):
        from .models import Video, CanalYT

        if self.canal == "":
            c = CanalYT(titulo=self.CanalTit, link=self.CanalLink)
            c.save()
            self.canal = c
        v = Video(canal=self.canal, titulo=self.title, link=self.link,
                  ytid=self.ytid, img=self.img, fechaPub=self.fechaPub,
                  descri=self.descrip)
        v.save()

    def __init__(self):
        self.inEntry = False
        self.inContent = False
        self.content = ""
        self.title = ""
        self.link = ""
        self.ytid = ""
        self.inCanal = False
        self.CanalTit = ""
        self.CanalLink = ""
        self.inContentCanal = False
        self.img = ""
        self.descrip = ""
        self.canal = ""

    def startElement(self, name, attrs):
        if name == 'entry':
            self.inEntry = True
        elif self.inEntry:
            if name == 'title' or name == 'yt:videoId'  \
              or name == "media:description" or name == "published":
                self.inContent = True
            elif name == 'link':
                self.link = attrs.get('href')
            elif name == "media:thumbnail":
                self.img = attrs.get('url')
        elif name == "feed":
            self.inCanal = True
        elif self.inCanal:
            if name == "title":
                self.inContent = True
            elif name == "link" and (attrs.get('rel') == "alternate"):
                self.CanalLink = attrs.get('href')

    def endElement(self, name):
        if name == 'entry':
            self.inEntry = False
            self.meterBSVideo()
        elif self.inEntry:
            if name == 'title':
                self.title = self.content
                self.content = ""
                self.inContent = False
            elif name == "yt:videoId":
                self.ytid = self.content
                self.content = ""
                self.inContent = False
            elif name == "media:description":
                self.descrip = self.content
                self.content = ""
                self.inContent = False
            elif name == "published":
                self.fechaPub = self.content
                self.content = ""
                self.inContent = False
        elif name == "feed":
            self.inCanal = False
        elif self.inCanal:
            if name == "title":
                self.CanalTit = self.content
                self.inContent = False
                self.content = ""

    def characters(self, chars):
        if self.inContent:
            self.content = self.content + chars


class CmsConfig(AppConfig):
    name = 'cms'

    def ready(self):
        from .models import Video
        global seguir
        if 'runserver' in sys.argv and seguir:
            url = 'https://www.youtube.com/feeds/videos.xml?channel_id=' \
                + 'UC300utwSVAYOoRLEqmsprfg'
            print("---------------------valor de url:"+url)
            deleteDB()
            xmlStream = urlopen(url)
            Parser = make_parser()
            Parser.setContentHandler(YoutubeHandler())
            Parser.parse(xmlStream)
            seguir = False
