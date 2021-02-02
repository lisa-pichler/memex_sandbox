## Homework lesson 12
##finishing the publication pages; 
# add tables with the most similar results based on tf-idf similarities
#add wordclouds
#details page looks different than the rest; 
#use page template; add the collapsible thing
# ad wordclouds add similarities

import os, json
import pdf2image    # extracts images from PDF
import pytesseract  # interacts with Tesseract, which extracts text from images
import PyPDF2       # cleans PDFs
import yaml 
import os, json, re

import functions
import textwrap
# SCRIPT WITH OUR PREVIOUS FUNCTIONS
import functions

###########################################################
# VARIABLES ###############################################
###########################################################

settings = functions.loadYmlSettings("settings.yml")
memexPath = settings["path_to_memex"]
###########################################################
# FUNCTIONS ###############################################
###########################################################


simTemplate = """
<table id="" class="display" width="100%">
<thead>
    <tr>
        <th><i>link</i></th> 
        <th>Sim</th>
        <th>Publication</th>
    </tr>
</thead>
<tbody>
@TABLECONTENTS@
</tbody>
</table>
"""

imTemplate = """
<table id="" class="display" width="100%">
<thead>
    <tr>
        <th><i>link</i></th> 
        <th>Sim</th>
        <th>Publication</th>
    </tr>
</thead>
<tbody>
@TABLECONTENTS@
</tbody>
</table>
"""

def generatePublicationInterface(citeKey, pathToBibFile):
    print("="*80)
    print(citeKey)

    jsonFile = pathToBibFile.replace(".bib", ".json")
    with open(jsonFile, encoding="utf8") as jsonData:
        ocred = json.load(jsonData)
        pNums = ocred.keys()

        pageDic = functions.generatePageLinks(pNums)

        # load page template
        with open(settings["template_page"], "r", encoding="utf8") as ft:
            template = ft.read()

        # load individual bib record
        bibFile = pathToBibFile
        bibDic = functions.loadBib(bibFile)
        bibForHTML = functions.prettifyBib(bibDic[citeKey]["complete"])

        orderedPages = list(pageDic.keys())

        for o in range(0, len(orderedPages)):
            #print(o)
            k = orderedPages[o]
            v = pageDic[orderedPages[o]]

            pageTemp = template
            pageTemp = pageTemp.replace("@PAGELINKS@", v)
            pageTemp = pageTemp.replace("@PATHTOFILE@", "")
            pageTemp = pageTemp.replace("@CITATIONKEY@", citeKey)

            if k != "DETAILS":
                mainElement = '<img src="@PAGEFILE@" width="100%" alt="">'.replace("@PAGEFILE@", "%s.png" % k)
                pageTemp = pageTemp.replace("@MAINELEMENT@", mainElement)
                pageTemp = pageTemp.replace("@OCREDCONTENT@", ocred[k].replace("\n", "<br>"))
            else:
                mainElement = bibForHTML.replace("\n", "<br> ")
                mainElement = '<div class="bib">%s</div>' % mainElement
                mainElement += '\n<img src="../@CITATIONKE@_wCloud.jpg" width="80%" alt="wordcloud">'
                pageTemp = pageTemp.replace("@MAINELEMENT@", mainElement)
                pageTemp = pageTemp.replace("@OCREDCONTENT@", "")

                pageTemp = pageTemp.replace("@CONNECTEDTEXTS@", simTemplate.replace("@TABLECONTENTS@",genConnectedTexts(citeKey)))
                

            # @NEXTPAGEHTML@ and @PREVIOUSPAGEHTML@
            if k == "DETAILS":
                nextPage = "0001.html"
                prevPage = ""
            elif k == "0001":
                nextPage = "0002.html"
                prevPage = "DETAILS.html"
            elif o == len(orderedPages)-1:
                nextPage = ""
                prevPage = orderedPages[o-1] + ".html"
            else:
                nextPage = orderedPages[o+1] + ".html"
                prevPage = orderedPages[o-1] + ".html"

            pageTemp = pageTemp.replace("@NEXTPAGEHTML@", nextPage)
            pageTemp = pageTemp.replace("@PREVIOUSPAGEHTML@", prevPage)

            pagePath = os.path.join(pathToBibFile.replace(citeKey+".bib", ""), "pages", "%s.html" % k)
            with open(pagePath, "w", encoding="utf8") as f9:
                f9.write(pageTemp)



def genConnectedTexts(citeKey):  
    similarities = json.load(open("cosineTableDic_filtered.txt", "r", encoding="utf8"))
    contentTemp = "<tr><td><i><a href='@link@'>read</a></i></td><td>@Sim@</td><td>@Publication@</td></tr>"
    
    if similarities:
        temp = similarities[citeKey]
        content = ""
    
        for k,v in temp.items():
            content = content + contentTemp.replace("@Publication@", k)
            content = content.replace("@Sim@", str(v))
            link = "..\\..\\..\\..\\." + functions.generatePublPath(memexPath, k) + "\\pages\\DETAILS.html"
            content = content.replace("@link@", link)
    return(content)       
        
