import cv2
import mediapipe as mp
import pyautogui
import math  # Needed for distance calculation

# --- Setup ---
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Set a smaller, faster frame width
cap.set(4, 480)  # Set a smaller, faster frame height
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False  # Disables the corner failsafe

# --- Smoothing Variables ---
smoothing_factor = 7  # Adjust this: higher = smoother, more lag
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0

while True:
    # 1. Read Frame
    success, frame = cap.read()
    if not success:
        break

    # 2. Flip and Process Frame
    frame = cv2.flip(frame, 1)  # Flip horizontally (mirror view)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            # Draw landmarks for debugging
            drawing_utils.draw_landmarks(frame, hand)

            # Get the list of all landmarks
            landmarks = hand.landmark

            # --- Get Coordinates for Index and Thumb ---
            # We don't need to loop, just get them by ID
            index_tip = landmarks[8]  # Index finger tip
            thumb_tip = landmarks[4]  # Thumb tip

            # --- Convert to Pixel Coordinates ---
            # Get pixel coordinates for the index finger
            index_x_px = int(index_tip.x * frame_width)
            index_y_px = int(index_tip.y * frame_height)
            cv2.circle(frame, (index_x_px, index_y_px), 10, (0, 255, 255), -1)  # Yellow circle

            # Get pixel coordinates for the thumb
            thumb_x_px = int(thumb_tip.x * frame_width)
            thumb_y_px = int(thumb_tip.y * frame_height)
            cv2.circle(frame, (thumb_x_px, thumb_y_px), 10, (0, 0, 255), -1)  # Red circle

            # --- 1. Move Mouse (controlled by Index Finger) ---

            # Convert index finger position to screen coordinates
            curr_x = (index_x_px / frame_width) * screen_width
            curr_y = (index_y_px / frame_height) * screen_height

            # Apply smoothing
            smooth_x = prev_x + (curr_x - prev_x) / smoothing_factor
            smooth_y = prev_y + (curr_y - prev_y) / smoothing_factor

            # Move the mouse
            pyautogui.moveTo(smooth_x, smooth_y)

            # Update previous coordinates for next frame's smoothing
            prev_x, prev_y = smooth_x, smooth_y

            # --- 2. Check for Click (Thumb and Index close) ---

            # Calculate the 2D distance between thumb and index in pixels
            distance = math.hypot(index_x_px - thumb_x_px, index_y_px - thumb_y_px)
            # print(f"Distance: {distance}") # Uncomment to debug distance

            # If distance is small, it's a "pinch" or "click"
            if distance < 35:  # You may need to adjust this threshold
                cv2.circle(frame, (index_x_px, index_y_px), 10, (0, 255, 0), -1)  # Green circle on click
                pyautogui.click()
                pyautogui.sleep(0.5)  # Short pause to prevent rapid-fire clicks

    # --- Display ---
    cv2.imshow('Virtual Mouse', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- Cleanup ---
cap.release()
cv2.destroyAllWindows()