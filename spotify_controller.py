# Spotify Camera Controller - Control Spotify with hand gestures

import os
import time
import threading
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Tuple, Dict, Any

# Load environment variables
load_dotenv()

class SpotifyController:
    
    def __init__(self):
        self.scope = "user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
        self.sp = None
        self.setup_spotify()
    
    def setup_spotify(self):
        try:
            auth_manager = SpotifyOAuth(
                client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI', 'https://127.0.0.1:8080/callback'),
                scope=self.scope,
                open_browser=True,  # Automatically open browser
                cache_path=".spotify_cache"  # Use cache file
            )
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            print("Spotify authentication successful!")
        except Exception as e:
            print(f"Spotify authentication failed: {e}")
            print("Please check your credentials in the .env file")
    
    def play_pause(self):
        """Toggle play/pause"""
        try:
            current = self.sp.current_playback()
            if current and current['is_playing']:
                self.sp.pause_playback()
                print("Paused")
            else:
                self.sp.start_playback()
                print("Playing")
        except Exception as e:
            print(f"Play/pause error: {e}")
    
    def next_track(self):
        """Skip to next track"""
        try:
            self.sp.next_track()
            print("Next track")
        except Exception as e:
            print(f"Next track error: {e}")
    
    def previous_track(self):
        """Go to previous track"""
        try:
            self.sp.previous_track()
            print("Previous track")
        except Exception as e:
            print(f"Previous track error: {e}")
    
    def volume_up(self):
        """Increase volume by 10%"""
        try:
            current = self.sp.current_playback()
            if current:
                new_volume = min(100, current['device']['volume_percent'] + 10)
                self.sp.volume(new_volume)
                print(f"Volume: {new_volume}%")
        except Exception as e:
            print(f"Volume up error: {e}")
    
    def volume_down(self):
        """Decrease volume by 10%"""
        try:
            current = self.sp.current_playback()
            if current:
                new_volume = max(0, current['device']['volume_percent'] - 10)
                self.sp.volume(new_volume)
                print(f"Volume: {new_volume}%")
        except Exception as e:
            print(f"Volume down error: {e}")
    
    def get_current_track(self) -> Optional[Dict[str, Any]]:
        """Get currently playing track info"""
        try:
            current = self.sp.current_playback()
            if current and current['item']:
                return {
                    'name': current['item']['name'],
                    'artist': current['item']['artists'][0]['name'],
                    'is_playing': current['is_playing']
                }
        except Exception as e:
            print(f"Get current track error: {e}")
        return None


