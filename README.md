# Small Projects

This repository contains small learning projects that I create to practice and explore new concepts.  
Each project is simple, focused, and helps me improve my coding skills step by step.

---

## Projects

### 1. Email OTP Authenticator

A simple email-based OTP (One-Time Password) verification system using Gmail SMTP.

**Features:**
- Generates a random 6-digit OTP
- Sends OTP via email using Gmail SMTP
- Verifies user input against the generated OTP

**Technologies:**
- Python
- `smtplib` for email sending
- `python-dotenv` for environment variables

**Setup & Run:**

1. **Install dependencies:**
   ```bash
   pip install python-dotenv
   ```

2. **Create `op.env` file** in the `Email OTP Authenticator` folder:
   ```env
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   ```
   > **Note:** Use a Gmail App Password, not your regular password. [Generate one here](https://myaccount.google.com/apppasswords)

3. **Run:**
   ```bash
   python "Email OTP Authenticator/email_otp_auth.py"
   ```

---

### 2. Terminal Video Player

An ASCII art video player that renders videos directly in the terminal using character-based graphics.

**Features:**
- Converts video frames to ASCII art in real-time
- Stretches video to full terminal size
- Inverted ASCII rendering (dark → bright)

**Technologies:**
- Python
- OpenCV (`cv2`) for video processing
- `asciimatics` for terminal rendering

**Setup & Run:**

1. **Install dependencies:**
   ```bash
   pip install opencv-python asciimatics
   ```

2. **Place your video file** named `black_n_white_animation.mp4` in the `Terminal video player` folder, or modify the filename in the code.

3. **Run:**
   ```bash
   python "Terminal video player/terminal_video_player.py"
   ```

> **Tip:** Works best with black & white or high-contrast videos. Maximize your terminal window for best viewing experience.

---

### 3. Terminal Spotify

A command-line Spotify controller that plays songs directly from your terminal without opening the Spotify window.

**Features:**
- Search and play songs via command line
- Starts Spotify minimized and hidden in the background
- Smart device detection and caching for fast playback
- Intelligent track matching (exact name, artist, partial matches)

**Technologies:**
- Python
- `spotipy` (Spotify Web API wrapper)
- `python-dotenv` for credentials management

**Setup & Run:**

1. **Create a Spotify App** to get API credentials:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new app
   - Copy your `Client ID` and `Client Secret`
   - Add `http://127.0.0.1:8888/callback` as a Redirect URI

2. **Install dependencies:**
   ```bash
   cd Terminal_spotify
   pip install -r requirements.txt
   ```

3. **Create `.env` file** (copy from `.env.example`):
   ```env
   SPOTIPY_CLIENT_ID=your_client_id_here
   SPOTIPY_CLIENT_SECRET=your_client_secret_here
   SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
   ```

4. **Run:**
   ```bash
   python Terminal_spotify/play.py "song name"
   ```
   
   **Examples:**
   ```bash
   python Terminal_spotify/play.py "Bohemian Rhapsody"
   python Terminal_spotify/play.py "Blinding Lights"
   ```

> **First Run:** You'll be asked to authorize the app in your browser. After that, authentication tokens are cached for future use.

---

## Notes

- All projects use environment variables to keep sensitive credentials secure
- `.env` files are gitignored and won't be pushed to GitHub
- Each project is self-contained in its own folder

---

## Getting Started

1. Clone this repository
2. Navigate to the project folder you want to try
3. Follow the setup instructions for that specific project
4. Run and enjoy!

---

## Requirements

- Python 3.7+
- Project-specific dependencies (see individual project sections)
