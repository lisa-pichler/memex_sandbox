# program to import functions
# code reuse ; has to be in folder with other scripts
#############################
# STORING FUNCTIONS #########
#############################

import os
import PyPDF2
import functions
import yaml 
import re
import shutil

#add yaml function


# generate path from bibtex code:
def generatePublPath(pathToMemex, bibTexCode):
    temp = bibTexCode.lower()
    directory = os.path.join(pathToMemex, temp[0], temp[:2], bibTexCode)
    return(directory)


# progarm to create a dictionary
def loadBib(bibTexFile):

    bibDic = {}
    recordsNeedFixing = []

    with open("memex_bibtex.bib", "r", encoding="utf8") as f1:
        records = f1.read().split("\n@")

        for record in records[1:]:
            # let process ONLY those records that have PDFs
            if ".pdf" in record.lower():
                completeRecord = "\n@" + record

                record = record.strip().split("\n")[:-1]

                rType = record[0].split("{")[0].strip()
                rCite = record[0].split("{")[1].strip().replace(",", "")

                bibDic[rCite] = {}
                bibDic[rCite]["rCite"] = rCite
                bibDic[rCite]["rType"] = rType
                bibDic[rCite]["complete"] = completeRecord

                for r in record[1:]:
                    key = r.split("=")[0].strip()
                    val = r.split("=")[1].strip()
                    val = re.sub("^\{|\},?", "", val)

                    bibDic[rCite][key] = val

                    # fix the path to PDF
                    if key == "file":
                        if ";" in val:
                            #print(val)
                            temp = val.split(";")

                            for t in temp:
                                if ".pdf" in t:
                                    val = t

                            bibDic[rCite][key] = val

    print("="*80)
    print("NUMBER OF RECORDS IN BIBLIGORAPHY: %d" % len(bibDic))
    print("="*80)
    return(bibDic)

# function to generate page links
def generatePageLinks(pNumList):
    listMod = ["DETAILS"]
    listMod.extend(pNumList)

    toc = []
    for l in listMod:
        toc.append('<a href="%s.html">%s</a>' % (l, l))
    toc = " ".join(toc)

    pageDic = {}
    for l in listMod:
        pageDic[l] = toc.replace('>%s<' % l, ' style="color: red;">%s<' % l)

    return(pageDic)

# html friendly BIB; makes bib record more readable 
def prettifyBib(bibText):
    bibText = bibText.replace("{{", "").replace("}}", "")
    bibText = re.sub(r"\n\s+file = [^\n]+", "", bibText)
    bibText = re.sub(r"\n\s+abstract = [^\n]+", "", bibText)
    return(bibText)

# dictionary of citation keys; paths to specific files
def dicOfRelevantFiles(pathToMemex, extension):

    dic = {}
    for subdir, dirs, files in os.walk(pathToMemex):
        for file in files:
            # process publication tf data
            if file.endswith(extension):
                key = file.replace(extension, "")
                value = os.path.join(subdir, file)
                dic[key] = value
    return(dic)

## function for bibrecord

def processBibRecord(pathToMemex, bibRecDict):
    tempPath = generatePublPath(pathToMemex, bibRecDict["rCite"])

    print("="*80)
    print("%s :: %s" % (bibRecDict["rCite"], tempPath))
    print("="*80)

    if not os.path.exists(tempPath):
        os.makedirs(tempPath)

        bibFilePath = os.path.join(tempPath, "%s.bib" % bibRecDict["rCite"])
        with open(bibFilePath, "w", encoding="utf8") as f9:
            f9.write(bibRecDict["complete"])

        pdfFileSRC = bibRecDict["file"]

        #betterbibtex escaped: , this line replaces "\:" with ":"
        pdfFileSRC = pdfFileSRC.replace("\\:", ":")

        pdfFileDST = os.path.join(tempPath, "%s.pdf" % bibRecDict["rCite"])
        if not os.path.isfile(pdfFileDST): # this is to avoid copying that had been already copied.
            shutil.copyfile(pdfFileSRC, pdfFileDST)
    return(bibFilePath)

