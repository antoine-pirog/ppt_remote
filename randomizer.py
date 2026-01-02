import os
import glob
import random
import string

L_RANDOM = 16 # Length of randomized IDs

PLACEHOLDER_ID        = "ID_PLACEHOLDER"
PLACEHOLDER_STYLE     = "<!-- STYLE_PLACEHOLDER -->"
PLACEHOLDER_CALLBACKS = "<!-- CALLBACKS_PLACEHOLDER -->"
PLACEHOLDER_BUTTONS   = "<!-- BUTTONS_PLACEHOLDER -->"

def gen_id(length):
    characters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(characters) for i in range(length))
    return result_str

""" Randomize elements """
PORT = random.randint(49152,65535)
ID_INDEX             = gen_id(L_RANDOM)
ID_BTN_PREV          = gen_id(L_RANDOM)
ID_BTN_NEXT          = gen_id(L_RANDOM)
ID_BTN_WHITE         = gen_id(L_RANDOM)
ID_BTN_BLACK         = gen_id(L_RANDOM)
ID_BTN_START_FIRST   = gen_id(L_RANDOM)
ID_BTN_START_CURRENT = gen_id(L_RANDOM)
ID_BTN_STOP_SHOW     = gen_id(L_RANDOM)
ID_BTN_PEN           = gen_id(L_RANDOM)
ID_BTN_ERASER        = gen_id(L_RANDOM)
ID_BTN_ARROW         = gen_id(L_RANDOM)

""" CREATE HTML FILE FROM TEMPLATES """
URL_INDEX = ID_INDEX + ".html"

path_skeleton_html  = "./skeleton/index.html"
path_skeleton_style = "./skeleton/style.css"
path_index = "./templates/" + URL_INDEX
path_templates = "./templates"

JSCALLBACKS = {
        "PREV"          : ID_BTN_PREV,
        "NEXT"          : ID_BTN_NEXT,
        "WHITE"         : ID_BTN_WHITE,
        "BLACK"         : ID_BTN_BLACK,
        "START_FIRST"   : ID_BTN_START_FIRST,
        "START_CURRENT" : ID_BTN_START_CURRENT,
        "STOP_SHOW"     : ID_BTN_STOP_SHOW,
        "PEN"           : ID_BTN_PEN,
        "ERASER"        : ID_BTN_ERASER,
        "ARROW"         : ID_BTN_ARROW
    }

HTML_BUTTON_ROWS = [
            {
                "PREV"          : f"  <a href=# id={PLACEHOLDER_ID} class='button bglo bigtext tall' style='width: 40%'>&#x25C0;</a>", # Left arrow
                "NEXT"          : f"  <a href=# id={PLACEHOLDER_ID} class='button bgdo bigtext tall' style='width: 40%'>&#x25B6;</a>", # Right arrow
            },
            {
                "BLACK"         : f"  <a href=# id={PLACEHOLDER_ID} class='button bgk normaltext short' style='width: 40%'>Black screen</a>",
                "WHITE"         : f"  <a href=# id={PLACEHOLDER_ID} class='button bgw normaltext short' style='width: 40%'>White screen</a>"
            },
            {
                "PEN"           : f"  <a href=# id={PLACEHOLDER_ID} class='button bgb normaltext short' style='width: 25%'>Pen</a>",
                "ERASER"        : f"  <a href=# id={PLACEHOLDER_ID} class='button bgw normaltext short' style='width: 25%'>Eraser</a>",
                "ARROW"         : f"  <a href=# id={PLACEHOLDER_ID} class='button bgk normaltext short' style='width: 25%'>Arrow</a>"
            },
            {
                "START_FIRST"   : f"  <a href=# id={PLACEHOLDER_ID} class='button bglg normaltext shorter' style='width: 15%'>Start from first slide</a>",
                "START_CURRENT" : f"  <a href=# id={PLACEHOLDER_ID} class='button bgdg normaltext shorter' style='width: 15%'>Start from current slide</a>",
                "STOP_SHOW"     : f"  <a href=# id={PLACEHOLDER_ID} class='button bgr  normaltext shorter'  style='width: 40%'>Stop slideshow</a>"
            }
        ]

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
    for row in HTML_BUTTON_ROWS:
        text += "<div class='row'>\n"
        for k in row:
            if k in JSCALLBACKS:
                text += row[k].replace(PLACEHOLDER_ID, JSCALLBACKS[k]) + "\n"
            else:
                text += row[k] + "\n"
        text += "</div>\n"
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
                if PLACEHOLDER_STYLE in l:
                    fout.write(gen_style())
                elif PLACEHOLDER_CALLBACKS in l:
                    fout.write(gen_jscallbacks())
                elif PLACEHOLDER_BUTTONS in l:
                    fout.write(gen_htmlbuttons())
                else:
                    fout.write(l)
    return path_index

