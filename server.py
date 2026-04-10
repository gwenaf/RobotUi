from microdot import Microdot, Response, send_file
import urandom

from components.display import show_message

app = Microdot()

@app.route('/')
async def index(request):
    return send_file("templates/login.html")

@app.route('/forgot')
async def forgot(request):
    global current_otp
    current_otp = str(urandom.getrandbits(6))
    show_message("OTP Generated", current_otp)

    return send_file('templates/forgot.html')

def start():
    print("Starting Web Server...")
    app.run(port=80)