def loadYmlSettings(ymlFile):
    with open("config_MA_new.yml", "r", encoding="utf8") as f1:
        data = f1.read()
        data = re.sub(r"#.*", "", data) # remove comments
        data = re.sub(r"\n+", "\n", data) # remove extra linebreaks used for readability
        data = re.split(r"\n(?=\w)", data) # splitting
        dic = {}
        for d in data:
            if ":" in d:
                d = re.sub(r"\s+", " ", d.strip())
                d = re.split(r"^([^:]+) *:", d)[1:]
                key = d[0].strip()
                value = d[1].strip()
                dic[key] = value
    #input(dic)
    return(dic)

def filterDic(dic, thold):
    retDic = {}    #empty Dictonary to copy filterd values into
    for k,v in dic.items():     #loop through outer first dic, containig the titles
        retDic[k]={}            #create a subDic for each title
        for key,val in v.items():   #loop through the entries of each title
            if val > thold:         #check threshold
                if val < 0.97:        #check to not match the publication with itself
                    retDic[k][key] = val    #add value
    return(retDic)

def memexStatusUpdates(pathToMemex, fileType):
    # collect stats
    NumberOfPublications = len(listOfRelevantFiles(pathToMemex, ".pdf")) # PDF is the main measuring stick
    NumberOfCountedItems = len(listOfRelevantFiles(pathToMemex, fileType))

    currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # check if dictionary exists
    dicFile = os.path.join(pathToMemex, "memex.status")
    if os.path.isfile(dicFile):
        dic = json.load(open(dicFile))
    else:
        dic = {}

    dic[fileType] = {}
    dic[fileType]["files"] = NumberOfCountedItems
    dic[fileType]["pdfs"] = NumberOfPublications
    dic[fileType]["time"] = currentTime

    # save dic
    with open(dicFile, 'w', encoding='utf8') as f9:
        json.dump(dic, f9, sort_keys=True, indent=4, ensure_ascii=False)

    print("="*40)
    print("Memex Stats have been updated for: %s" % fileType)
    print("="*40)

# the function will quickly remove all files with a certain
# extension --- useful when messing around and need to delete
# lots of temporary files


def removeFilesOfType(pathToMemex, fileExtension):
    if fileExtension in [".pdf", ".bib"]:
        sys.exit("files with extension %s must not be deleted in batch!!! Exiting..." % fileExtension)
    else:
        for subdir, dirs, files in os.walk(pathToMemex):
            for file in files:
                # process publication tf data
                if file.endswith(fileExtension):
                    pathToFile = os.path.join(subdir, file)
                    print("Deleting: %s" % pathToFile)
                    os.remove(pathToFile)

def loadMultiLingualStopWords(listOfLanguageCodes):
    print("Loading stopwords...")
    stopwords = []
    pathToFiles = settings["stopwords"]
    codes = json.load(open(os.path.join(pathToFiles, "languages.json")))

    for l in listOfLanguageCodes:
        with open(os.path.join(pathToFiles, codes[l]+".txt"), "r", encoding="utf8") as f1:
            lang = f1.read().strip().split("\n")
            stopwords.extend(lang)

    stopwords = list(set(stopwords))
    print("\tStopwords for: ", listOfLanguageCodes)
    print("\tNumber of stopwords: %d" % len(stopwords))
    #print(stopwords)
    return(stopwords)         

def generatePublicationInterface(citeKey, pathToBibFile):
    print("="*80)
    print(citeKey)

    jsonFile = pathToBibFile.replace(".bib", ".json")
    with open(jsonFile, encoding="utf8") as jsonData:
        ocred = json.load(jsonData)
        pNums = ocred.keys()

        pageDic = generatePageLinks(pNums)

        # load page template
        with open(settings["template_page"], "r", encoding="utf8") as ft:
            template = ft.read()

        # load individual bib record
        bibFile = pathToBibFile
        bibDic = functions.loadBib(bibFile)
        bibForHTML = prettifyBib(bibDic[citeKey]["complete"])

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
                mainElement += '\n<img src="wordcloud.jpg" width="100%" alt="wordcloud">'
                pageTemp = pageTemp.replace("@MAINELEMENT@", mainElement)
                pageTemp = pageTemp.replace("@OCREDCONTENT@", "")

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
