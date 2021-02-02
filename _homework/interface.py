# python file to generate interface for memex machine
# merges together page images, ocr-ed text, bibliographical info
# into a simple HTML based interface
## the one we worked on;
import os, json
import pdf2image, pytesseract
import functions 
import yaml
import remove_comments
### variables
settingsFile = "config_MA_new.yml"
settings = yaml.safe_load(open(settingsFile))

memexPath = settings["path_to_memex"]


# generate interface for the publication
def generatePublicationInterface(citeKey, pathToBibFile):              # function takes a citation key and path to bib file
    print("="*80)
    print(citeKey)

    jsonFile = pathToBibFile.replace(".bib", ".json")
    with open(jsonFile, encoding="utf8") as jsonData:                  #add encoding to not get error; 
        ocred = json.load(jsonData)
        pNums = ocred.keys()

        pageDic = functions.generatePageLinks(pNums)                    # number of pages of each publication;links to make it navigatable

        # load page template
        with open(settings["template_page"], "r", encoding="utf8") as ft:
            template = ft.read()

        # load individual bib record
        bibFile = pathToBibFile
        bibDic = functions.loadBib(bibFile)                              #loads entire bib
        bibForHTML = functions.prettifyBib(bibDic[citeKey]["complete"])  #makes the bib file look better for this view

        orderedPages = list(pageDic.keys())                               #list of all keys and pagenummers from page dic

        for o in range(0, len(orderedPages)):                             #long loop that creates every single page
            #print(o)
            k = orderedPages[o]
            v = pageDic[orderedPages[o]]

            pageTemp = template                                           # take a template
            pageTemp = pageTemp.replace("@PAGELINKS@", v)                 # replace values in template
            pageTemp = pageTemp.replace("@PATHTOFILE@", "")
            pageTemp = pageTemp.replace("@CITATIONKEY@", citeKey)

            if k != "DETAILS":                                             #one page is different than the rest;this for regular
                mainElement = '<img src="@PAGEFILE@" width="100%" alt="">'.replace("@PAGEFILE@", "%s.png" % k)
                pageTemp = pageTemp.replace("@MAINELEMENT@", mainElement)
                pageTemp = pageTemp.replace("@OCREDCONTENT@", ocred[k].replace("\n", "<br>")) 
            else:                                                                             # if pages is details.html           
                mainElement = bibForHTML.replace("\n", "<br> ")
                mainElement = '<div class="bib">%s</div>' % mainElement                       # class for changes in style sheet
                mainElement += '\n<img src="wordcloud.jpg" width="100%" alt="wordcloud">'     #wordcloud we will generate in the next class
                pageTemp = pageTemp.replace("@MAINELEMENT@", mainElement)
                pageTemp = pageTemp.replace("@OCREDCONTENT@", "")

            # @NEXTPAGEHTML@ and @PREVIOUSPAGEHTML@  #links to next and previous page; and when we are on the last it stops
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

            pageTemp = pageTemp.replace("@NEXTPAGEHTML@", nextPage) ##find replace in template
            pageTemp = pageTemp.replace("@PREVIOUSPAGEHTML@", prevPage)

            pagePath = os.path.join(pathToBibFile.replace(citeKey+".bib", ""), "pages", "%s.html" % k) # saves the actual page
            with open(pagePath, "w", encoding="utf8") as f9:
                f9.write(pageTemp)
                
###test##generatePublicationInterface("baggeOldNorseKings2016","C:\\Users\\LisaP\\OneDrive\\Documents\\DHprogramming\\memex_sandbox\\_data\\b\\ba\\baggeOldNorseKings2016\\baggeOldNorseKings2016.bib")
def processAll(pathToMemex):
    pathData = functions.dicOfRelevantFiles(memexPath, ".bib")
    print(pathData)
    
   
    for k, v in pathData.items():
        generatePublicationInterface(k, v)

processAll(memexPath)



   
       
    


