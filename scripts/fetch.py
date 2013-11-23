import json, os, re, urllib2
from utils import download, write
from lxml.html import fromstring
from extract import convert

def retrieve(url):
    doc = fromstring(download(url))
    items = doc.xpath("//table[@class='dates_n_proceedings']/tr")
    data = []
    
    for item in items:
        info = item.xpath("td")
        if len(info) == 0:
            continue
        date = info[0].xpath("text()")[0]
        link = info[1].xpath("a")
        if len(link) == 0:
            continue
        link = link[0]
        title = link.xpath("text()")[0]
        if "amic" in title:
            org = re.search("curiae of (.*?) (\(|filed)", title).group(1)
            href = link.xpath("@href")[0]
            
            if not os.path.exists(os.getcwd() + "/briefs/" + org + ".pdf"):
                print "Downloading pdf for", org
                pdf = urllib2.urlopen(href).read()
                f = open(os.getcwd() + "/briefs/" + org + ".pdf", "wb")
                f.write(pdf)
                f.close()                            
                
            brief = { 
                "date": date,
                "author": org,
                "url": href,
                "pdf": os.getcwd() + "/briefs/" + org + ".pdf"
            }
            
            #extract
            try:
                convert(os.getcwd() + "/briefs/" + org + ".pdf", os.getcwd() + "/data/briefs/" + org)
                print "Converted", org
            except:
                print "Error converting", org
                
            data.append(brief)
    write(json.dumps(data, indent=2), "briefs.json")    

retrieve('http://www.scotusblog.com/case-files/cases/windsor-v-united-states-2')

