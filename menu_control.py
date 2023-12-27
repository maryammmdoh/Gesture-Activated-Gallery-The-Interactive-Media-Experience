import cv2
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk
import math
import random

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize Tkinter
root = tk.Tk()
root.title("Hand Gesture Menu")

# Create a label to display hand gesture direction
direction_label = tk.Label(root, text="Move hand", font=("Arial", 14))
direction_label.pack()

# Create a canvas to display the camera feed
canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()

# Create a square object on the canvas
#square = canvas.create_rectangle(300, 200, 340, 240, fill="blue")


# Function to update direction text based on hand gesture
def update_direction(direction):
    direction_label.config(text=direction)

# Function to calculate the distance between two points
#def calculate_distance(point1, point2):
#    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

# Object class to represent objects on the canvas
class GameObject:
    def __init__(self, x, y, size):
        self.size = size
        self.x = x
        self.y = y
        self.is_picked_up = False

    def update_position(self, x, y):
        if not self.is_picked_up:
            self.x = x
            self.y = y
            #canvas.coords(self.obj, x, y, x + self.size, y + self.size)




# Function to detect hand gestures and update direction
def detect_hand_gesture():
    global objects
    # Create objects at random positions on the canvas
    objects = []
    for _ in range(5):
        x = random.randint(50, 590)
        y = random.randint(50, 430)
        obj = GameObject(x, y, 40)
        objects.append(obj)
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame = cv2.flip(rgb_frame, 1)  # Avoid flipping the camera
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the landmark positions
                landmark_positions = []
                for landmark in hand_landmarks.landmark:
                    landmark_x = landmark.x * frame.shape[1]
                    landmark_y = landmark.y * frame.shape[0]
                    landmark_positions.append((landmark_x, landmark_y))

                # Detect left, right, or rotate hand movement
                if landmark_positions[8][0] < landmark_positions[5][0]:
                    update_direction("Move left")
                    #canvas.move(square, -5, 0)  # Move the square left
                elif landmark_positions[8][0] > landmark_positions[5][0]:
                    update_direction("Move right")
                    #canvas.move(square, 5, 0)  # Move the square right
                elif landmark_positions[4][1] < landmark_positions[3][1]:
                    update_direction("Rotate")
                else:
                    # Detect if hand is close to an object and pick it up
                    for obj in objects:
                        distance = math.sqrt((landmark_positions[8][0] - obj.x)**2 + (landmark_positions[8][1] - obj.y)**2)
                        if distance < 50:  # Change the distance threshold as needed
                            obj.is_picked_up = True

                    update_direction("No movement")

                # Update object positions based on hand movement
                for obj in objects:
                    if obj.is_picked_up:
                        obj.update_position(landmark_positions[8][0] - obj.size // 2, landmark_positions[8][1] - obj.size // 2)
                # Draw objects on the camera feed
                for obj in objects:
                    if not obj.is_picked_up:
                        cv2.rectangle(rgb_frame, (obj.x, obj.y), (obj.x + obj.size, obj.y + obj.size), (255, 0, 0), 2)


        # Convert the RGB frame to BGR for displaying in OpenCV window
        bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
        cv2.imshow('Hand Gesture Object Interaction', bgr_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()

# Start detecting hand gestures and update direction text
detect_hand_gesture()

root.mainloop()