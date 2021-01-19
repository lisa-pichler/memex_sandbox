# homework lesson 11
# part 5, searing for publications; wordclouds; loading stopwords


## generate wordcloud, provide function with path to save file 
## and dictionary of tf-idf terms

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import functions 
import yaml
import os
import json
settingsFile = "config_MA_new.yml"
settings = yaml.safe_load(open(settingsFile))

memexPath = settings["path_to_memex"]

ocrFiles = functions.dicOfRelevantFiles(memexPath, ".json")   
citeKeys = list(ocrFiles.keys())




#print(tfidfDic)
def createWordCloud(savePath, tfIdfDic):
    wc = WordCloud(width=1000, height=600, background_color="white", random_state=2,
                   relative_scaling=0.5, colormap="gray") 
    wc.generate_from_frequencies(tfIdfDic)
    # plotting
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    #plt.show() # this line will show the plot
    plt.savefig(savePath, dpi=200, bbox_inches='tight')

#createWordCloud(savePath, tfIdfDic)

def processAllClouds(filename): 
    

    docData = json.load(open(filename, "r", encoding = "utf8"))

    for k,v in docData.items():
        savePath = functions.generatePublPath(memexPath,k)
        savePath = savePath + "\\" + k
        if v:
            createwordCloud(savePath, k)

processAllClouds("tdidfTableDic_filtered.txt")

    