class GestureDetector:
    """Handles hand gesture detection using MediaPipe"""
    
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Gesture cooldown to prevent rapid firing
        self.last_gesture_time = 0
        self.gesture_cooldown = 1.0  # seconds
    
    def detect_gesture(self, landmarks) -> Optional[str]:
        """Detect gesture based on hand landmarks"""
        if not landmarks:
            return None
        
        # Get landmark positions
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]
        index_tip = landmarks[8]
        index_pip = landmarks[6]
        index_mcp = landmarks[5]
        middle_tip = landmarks[12]
        middle_pip = landmarks[10]
        ring_tip = landmarks[16]
        ring_pip = landmarks[14]
        pinky_tip = landmarks[20]
        pinky_pip = landmarks[18]
        
        # Count extended fingers with improved logic
        fingers = []
        
        # Thumb - check if tip is further from wrist than IP joint
        wrist = landmarks[0]
        thumb_extended = (abs(thumb_tip.x - wrist.x) > abs(thumb_ip.x - wrist.x))
        fingers.append(thumb_extended)
        
        # Other fingers - check if tip is above PIP joint
        fingers.append(index_tip.y < index_pip.y)
        fingers.append(middle_tip.y < middle_pip.y)
        fingers.append(ring_tip.y < ring_pip.y)
        fingers.append(pinky_tip.y < pinky_pip.y)
        
        total_fingers = sum(fingers)
        

        
        # Improved gesture recognition with more specific conditions
        if total_fingers == 1 and fingers[1] and not any(fingers[i] for i in [0, 2, 3, 4]):
            return "play_pause"  # Only index finger
        elif total_fingers == 2 and fingers[1] and fingers[2] and not any(fingers[i] for i in [0, 3, 4]):
            return "next"  # Peace sign (index + middle)
        elif total_fingers >= 3 and fingers[0] and fingers[1] and fingers[2] and not fingers[4] and not fingers[3]:
            return "previous"  # Three or more fingers including thumb, index, middle
        elif total_fingers >= 4:  # Open palm (4 or 5 fingers)
            return "volume_up"
        elif total_fingers == 0:  # Closed fist
            return "volume_down"
        elif total_fingers == 2 and fingers[0] and fingers[2] and not fingers[1] and not fingers[3] and not fingers[4]: #middle finger basically
            return "play_song"
        return None
    
    def process_frame(self, frame):
        """Process a single frame and return gesture if detected"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        gesture = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # Detect gesture with cooldown
                current_time = time.time()
                if current_time - self.last_gesture_time > self.gesture_cooldown:
                    gesture = self.detect_gesture(hand_landmarks.landmark)
                    if gesture:
                        self.last_gesture_time = current_time
        
        return frame, gesture


class SpotifyCameraApp:
    """Main application class"""
    
    def __init__(self):
        self.spotify = SpotifyController()
        self.gesture_detector = GestureDetector()
        self.cap = None
        self.running = False
    
    def start_camera(self):
        """Initialize camera"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Cannot open camera")
            return False
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("Camera initialized")
        return True
    
    def execute_gesture(self, gesture: str):
        """Execute the corresponding Spotify action for a gesture"""
        if gesture == "play_pause":
            self.spotify.play_pause()
        elif gesture == "next":
            self.spotify.next_track()
        elif gesture == "previous":
            self.spotify.previous_track()
        elif gesture == "volume_up":
            self.spotify.volume_up()
        elif gesture == "volume_down":
            self.spotify.volume_down()
        elif gesture == "play_song": #Plays the GOAT Toby Keith
            self.spotify.sp.start_playback(uris=["spotify:track:4TJUS843fKiqqIzycM74Oy"])
    
    def draw_ui(self, frame):
        """Draw UI elements on the frame"""
        height, width = frame.shape[:2]
        
        # Background for instructions
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (width-10, 150), (0, 0, 0), -1)
        frame = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)
        
        # Instructions
        instructions = [
            "Spotify Camera Controller",
            "Index finger: Play/Pause",
            "Peace sign: Next track", 
            "Three fingers: Previous track",
            "Open palm: Volume up",
            "Closed fist: Volume down",
            "Thumb + Ring: Play specific song"
        ]
        
        for i, text in enumerate(instructions):
            y = 30 + (i * 20)
            cv2.putText(frame, text, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Current track info
        track_info = self.spotify.get_current_track()
        if track_info:
            status = "Playing" if track_info['is_playing'] else "Paused"
            track_text = f"{status} {track_info['name']} - {track_info['artist']}"
            cv2.putText(frame, track_text, (20, height-30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame
    
    def run(self):
        """Main application loop"""
        if not self.start_camera():
            return
        
        self.running = True
        print("Spotify Camera Controller started!")
        print("Press 'q' to quit")
        
        try:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Process gestures
                frame, gesture = self.gesture_detector.process_frame(frame)
                
                # Execute gesture command
                if gesture:
                    self.execute_gesture(gesture)
                
                # Draw UI
                frame = self.draw_ui(frame)
                
                # Display frame
                cv2.imshow('Spotify Camera Controller', frame)
                
                # Check for quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        except KeyboardInterrupt:
            print("\nShutting down...")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Cleanup complete")


if __name__ == "__main__":
    app = SpotifyCameraApp()
    app.run()