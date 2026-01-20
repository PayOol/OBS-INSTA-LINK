# -------------------------------------------------------------------
# OBS INSTA-LINK
# Transfer your OBS recordings to Mobile instantly via QR Code.
#
# Author: PayOol™
# License: Free & Open Source
#
# Support the project: https://payool.mychariow.shop/prd_t2vk4y
# -------------------------------------------------------------------

import obspython as obs
import http.server
import socketserver
import threading
import socket
import os
import urllib.request
import urllib.parse
import time

# --- GLOBAL VARIABLES & DEFAULTS ---
port = 8080
source_name_in_obs = "QR_Share"
qr_api_url = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data="
httpd = None

def log(msg):
    print(f"[INSTA-LINK] {msg}")

# --- FORCE DOWNLOAD HANDLER ---
class ForceDownloadHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Content-Disposition', 'attachment')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

# --- UTILITIES ---

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def set_source_visibility(visible):
    current_scene = obs.obs_frontend_get_current_scene()
    scene = obs.obs_scene_from_source(current_scene)
    scene_item = obs.obs_scene_find_source(scene, source_name_in_obs)

    if scene_item:
        obs.obs_sceneitem_set_visible(scene_item, visible)
        state = "VISIBLE" if visible else "HIDDEN"
        log(f"Source '{source_name_in_obs}' is now {state}.")
    else:
        if visible: 
            log(f"Warning: Source '{source_name_in_obs}' not found in current scene.")

    obs.obs_source_release(current_scene)

def start_server(directory):
    global httpd
    if httpd:
        try:
            httpd.shutdown()
            httpd.server_close()
        except:
            pass
    
    os.chdir(directory)
    
    handler = ForceDownloadHandler
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        httpd = socketserver.TCPServer(("", port), handler)
        log(f"Server started at http://{get_local_ip()}:{port}")
        thread = threading.Thread(target=httpd.serve_forever)
        thread.daemon = True
        thread.start()
    except Exception as e:
        log(f"SERVER ERROR: {e}")

def update_qr_image(url_to_encode):
    log(f"Generating new QR Code...")
    full_api_url = qr_api_url + urllib.parse.quote(url_to_encode)
    temp_qr_path = os.path.join(os.path.expanduser("~"), "obs_qr_temp.png")
    
    try:
        req = urllib.request.Request(
            full_api_url, 
            data=None, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response, open(temp_qr_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception as e:
        log(f"QR DOWNLOAD ERROR: {e}")
        return

    # Update Image Source
    current_scene = obs.obs_frontend_get_current_scene()
    scene = obs.obs_scene_from_source(current_scene)
    scene_item = obs.obs_scene_find_source(scene, source_name_in_obs)

    if scene_item:
        source = obs.obs_sceneitem_get_source(scene_item)
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "file", temp_qr_path)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
    
    obs.obs_source_release(current_scene)
    set_source_visibility(True)

# --- OBS CALLBACKS ---

def on_event(event):
    if event == obs.OBS_FRONTEND_EVENT_RECORDING_STARTED:
        log("Recording Started -> Hiding QR Code.")
        set_source_visibility(False)

    elif event == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        log("Recording Stopped -> Processing...")
        last_recording = obs.obs_frontend_get_last_recording()
        
        if not last_recording:
            time.sleep(1)
            last_recording = obs.obs_frontend_get_last_recording()

        if last_recording:
            directory = os.path.dirname(last_recording)
            filename = os.path.basename(last_recording)
            
            start_server(directory)
            
            local_ip = get_local_ip()
            download_url = f"http://{local_ip}:{port}/{urllib.parse.quote(filename)}"
            update_qr_image(download_url)

# --- SCRIPT PROPERTIES (UI) ---

def script_defaults(settings):
    obs.obs_data_set_default_int(settings, "port", 8080)
    obs.obs_data_set_default_string(settings, "source_name", "QR_Share")

def script_description():
    return """
    <center><h2>🚀 OBS INSTA-LINK</h2></center>
    <p>Automatically transfer your latest recording to your Smartphone using a local QR Code.</p>
    
    <p><b>How to use:</b><br>
    1. Create an <b>Image Source</b> named <code>QR_Share</code>.<br>
    2. Start Recording (The image will hide).<br>
    3. Stop Recording (The QR Code will appear).<br>
    4. Scan & Download!</p>
    
    <hr>
    <center><h3>☕ Support the Development</h3>
    <p>This tool is 100% Free & Open Source.<br>
    If it saves you time, consider buying me a coffee:</p>
    <p><a href="https://payool.mychariow.shop/prd_t2vk4y" style="font-size:16px; color:#ff0055; font-weight:bold;">
    >>> CLICK HERE TO DONATE <<<
    </a></p></center>
    """

def script_update(settings):
    global port
    global source_name_in_obs
    
    port = obs.obs_data_get_int(settings, "port")
    source_name_in_obs = obs.obs_data_get_string(settings, "source_name")
    log(f"Settings Updated: Port={port}, Source={source_name_in_obs}")

def script_properties():
    props = obs.obs_properties_create()
    
    obs.obs_properties_add_int(props, "port", "Server Port", 1024, 65535, 1)
    obs.obs_properties_add_text(props, "source_name", "Image Source Name", obs.OBS_TEXT_DEFAULT)
    
    return props

def script_load(settings):
    log("Insta-Link Loaded successfully.")
    obs.obs_frontend_add_event_callback(on_event)