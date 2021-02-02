# NEW LIBRARIES
import pdf2image
import pytesseract

import os, yaml, json, random

import functions

###########################################################
# VARIABLES ###############################################
###########################################################

settingsFile = "config_MA_new.yml"                                                    ## loads my yaml file with the settings
settings = yaml.safe_load(open(settingsFile))

memexPath = settings["path_to_memex"]                               ## loads settings yaml with keys

memexPath = settings["path_to_memex"]                               ## path to memex folder in settings file
langKeys = yaml.load(open(settings["language_keys"]))               ## loads yaml file with the languages from my bib file

###########################################################
# TRICKY FUNCTIONS ########################################
###########################################################

def ocrPublication(pathToMemex, citationKey, language):                                   ## ocr function takes path, citationkey and language as argument
    publPath = functions.generatePublPath(pathToMemex, citationKey)                       ## generates path that gets us to the file with the citekey name
    pdfFile  = os.path.join(publPath, citationKey + ".pdf")                               ## generates pdf
    jsonFile = os.path.join(publPath, citationKey + ".json")                              ## generates json file
    saveToPath = os.path.join(publPath, "pages")                                          ## creates new folder for all the ocr-ed pages

    if not os.path.isfile(jsonFile):                                                      ## checks if there is a json file to see if it has been ocr-ed already
        if not os.path.exists(saveToPath):                                                ## if not it makes one and starts the process
            os.makedirs(saveToPath)
        
        print("\t>>> OCR-ing: %s" % citationKey)                                          ## shows us that it is ocr-ing the pdf and the citationkey of that one

        textResults = {}                                                                  ## creates dictionary for results
        images = pdf2image.convert_from_path(pdfFile)                                     ## creates the images of the single pages in the pdf
        pageTotal = len(images)                                                           ## to know how many pages have been processed; always adds 1
        pageCount = 1
        for image in images:                                                              ## loops through the images
            text = pytesseract.image_to_string(image, lang=language)                      ## analyses the string with the given language 
            textResults["%04d" % pageCount] = text

            image = image.convert('1') # binarizes image, reducing its size
            finalPath = os.path.join(saveToPath, "%04d.png" % pageCount)                  ## saves the pages into pages folder
            image.save(finalPath, optimize=True, quality=10)

            print("\t\t%04d/%04d pages" % (pageCount, pageTotal))
            pageCount += 1

        with open(jsonFile, 'w', encoding='utf8') as f9:
            json.dump(textResults, f9, sort_keys=True, indent=4, ensure_ascii=False)      ## dumps results into json file
    
    else:
        print("\t>>> %s has already been OCR-ed..." % citationKey)                        ## if it finds the json file in the beginning it prints this

def identifyLanguage(bibRecDict, fallBackLanguage):                                       ## function to identify language; or add a default language if it is not given
    if "langid" in bibRecDict:
        try:
            language = langKeys[bibRecDict["langid"]]                                    ## if it finds key langid(or whatever it is called in my bib file) it prints the language
            message = "\t>> Language has been successfuly identified: %s" % language
        except:
            message = "\t>> Language ID `%s` cannot be understood by Tesseract; fix it and retry\n" % bibRecDict["langid"] # if it does not know -
            message += "\t>> For now, trying `%s`..." % fallBackLanguage                                                   # goes back to a default language
            language = fallBackLanguage
    else:
        message = "\t>> No data on the language of the publication"                        ## if there is no attribute language in my bib record
        message += "\t>> For now, trying `%s`..." % fallBackLanguage                       ## again tries my default language
        language = fallBackLanguage
    print(message)
    return(language)


###########################################################
# PROCESS ALL RECORDS: APPROACH 2 #########################
###########################################################

# Why this way? Our computers are now quite powerful; they
# often have multiple cores and we can take advantage of this;
# if we process our data in the manner coded below --- we shuffle
# our publications and process them in random order --- we can
# run multiple instances fo the same script and data will
# be produced in parallel. You can run as many instances as
# your machine allows (you need to check how many cores
# your machine has). Even running two scripts will cut
# processing time roughly in half.

def processAllRecords(bibData):                                   ## now function to process all the pdfs
    keys = list(bibData.keys())                                   ## in a list and random to do more than one process at a time 
    random.shuffle(keys)

    for key in keys:                                              ## looping through keys; applying the function from above to all of the pdfs;
        bibRecord = bibData[key]

        functions.processBibRecord(memexPath, bibRecord)

        language = identifyLanguage(bibRecord, "eng")              ## checking language every time 
        ocrPublication(memexPath, bibRecord["rCite"], language)


bibData = functions.loadBib(settings["bib_all"])
processAllRecords(bibData)