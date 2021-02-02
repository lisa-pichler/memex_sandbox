# program for starting age; index.html
# main entry point to our memex
# join index page template with the index page content
import os, json
import pdf2image, pytesseract
import functions 
import yaml
import remove_comments
### variables
settingsFile = "config_MA_new.yml"
settings = yaml.safe_load(open(settingsFile))

def generateIndexInterface(....):
    # load page template
    with open(settings["template_index"], "r", encoding="utf8") as ft:
        template = ft.read()
    
    #load index content; then connect
    with open(settings["contend_index"], "r", encoding="utf8") as ft:
        template = ft.read()

    #connect as: index.html to get the starting page


def generateContents (...):
    #generate a list of publications with links 
    #join it with the index page template
    # shoud look like this: <li><a href="@PATHTOPUBL@/pages/DETAILS.html">[@CITEKEY@]</a> @AUTHOR@ (@DATE@) - <i>@TITLE@</i></li>
    #load the bib file to get all the values
    # load the index template file 
    # write the <li> etc. into the content 
    # replace @author with author etc.
    # open as contents.html 

    # #
####
#### Pseudocode: 
#### funkion: 
#### template öffnen
#### @PATHTOPUBL@, [@CITEKEY@], @AUTHOR@ (@DATE@) @TITLE@ + Link zur details(.html) des Textes
#### dictionary mit diesen variablen 
#### loop um jeweils einen citekey/text/
#### Input: citekey,Path zum file, usw. -> Output Liste
###         
        # load individual bib record
       # bibFile = pathToBibFile
        #bibDic = functions.loadBib(bibFile)
        #bibForHTML = functions.prettifyBib(bibDic[citeKey]["complete"])
####                
         #   pageTemp = template
          #  pageTemp = pageTemp.replace("@PATHTOPUBL@", v)
            #pageTemp = pageTemp.replace("@CITEKEY@", v)
           #pageTemp = pageTemp.replace("@AUTHOR@", v)
            #pageTemp = pageTemp.replace("@DATE@", v)
            #pageTemp = pageTemp.replace("@TITLE@", v)
        detailfileDic = functions.generatePageLinks(pNums)
###        # load page template # wir brauchen template_index.html
        with open(settings["template_index"], "r", encoding="utf8") as ft:
            template = ft.read()
        # load page template
        #with open(settings["template_page"], "r", encoding="utf8") as ft:
            #template = ft.read()
        # load individual bib record
        bibFile = pathToBibFile
        bibDic = functions.loadBib(bibFile)
        bibForHTML = functions.prettifyBib(bibDic[citeKey]["complete"])
        orderedPages = list(detailfileDic.keys())
        for o in range(0, len(orderedPages)):
            #print(o)
            k = orderedPages[o]
            v = pageDic[orderedPages[o]]
            pageTemp = template
            pageTemp = pageTemp.replace("@PAGELINKS@", v)
            pageTemp = pageTemp.replace("@PATHTOFILE@", "")
            pageTemp = pageTemp.replace("@CITATIONKEY@", citeKey)
def generateDetailsLinks(pNumList):
    detailsDic = {}
    listMod.extend()
#   add bib rec + link to details.html for each record to dictionay
#   k= <li><a href="@PATHTOPUBL@/pages/DETAILS.html">[@CITEKEY@]</a> @AUTHOR@ (@DATE@) - <i>@TITLE@</i></li>, v= path to details.html
    return(pageDic)