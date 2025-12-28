import sys
import json
import os
import time
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

# Get song name from arguments
song_name = " ".join(sys.argv[1:])
if not song_name:
    sys.exit(1)

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEVICE_CACHE = os.path.join(BASE_DIR, ".spotify_device.cache")

# Initialize Spotify client
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="user-read-playback-state user-modify-playback-state",
        cache_path=os.path.join(BASE_DIR, ".spotify_token.cache")
    )
)

def is_spotify_running():
    """Check if Spotify process is running"""
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq Spotify.exe"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return "Spotify.exe" in result.stdout
    except:
        return False

def find_spotify_exe():
    """Find Spotify executable path"""
    possible_paths = [
        os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\Spotify.exe"),
        r"C:\Program Files\Spotify\Spotify.exe",
        r"C:\Program Files (x86)\Spotify\Spotify.exe",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def start_spotify_hidden():
    """Start Spotify minimized and hidden"""
    if is_spotify_running():
        return
    
    # Try direct exe launch first
    spotify_exe = find_spotify_exe()
    if spotify_exe:
        try:
            subprocess.Popen(
                [spotify_exe, "--minimized"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
            )
            return
        except:
            pass
    
    # Fallback: use protocol handler with hidden window
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0  # SW_HIDE
        
        subprocess.Popen(
            "spotify:",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            startupinfo=startupinfo
        )
    except:
        pass

def get_cached_device():
    """Get cached device ID"""
    try:
        if os.path.exists(DEVICE_CACHE):
            with open(DEVICE_CACHE, "r") as f:
                return json.load(f).get("device_id")
    except:
        pass
    return None

def cache_device(device_id):
    """Cache device ID for faster future runs"""
    try:
        with open(DEVICE_CACHE, "w") as f:
            json.dump({"device_id": device_id}, f)
    except:
        pass

def find_device():
    """Find active computer device"""
    try:
        devices = sp.devices()["devices"]
        for device in devices:
            if device.get("type") == "Computer" and device.get("is_active"):
                return device["id"]
        for device in devices:
            if device.get("type") == "Computer":
                return device["id"]
    except:
        pass
    return None

def get_device_with_retry(max_wait=10):
    """Get device with smart polling"""
    device_id = find_device()
    if device_id:
        return device_id
    
    start_spotify_hidden()
    
    # Poll every 0.5s for up to max_wait seconds
    for _ in range(int(max_wait * 2)):
        time.sleep(0.5)
        device_id = find_device()
        if device_id:
            return device_id
    
    return None

# Try cached device first (fastest path)
device_id = get_cached_device()
if device_id:
    try:
        # Quick test if cached device still works
        sp.current_playback()
        devices = sp.devices()["devices"]
        if not any(d["id"] == device_id for d in devices):
            device_id = None
    except:
        device_id = None

# Find device if cache failed
if not device_id:
    device_id = get_device_with_retry()
    if not device_id:
        print("No Spotify device found")
        sys.exit(1)
    cache_device(device_id)

# Search for track with better matching
results = sp.search(q=song_name, limit=10, type="track")
tracks = results.get("tracks", {}).get("items", [])

if not tracks:
    print(f"No track found for: {song_name}")
    sys.exit(1)

# Find best match - prioritize exact title matches
song_lower = song_name.lower()
best_match = None

# First: try exact match
for track in tracks:
    track_name = track["name"].lower()
    if track_name == song_lower:
        best_match = track
        break

# Second: try exact match with artist
if not best_match:
    for track in tracks:
        track_full = f"{track['name']} {track['artists'][0]['name']}".lower()
        if song_lower in track_full or track_full in song_lower:
            if abs(len(track['name']) - len(song_name)) < 5:
                best_match = track
                break

# Third: use first result if no better match
if not best_match:
    best_match = tracks[0]

track_uri = best_match["uri"]

# Display what's playing
artist_names = ", ".join([artist["name"] for artist in best_match["artists"]])
print(f"♫ Now Playing: {best_match['name']} - {artist_names}")

# Play the track
try:
    sp.start_playback(device_id=device_id, uris=[track_uri])
except Exception as e:
    # If playback fails, clear cache and retry once
    cache_device(None)
    device_id = find_device()
    if device_id:
        sp.start_playback(device_id=device_id, uris=[track_uri])
    else:
        print("Failed to play track")
        sys.exit(1)
