from microdot import Microdot, Response, send_file
import urandom
import hashlib
import ubinascii
import json

from config import OTP_LENGTH, CONFIG_FILE

app = Microdot()

_display = None
_wifi = None
_motors = None
_ultrasound = None
_photo = None
_rgb = None
_serial = None
_accel = None
_session_token = None
_current_otp = None


def _hash(password):
    return ubinascii.hexlify(hashlib.sha256(password.encode()).digest()).decode()


def _generate_token():
    return ubinascii.hexlify(bytes([urandom.getrandbits(8) for _ in range(16)])).decode()


def _load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"networks": [], "admin_pass": ""}


def _save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)


def _is_authenticated(request):
    return _session_token is not None and request.cookies.get('session') == _session_token


def _redirect(url):
    return Response('', status_code=302, headers={'Location': url})


# ---------------------------------------------------------------------------
# Auth routes
# ---------------------------------------------------------------------------

@app.route('/')
async def index(request):
    return send_file('templates/login.html')


@app.route('/login', methods=['POST'])
async def login(request):
    global _session_token
    config = _load_config()

    if not config.get('admin_pass'):
        return _redirect('/forgot')

    form = request.form or {}
    if _hash(form.get('pwd', '')) == config['admin_pass']:
        _session_token = _generate_token()
        response = _redirect('/control')
        response.set_cookie('session', _session_token)
        return response

    return _redirect('/')


@app.route('/forgot')
async def forgot(request):
    global _current_otp
    _current_otp = ''.join([str(urandom.getrandbits(8) % 10) for _ in range(OTP_LENGTH)])
    _display.show_message("OTP:", _current_otp)
    return send_file('templates/forgot.html')


@app.route('/reset', methods=['POST'])
async def reset(request):
    global _current_otp
    form = request.form or {}
    otp = form.get('otp', '')
    new_pwd = form.get('new_pwd', '')

    if _current_otp is None or otp != _current_otp:
        return _redirect('/forgot')

    config = _load_config()
    config['admin_pass'] = _hash(new_pwd)
    _save_config(config)
    _current_otp = None

    return _redirect('/')


# ---------------------------------------------------------------------------
# WiFi management routes (authentication required)
# ---------------------------------------------------------------------------

@app.route('/wifi')
async def wifi_page(request):
    if not _is_authenticated(request):
        return _redirect('/')
    return send_file('templates/wifi.html')


@app.route('/wifi/list')
async def wifi_list(request):
    if not _is_authenticated(request):
        return Response('Unauthorized', status_code=401)
    config = _load_config()
    ssids = [{'ssid': n['ssid']} for n in config.get('networks', [])]
    return Response(json.dumps(ssids), headers={'Content-Type': 'application/json'})


@app.route('/wifi/scan')
async def wifi_scan(request):
    if not _is_authenticated(request):
        return Response('Unauthorized', status_code=401)
    try:
        networks = _wifi.scan_detailed()
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status_code=500,
                        headers={'Content-Type': 'application/json'})
    return Response(json.dumps(networks),
                    headers={'Content-Type': 'application/json'})


@app.route('/wifi/add', methods=['POST'])
async def wifi_add(request):
    if not _is_authenticated(request):
        return _redirect('/')

    form = request.form or {}
    ssid = form.get('ssid', '').strip()
    password = form.get('password', '')

    if not ssid:
        return _redirect('/wifi')

    config = _load_config()
    config['networks'] = [n for n in config['networks'] if n['ssid'] != ssid]
    config['networks'].append({'ssid': ssid, 'password': password})
    _save_config(config)

    return _redirect('/wifi')


@app.route('/wifi/update', methods=['POST'])
async def wifi_update(request):
    if not _is_authenticated(request):
        return _redirect('/')

    form = request.form or {}
    ssid = form.get('ssid', '')
    password = form.get('password', '')

    config = _load_config()
    for net in config['networks']:
        if net['ssid'] == ssid:
            net['password'] = password
            break
    _save_config(config)

    return _redirect('/wifi')


@app.route('/wifi/delete', methods=['POST'])
async def wifi_delete(request):
    if not _is_authenticated(request):
        return _redirect('/')

    form = request.form or {}
    ssid = form.get('ssid', '')
    config = _load_config()
    config['networks'] = [n for n in config['networks'] if n['ssid'] != ssid]
    _save_config(config)

    return _redirect('/wifi')


