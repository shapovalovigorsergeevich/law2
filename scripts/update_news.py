import json,re,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from html.parser import HTMLParser

KEYWORDS=("недвиж","квартир","жиль","земел","участ","аренд","строитель","долев","собственност","ипотек","апартамент","росреестр")

def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 legal-news-updater"})
    with urllib.request.urlopen(req,timeout=30) as r:return r.read()

def consultant():
    root=ET.fromstring(get("https://www.consultant.ru/rss/nw.xml"))
    out=[]
    for item in root.findall(".//item"):
        title=" ".join((item.findtext("title") or "").split())
        desc=" ".join(re.sub("<[^>]+>"," ",item.findtext("description") or "").split())
        link=item.findtext("link") or "https://www.consultant.ru/legalnews/jur/"
        if any(k in (title+" "+desc).lower() for k in KEYWORDS):
            pub=item.findtext("pubDate") or ""
            out.append({"source":"КонсультантПлюс","date":pub[:16],"title":title,"description":desc[:320],"url":link})
    return out[:12]

class Links(HTMLParser):
    def __init__(self):
        super().__init__();self.items=[];self.href=None;self.text=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a":
            d=dict(attrs);h=d.get("href","")
            if "/press_center/news/" in h or re.match(r"/news/\d+",h):
                self.href=h;self.text=[]
    def handle_data(self,data):
        if self.href:self.text.append(data)
    def handle_endtag(self,tag):
        if tag=="a" and self.href:
            title=" ".join("".join(self.text).split())
            if title and any(k in title.lower() for k in KEYWORDS):
                h=self.href if self.href.startswith("http") else "https://www.vsrf.ru"+self.href
                self.items.append({"source":"Верховный Суд РФ","date":"","title":title,"description":"Материал опубликован на официальном сайте Верховного Суда Российской Федерации.","url":h})
            self.href=None;self.text=[]

def supreme():
    p=Links();p.feed(get("https://www.vsrf.ru/press_center/news/").decode("utf-8","ignore"))
    return p.items[:12]

items=consultant()+supreme()
seen=set();clean=[]
for n in items:
    key=n["url"]
    if key not in seen:
        seen.add(key);clean.append(n)
clean=clean[:18]
data={"updated_at":datetime.now(timezone.utc).astimezone().strftime("%d.%m.%Y %H:%M"),"items":clean}
with open("data/news.json","w",encoding="utf-8") as f:json.dump(data,f,ensure_ascii=False,indent=2)
