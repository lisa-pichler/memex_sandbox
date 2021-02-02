import os, shutil, re
import yaml

###########################################################
# VARIABLES ###############################################
###########################################################

settingsFile = "config_MA_new.yml"                                                    ## loads my yaml file with the settings
settings = yaml.safe_load(open(settingsFile))

memexPath = settings["path_to_memex"]                                                    ## path to memex folder

###########################################################
# FUNCTIONS ###############################################
###########################################################

# load bibTex Data into a dictionary                                                  ## loading data in dictionary
def loadBib(bibTexFile):   

    bibDic = {}                                                                       ## creates an empty dictionary 
    recordsNeedFixing = []                                                            ## creates a list 

    with open(bibTexFile, "r", encoding="utf8") as f1:                        ## opens my bibtex file, r fo reading 
        records = f1.read().split("\n@")                                              ## splits at new line and @

        for record in records[1:]:                                                    ## loops through records, leaving out first 1
            # let process ONLY those records that have PDFs
            if ".pdf" in record.lower():                                              ## only looks at records with .pdf extension
                completeRecord = "\n@" + record                                       ## adding the new line and @ again to have a complete record

                record = record.strip().split("\n")[:-1]                             ## stripping record of spaces and splitting at new line; -1: means no }

                rType = record[0].split("{")[0].strip()                              ## splits the record at {
                rCite = record[0].split("{")[1].strip().replace(",", "")             ## gives us the citekey

                bibDic[rCite] = {}                                                   ## definitions for dictionary 
                bibDic[rCite]["rCite"] = rCite
                bibDic[rCite]["rType"] = rType
                bibDic[rCite]["complete"] = completeRecord

                for r in record[1:]:                                                ## looping again
                    key = r.split("=")[0].strip()                                   ## splitting records into key and value pairs at =
                    val = r.split("=")[1].strip()
                    val = re.sub("^\{|\},?", "", val) 

                    bibDic[rCite][key] = val

                    # fix the path to PDF
                    if key == "file":                                               ## make sure to get the pdf not any other paths
                        if ";" in val:                                              ## if there is more there would be a ;
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

# generate path from bibtex code, and create a folder, if does not exist;
# if the code is `SavantMuslims2017`, the path will be pathToMemex+`/s/sa/SavantMuslims2017/`
def generatePublPath(pathToMemex, bibTexCode):
    temp = bibTexCode.lower()
    directory = os.path.join(pathToMemex, temp[0], temp[:2], bibTexCode)
    return(directory)

# process a single bibliographical record: 1) create its unique path; 2) save a bib file; 3) save PDF file 
def processBibRecord(pathToMemex, bibRecDict):
    tempPath = generatePublPath(pathToMemex, bibRecDict["rCite"])

    print("="*80)
    print("%s :: %s" % (bibRecDict["rCite"], tempPath))
    print("="*80)

    if not os.path.exists(tempPath):                                                 # if the path does not alread exist it makes a new 
        os.makedirs(tempPath)                                                        # folder with the rules of tempPath - using citation key

        bibFilePath = os.path.join(tempPath, "%s.bib" % bibRecDict["rCite"])         # adds a bib file for the record with path plus .bib
        with open(bibFilePath, "w", encoding="utf8") as f9:
            f9.write(bibRecDict["complete"])

        pdfFileSRC = bibRecDict["file"]

        #betterbibtex escaped: , this line replaces "\:" with ":"
        pdfFileSRC = pdfFileSRC.replace("\\:", ":")

        pdfFileDST = os.path.join(tempPath, "%s.pdf" % bibRecDict["rCite"])          # adds pdf file into the folder with path plus .pdf
        if not os.path.isfile(pdfFileDST): # this is to avoid copying that had been already copied.
            shutil.copyfile(pdfFileSRC, pdfFileDST)


###########################################################
# PROCESS ALL RECORDS #####################################
###########################################################

def processAllRecords(bibData):
    for k,v in bibData.items():
        processBibRecord(memexPath, v)

bibData = loadBib(settings["bib_all"])
processAllRecords(bibData)

print("Done!")