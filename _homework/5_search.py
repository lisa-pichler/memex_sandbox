# homework for lesson 5
## search function; first tries studygroup

import functions
import json 
import re 
import yaml
### variables
settingsFile = "config_MA_new.yml"
settings = yaml.safe_load(open(settingsFile))

memexPath = settings["path_to_memex"]

#take a string as argument
def search():
    

    ## load OCR results
    ocrFiles = functions.dicOfRelevantFiles(memexPath, ".json")   
    citeKeys = list(ocrFiles.keys())

    #word = input("Please enter a word:" )

    dicOfMatches = {}       # dictionary with citeKeys as value, matches as value
    
    ## loop through OCR results

    for citeKeys, word in ocrFiles.items():   
        val = json.load(open(ocrFiles[citeKeys],"r",encoding= "utf8")) 
        #print(val) val = dictionary with key: pagenumber and value: pagecontent
        
        for pagenumbers, pagecontent in val: 
            dicOfMatches = {}
            for k in v:
                if "christianity" in v:
                    print("yes")
                else: 
                     print("notinthepage")
        
    print (dicOfMatches)




   # def searchDic (dic, word):
 #   searchDic = {}    
  #  for k,v in dic.items():      # for citekeys
   #     searchDic[v]={}
    #    for key, val in v:
     #       if word in val: 
      #          searchDic[k][key] = val
    #return(searchDic)
    #searchedDic = {}
   # searchedDic = functions.searchDic(ocrFiles, word)
  #  with open("searchresults.txt", 'w', encoding='utf8') as f9:              ## save it into a textfile; avoid extension .json;
   #     json.dump(searchedDic, f9, sort_keys=True, indent=4, ensure_ascii=False)
search()


    



