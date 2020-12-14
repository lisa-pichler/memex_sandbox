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