## program to get file for languages 
import functions 
import yaml

settingsFile = "config_MA_new.yml"
settings = yaml.safe_load(open(settingsFile))

memexPath = settings["memex_path"]


bibData = functions.loadBib(settings["bib_all"])

def getLang(bibData):
    tempDic = {}
    for k,v in bibData.items():
        if v["language"] in tempDic:
            tempDic[v["language"]] +=1
        else:
            tempDic[v["language"]] = 1
    results = []
    for k,v in tempDic.items():
        result = "%010d\t%s" % (v, k)
        results.append(result)
    results = sorted(results, reverse=True)
    results = "\n".join(results)
    with open("lang_analysis.txt", "w", encoding="utf8") as f9:
        f9.write(results)
getLang(bibData)