@app.route('/wifi/connect', methods=['POST'])
async def wifi_connect(request):
    if not _is_authenticated(request):
        return _redirect('/')

    form = request.form or {}
    ssid = form.get('ssid', '')
    config = _load_config()

    target = next((n for n in config['networks'] if n['ssid'] == ssid), None)
    if not target:
        return _redirect('/wifi')

    _display.show_message("Connecting...", ssid)
    ip = _wifi.connect(target['ssid'], target['password'])

    if ip:
        _display.show_message("WiFi Mode", ip)
        html = (
            '<!DOCTYPE html><html><head>'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Connected</title></head><body>'
            f'<h2>Connected to {ssid}</h2>'
            f'<p>New IP: <strong>{ip}</strong></p>'
            f'<p><a href="http://{ip}">Go to http://{ip}</a></p>'
            '</body></html>'
        )
        return Response(html, headers={'Content-Type': 'text/html'})

    _display.show_message("Conn. Failed", ssid)
    return _redirect('/wifi')


# ---------------------------------------------------------------------------
# Robot control routes (authentication required)
# ---------------------------------------------------------------------------

@app.route('/control')
async def control_page(request):
    if not _is_authenticated(request):
        return _redirect('/')
    return send_file('templates/control.html')


@app.route('/control/move', methods=['POST'])
async def control_move(request):
    if not _is_authenticated(request):
        return Response('Unauthorized', status_code=401)
    if _motors is None:
        return Response(json.dumps({'error': 'motors unavailable'}),
                        headers={'Content-Type': 'application/json'})

    data = request.json or {}
    action = data.get('action', 'stop')
    speed = data.get('speed', 50)

    if action == 'forward':
        _motors.forward(speed)
    elif action == 'backward':
        _motors.backward(speed)
    elif action == 'left':
        _motors.turn_left(speed)
    elif action == 'right':
        _motors.turn_right(speed)
    else:
        _motors.stop()

    return Response(json.dumps({'ok': True}),
                    headers={'Content-Type': 'application/json'})


@app.route('/control/sensors')
async def control_sensors(request):
    if not _is_authenticated(request):
        return Response('Unauthorized', status_code=401)

    data = {}

    if _ultrasound:
        dist = _ultrasound.distance_cm()
        data['distance'] = round(dist, 1) if dist >= 0 else -1

    if _photo:
        data['light'] = round(_photo.read_percent(), 1)

    if _accel:
        try:
            raw = _accel.read_all()
            data['ax'] = round(raw.get('ax', 0), 2)
            data['ay'] = round(raw.get('ay', 0), 2)
            data['az'] = round(raw.get('az', 0), 2)
            data['gz'] = round(raw.get('gz', 0), 2)
        except Exception:
            pass

    return Response(json.dumps(data),
                    headers={'Content-Type': 'application/json'})


@app.route('/control/rgb', methods=['POST'])
async def control_rgb(request):
    if not _is_authenticated(request):
        return Response('Unauthorized', status_code=401)
    if _rgb is None:
        return Response(json.dumps({'error': 'rgb unavailable'}),
                        headers={'Content-Type': 'application/json'})

    data = request.json or {}
    _rgb.set_color(data.get('r', 0), data.get('g', 0), data.get('b', 0))
    return Response(json.dumps({'ok': True}),
                    headers={'Content-Type': 'application/json'})


@app.route('/control/serial', methods=['POST'])
async def control_serial(request):
    if not _is_authenticated(request):
        return Response('Unauthorized', status_code=401)
    if _serial is None:
        return Response(json.dumps({'error': 'serial leds unavailable'}),
                        headers={'Content-Type': 'application/json'})

    data = request.json or {}
    _serial.set_all(data.get('r', 0), data.get('g', 0), data.get('b', 0))
    return Response(json.dumps({'ok': True}),
                    headers={'Content-Type': 'application/json'})


def start(display, wifi, components=None):
    global _display, _wifi, _motors, _ultrasound, _photo, _rgb, _serial, _accel
    _display = display
    _wifi = wifi
    if components:
        _motors = components.get('motors')
        _ultrasound = components.get('ultrasound')
        _photo = components.get('photo')
        _rgb = components.get('rgb')
        _serial = components.get('serial')
        _accel = components.get('accel')
    print("Starting Web Server...")
    app.run(port=80)
