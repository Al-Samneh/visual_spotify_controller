# 🎵 Spotify Camera Controller

I built this app to control Spotify with hand gestures using my webcam. Pretty cool for when you're coding and don't want to reach for the mouse!

## ✨ Features

- **Gesture-based controls**: Control Spotify without touching your keyboard or mouse
- **Real-time hand tracking**: Uses MediaPipe for accurate hand detection
- **Multiple gestures supported**:
  - 👆 **Index finger**: Play/Pause
  - ✌️ **Peace sign**: Next track
  - 👆👆👆 **Three fingers**: Previous track
  - ✋ **Open palm**: Volume up
  - ✊ **Closed fist**: Volume down
- **Live feedback**: See current track info and gesture recognition in real-time
- **Smart cooldown**: Prevents accidental rapid-fire commands

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- A webcam
- Spotify Premium account (required for playback control)
- Active Spotify session (open Spotify app/web player)

### 2. Setup

1. **Clone and navigate to the project**:
   ```bash
   cd /Users/al-samneh/Desktop/spotify
   ```

2. **Run the setup script**:
   ```bash
   python setup.py
   ```
   
   This will:
   - Install all required dependencies
   - Guide you through Spotify API setup
   - Create your `.env` configuration file

3. **Alternative manual setup**:
   
   If you prefer to set up manually:
   
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Copy environment template
   cp env_example.txt .env
   
   # Edit .env with your Spotify credentials
   ```

### 3. Get Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account
3. Click "Create App"
4. Fill in the details:
   - **App name**: Spotify Camera Controller
   - **App description**: Control Spotify with hand gestures
   - **Redirect URI**: `https://127.0.0.1:8080/callback`
5. Copy your **Client ID** and **Client Secret**
6. Add them to your `.env` file

### 4. Run the App

```bash
python spotify_controller.py
```

## 🎮 How to Use

1. **Start the app**: Run `python spotify_controller.py`
2. **Position yourself**: Sit about 2-3 feet from your camera
3. **Make sure Spotify is playing**: Open Spotify and start playing music
4. **Use gestures**: Hold up your hand and make the gestures shown below
5. **Quit**: Press 'q' in the camera window or Ctrl+C in the terminal

## 🤚 Gesture Guide

| Gesture | Control | Description |
|---------|---------|-------------|
| 👆 Index finger up | Play/Pause | Point with your index finger |
| ✌️ Peace sign | Next track | Index and middle finger up |
| 👆👆👆 Three fingers | Previous track | Thumb, index, and middle finger up |
| ✋ Open palm | Volume up | All five fingers extended |
| ✊ Closed fist | Volume down | All fingers closed |

### 💡 Tips for Best Results

- **Good lighting**: Ensure your hand is well-lit
- **Clear background**: Avoid cluttered backgrounds behind your hand
- **Steady gestures**: Hold gestures for a moment to ensure detection
- **One hand**: Use only one hand at a time
- **Distance**: Keep your hand 1-2 feet from the camera

## 🛠️ Troubleshooting

### Common Issues

**"Cannot open camera"**
- Check if another app is using your camera
- Try a different camera index (change `0` to `1` in `cv2.VideoCapture(0)`)

**"Spotify authentication failed"**
- Verify your Client ID and Secret in `.env`
- Check that your Redirect URI is exactly `https://127.0.0.1:8080/callback`
- Make sure you have Spotify Premium

**Gestures not being detected**
- Check lighting conditions
- Ensure your hand is clearly visible
- Try adjusting the `min_detection_confidence` in the code

**"No active device found"**
- Open Spotify app or web player
- Start playing a song
- Make sure you're logged into the same account

### Debug Mode

To see more detailed output, you can modify the gesture detection confidence levels in `spotify_controller.py`:

```python
self.hands = self.mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,  # Lower for easier detection
    min_tracking_confidence=0.3    # Lower for easier tracking
)
```

## 🔧 Customization

### Adding New Gestures

To add custom gestures, modify the `detect_gesture` method in the `GestureDetector` class:

```python
def detect_gesture(self, landmarks) -> Optional[str]:
    # Add your custom gesture logic here
    # Return gesture name string
    pass
```

### Changing Cooldown

Adjust the gesture cooldown in the `GestureDetector` class:

```python
self.gesture_cooldown = 1.0  # Reduce for faster response
```

### Custom Controls

Add new Spotify controls in the `SpotifyController` class:

```python
def shuffle_toggle(self):
    """Toggle shuffle mode"""
    # Implementation here
```

## 📦 Dependencies

- `opencv-python`: Computer vision and camera handling
- `mediapipe`: Hand tracking and gesture recognition
- `spotipy`: Spotify Web API client
- `python-dotenv`: Environment variable management
- `numpy`: Numerical computations

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is open source and available under the MIT License.

## Built With

- MediaPipe for hand tracking
- Spotipy for Spotify API
- OpenCV for computer vision