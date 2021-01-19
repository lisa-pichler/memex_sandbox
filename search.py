# homework lesson 11
# search function; Alexander Huber version
import functions
import yaml, json, re, os



settingsFile = "config_MA_new.yml"
settings = yaml.safe_load(open(settingsFile))

memexPath = settings["path_to_memex"]

def search(searchArgument):
    targetFiles = functions.dicOfRelevantFiles(memexPath, ".json")
    citeKeys = list(targetFiles.keys())

    #searchArgument = input("What are you looking for: ")

    results = {}    
    for citeKey in citeKeys:    #loop trough all the keys
        docData = json.load(open(targetFiles[citeKey], "r", encoding="utf8"))   #load the respective json file with the ocr results
        for k, v in docData.items():    #keys = page numbers values = text
            if searchArgument in v:      #if the search Argument is in the page
                matchCounter = len(re.findall(searchArgument, v))    #count how often          
                if not citeKey in results.keys():   #creates an empty dict only if there isnt allready one                           
                    results[citeKey] = {}
                results[citeKey][k] = {}            #creates sub-dict with the page number as key
                results[citeKey][k]["matches"] = matchCounter   #at the key matches the number of matches 
                pagePath = os.path.join(functions.generatePublPath(memexPath, citeKey), "pages\\", k + ".html")  #creates the path to the html file for the page
                results[citeKey][k]["pathToPage"] = pagePath
                results[citeKey][k]["result"] = v   #adds the ocred text to the dict
    with open("search.txt", 'w', encoding='utf8') as f9:    #saves it into a file too
        json.dump(results, f9, sort_keys=True, indent=4, ensure_ascii=False)
    
    return(results)      



def createResultsPage(results, searchArgument):
    # load page template
    with open(settings["template_search"], "r", encoding="utf8") as ft:
        template = ft.read()

    pageTemp = template
    pageTemp = pageTemp.replace("@SEARCHARGUMENT@", searchArgument)

    content = ""
        
    for k, v in results.items():            
        content = content + "\n" + '<button class="collapsible">@CITEKEY@</button> <div class="content"> <ul>'.replace("@CITEKEY@", k + " (%d Pages with results)" %len(results[k].keys()))            
        for key, val in v.items():
            element = '<li><b><hr>(pdfPage: @PDFPAGE@)</b><hr> <span class='"searchResult"'>@SEARCHARGUMENT@</span><br> <hr> <a href="@PAGELINK@"><i>go to the original page...</i></a> </li>'.replace("@SEARCHARGUMENT@", searchArgument)
            element = element.replace("@PDFPAGE@", key)
            element = element.replace("@PAGELINK@", val["pathToPage"])

            content = content + element
        content = content + "</ul></div>"
                            

    pageTemp = pageTemp.replace("@buttons@", content)

    with open("search.html", "w", encoding="utf8") as f9:
        f9.write(pageTemp)

results = search("viking")
createResultsPage(results, "viking")