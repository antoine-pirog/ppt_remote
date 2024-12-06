import os
import glob
import random
import string

L_RANDOM = 16 # Length of randomized IDs

def gen_id(length):
    characters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(characters) for i in range(length))
    return result_str

""" Randomize elements """
PORT = random.randint(49152,65535)
ID_INDEX     = gen_id(L_RANDOM)
ID_BTN_PREV  = gen_id(L_RANDOM)
ID_BTN_NEXT  = gen_id(L_RANDOM)
ID_BTN_WHITE = gen_id(L_RANDOM)
ID_BTN_BLACK = gen_id(L_RANDOM)

""" CREATE HTML FILE FROM TEMPLATES """
URL_INDEX = ID_INDEX + ".html"

path_skeleton_html  = "./skeleton/index.phtml"
path_skeleton_style = "./skeleton/style.pcss"
path_index = "./templates/" + URL_INDEX
path_templates = "./templates"

JSCALLBACKS = {
        "PREV"  : ID_BTN_PREV,
        "NEXT"  : ID_BTN_NEXT,
        "WHITE" : ID_BTN_WHITE,
        "BLACK" : ID_BTN_BLACK
    }

HTMLBUTTONS = {
        "PREV"  : f"<a href=# id=%ID% class='button bg1 tall' style='width: 40%'>PREV</a>",
        "NEXT"  : f"<a href=# id=%ID% class='button bg2 tall' style='width: 40%'>NEXT</a>",
        "BR0"   : f"<br>",
        "BLACK" : f"<a href=# id=%ID% class='button bg5 short' style='width: 40%'>BLACK SCREEN</a>",
        "WHITE" : f"<a href=# id=%ID% class='button bg5rev short' style='width: 40%'>WHITE SCREEN</a>"
        }

def gen_style():
    text = ""
    with open(path_skeleton_style, "r") as fid:
        text += fid.read()
    text += "\n"
    return text

def gen_jscallbacks():
    text = ""
    for k in JSCALLBACKS:
        text += "$(function() {" + "\n"
        text += "    $('a#" + JSCALLBACKS[k]+ "').on('click', function(e) { e.preventDefault()" + "\n"
        text += "    $.getJSON('/btn_callback/" + JSCALLBACKS[k] + "', " + "function(data) {}); return false;" + "\n"
        text += "    });" + "\n"
        text += "});" + "\n"
    return text

def gen_htmlbuttons():
    text = ""
    for k in HTMLBUTTONS:
        if k in JSCALLBACKS:
            text += HTMLBUTTONS[k].replace("%ID%", JSCALLBACKS[k]) + "\n"
        else:
            text += HTMLBUTTONS[k]
    return text

def cleanup(which=None):
    if which:
        # Cleanup one file only
        os.remove(which)
    else:
        # Cleanup all html files in template directory
        for f in glob.glob(f"{path_templates}/*.html"):
            os.remove(f)

def generate_index_html():
    with open(path_index, "w") as fout:
        with open(path_skeleton_html, "r") as fhtml:
            for l in fhtml.readlines():
                if "%STYLE%" in l:
                    fout.write(gen_style())
                elif "%CALLBACKS%" in l:
                    fout.write(gen_jscallbacks())
                elif "%BUTTONS%" in l:
                    fout.write(gen_htmlbuttons())
                else:
                    fout.write(l)
    return path_index

