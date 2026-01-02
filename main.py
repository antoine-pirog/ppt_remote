import pynput
import flask
import socket
import qrcode
import io

import randomizer


"""
PPT KB SHORTCUTS :

F5          : Begin the slideshow from first slide
shift+F5    : Begin the slideshow from the current slide
spacebar    : Advance to next slide/animation
N           : Advance to next slide/animation              <<< Supported by app
right arrow : Advance to next slide/animation
backspace   : Go to the previous slide/animation
P           : Go to the previous slide/animation           <<< Supported by app
left arrow  : Go to the previous slide/animation
Ctrl+P      : change the mouse pointer to a pen
W           : Pause and display a white screen             <<< Supported by app
,           : Pause and display a white screen
B           : Pause and display a black screen             <<< Supported by app
.           : Pause and display a black screen
E           : Change the pointer to an eraser
Ctrl+E      : Change the pointer to an eraser
Ctrl+A      : Change the pointer to the default arrow
Esc         : Exit
"""

host = "0.0.0.0"

""" pynput bindings """
keyboard = pynput.keyboard.Controller()
k = pynput.keyboard.Key

BTN_NEXT_SLIDE   = k.right
BTN_PREV_SLIDE   = k.left
BTN_BLACK_SCREEN = 'b'
BTN_WHITE_SCREEN = 'w'

def press(btn):
    keyboard.press(btn)
    keyboard.release(btn)

""" CREATE FLASK APP """

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route(f'/{randomizer.ID_INDEX}')
def pptremote():
    return flask.render_template(randomizer.URL_INDEX)

@app.route(f'/btn_callback/{randomizer.JSCALLBACKS["NEXT"]}')
def btn_callback_next():
    press(BTN_NEXT_SLIDE)
    return "nothing"

@app.route(f'/btn_callback/{randomizer.JSCALLBACKS["PREV"]}')
def btn_callback_prev():
    press(BTN_PREV_SLIDE)
    return "nothing"

@app.route(f'/btn_callback/{randomizer.JSCALLBACKS["BLACK"]}')
def btn_callback_black():
    press(BTN_BLACK_SCREEN)
    return "nothing"

@app.route(f'/btn_callback/{randomizer.JSCALLBACKS["WHITE"]}')
def btn_callback_white():
    press(BTN_WHITE_SCREEN)
    return "nothing"



""" Generate UI """
randomizer.cleanup()
path_index = randomizer.generate_index_html()

""" Provide connection info to the user """
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
local_ip = s.getsockname()[0]
app_addr = f"http://{local_ip}:{randomizer.PORT}/{randomizer.ID_INDEX}"
print(f"Accessible via {app_addr}")

''' Generate & print qrcode '''
qr = qrcode.QRCode()
qr.add_data(app_addr)
f = io.StringIO()
qr.print_ascii(out=f)
f.seek(0)
print(f.read())

""" Run app """
app.run(host=host, port=randomizer.PORT, debug=False)

randomizer.cleanup(which=path_index)
