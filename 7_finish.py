#memex homework 12
#last step finishing the interface

import pdf2image    # extracts images from PDF
import pytesseract  # interacts with Tesseract, which extracts text from images
import PyPDF2       # cleans PDFs
import yaml 
import os, json
import functions
### python script to add the searches to the html; run this again to get all the searches
###Settings
generalTemplate = """
<button class="collapsible">@ELEMENTHEADER@</button>
<div class="content">
@ELEMENTCONTENT@
</div>
"""
searchesTemplate = """
<button class="collapsible">SAVED SEARCHES</button>
<div class="content">
<table id="" class="display" width="100%">
<thead>
    <tr>
        <th><i>link</i></th>
        <th>search string</th>
        <th># of publications with matches</th>
        <th>time stamp</th>
    </tr>
</thead>
<tbody>
@TABLECONTENTS@
</tbody>
</table>
</div>
"""


settingsFile = "config_MA_new.yml"
settings = yaml.safe_load(open(settingsFile))

memexPath = settings["path_to_memex"]
#language = settings["language_keys"]
#defaultLang = settings["defaultLang"]


def createIndex(pathToMemex):
    bibData = functions.loadBib(settings["bib_all"])
    with open(settings["template_index"], "r", encoding="utf8") as ft:
        template = ft.read()
    completeList = []
    for k,v in bibData.items():         
        path = functions.generatePublPath(memexPath, k)     
        entry = "<li><a href="+"@PATHTOPUBL@/pages/DETAILS.html"+">[@CITEKEY@]</a> @AUTHOR@ (@DATE@) - <i>@TITLE@</i></li>"
        entry = entry.replace("@PATHTOPUBL@", path)
        entry = entry.replace("@CITEKEY@", k)
        if "author" in v: 
            entry = entry.replace("@AUTHOR@", v["author"])
        else:
            entry = entry.replace("@AUTHOR@", "MISSING")
        if "year" in v: 
            entry = entry.replace("@DATE@", v["year"])
        else:
            entry = entry.replace("@DATE@", "MISSING")
        if "title" in v: 
            entry = entry.replace("@TITLE@", v["title"])
        else:
            entry = entry.replace("@TITLE@", "MISSING")
        completeList.append(entry)
    content = "\n<ul>\n%s\n</ul>" % "\n".join(sorted(completeList))
    content = content.replace("{","")
    content = content.replace("}","")
    toc = formatSearches(pathToMemex)
    template = template.replace("@SEARCHES@", toc)
    template = template.replace("@PUBLICATIONS@", content)
    with open(os.path.join(pathToMemex, "searchesInterface.html"), "w", encoding="utf8") as f9:
        f9.write(template)
def processAllEntries(pathToMemex):
    bibData = functions.loadBib(settings["bib_all"])    #loads the bib file
    for k,v in bibData.items():      
        path = functions.generatePublPath(memexPath, k)
        path = path + "\\" + k +".bib" 
        functions.generatePublicationInterface(k, path)    
# generate search pages and TOC


def formatSearches(pathToMemex):
    with open(settings["template_search"], "r", encoding="utf8") as f1:
        indexTmpl = f1.read()
    dof = functions.dicOfRelevantFiles(pathToMemex, ".searchResults")
    toc = []
    for file, pathToFile in dof.items():
        searchResults = []
        data = json.load(open(pathToFile, encoding="utf8"))
        # collect toc
        template = "<tr> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td></tr>"
        linkToSearch = os.path.join(".\\searches", file+".html") ##removed _data from Alex script, replace dot
        pathToPage = '<a href="%s"><i>read</i></a>' % linkToSearch
        searchString = '<div class="searchString">%s</div>' % data.pop("searchString")
        timeStamp = data.pop("timestamp")
        tocItem = template % (pathToPage, searchString, len(data), timeStamp)
        toc.append(tocItem)
        # generate the results page
        keys = sorted(data.keys(), reverse=True)
        for k in keys:
            searchResSingle = []
            results = data[k]
            temp = k.split("::::")
            header = "%s (pages with results: %d)" % (temp[1], int(temp[0]))
            for page, excerpt in results.items():
                pdfPage = int(page)
                linkToPage = '<a href="../%s"><i>go to the original page...</i></a>' % excerpt["pathToPage"]
                searchResSingle.append("<li><b><hr>(pdfPage: %d)</b><hr> %s <hr> %s </li>" % (pdfPage, excerpt["result"], linkToPage))
            searchResSingle = "<ul>\n%s\n</ul>" % "\n".join(searchResSingle)
            searchResSingle = generalTemplate.replace("@ELEMENTHEADER@", header).replace("@ELEMENTCONTENT@", searchResSingle)
            searchResults.append(searchResSingle)
        searchResults = "<h2>SEARCH RESULTS FOR: <i>%s</i></h2>\n\n" % searchString + "\n\n".join(searchResults)
        with open(pathToFile.replace(".searchResults", ".html"), "w", encoding="utf8") as f9:
            f9.write(indexTmpl.replace("@MAINCONTENT@", searchResults))
    toc = searchesTemplate.replace("@TABLECONTENTS@", "\n".join(toc))
    return(toc)
#processAllEntries(memexPath)
createIndex(memexPath)