import cv2
import mediapipe as mp
import socket
import json

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands.Hands(
max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Start capturing video from the first webcam.
cap = cv2.VideoCapture(0)
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = socket.gethostname()

# Reserve a port for your service.
port = 9999

# Bind to the port
serversocket.bind((host, port))

# Queue up to 5 requests
serversocket.listen(5)

# Establish a connection
clientsocket,addr = serversocket.accept()

print("Got a connection from %s" % str(addr))

# Check if the webcam is opened successfully.
if not cap.isOpened():
    print("Error: Could not open webcam.")
else:
    try:
        while True:
            # Read a frame from the webcam.
            success, frame = cap.read()
            
            # If the frame is not successfully read (e.g., webcam not accessible), break the loop.
            if not success:
                print("Couldn't read frame")
                break

            # Convert the frame to RGB.
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with MediaPipe Hands.
            results = mp_hands.process(rgb_image)
            if results.multi_hand_landmarks:
                hand_landmarks_data = [{'landmark': [{'x': landmark.x, 'y': landmark.y, 'z': landmark.z} for landmark in hand_landmarks.landmark]} for hand_landmarks in results.multi_hand_landmarks]
                json_data = json.dumps(hand_landmarks_data)
                clientsocket.send(json_data.encode('utf-8'))
            # Draw the hand annotations on the frame.
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=5),
                        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2))

            # Show the frame.
            cv2.imshow('Camera Feed', frame)

            # Press 'q' to exit the loop.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Release the webcam and destroy all OpenCV windows.
        cap.release()
        cv2.destroyAllWindows()
