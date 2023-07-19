import cv2
import mediapipe as mp
import math

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

import math

def detect_peace_sign(hand_landmarks):
    # Get the tip of the middle finger, index finger, and wrist
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

    # Calculate the distances between the middle finger and index finger tips and the wrist
    distance_middle_to_wrist = math.sqrt((middle_finger_tip.x - wrist.x)**2 + (middle_finger_tip.y - wrist.y)**2)
    distance_index_to_wrist = math.sqrt((index_finger_tip.x - wrist.x)**2 + (index_finger_tip.y - wrist.y)**2)

    # Check if the middle finger and index finger are sufficiently extended
    finger_extension_threshold = 0.1  # Adjust this threshold based on testing
    if distance_middle_to_wrist > finger_extension_threshold and distance_index_to_wrist > finger_extension_threshold:
        # Calculate the angle between the fingers and the wrist using dot product
        dot_product = (middle_finger_tip.x - wrist.x) * (index_finger_tip.x - wrist.x) + (middle_finger_tip.y - wrist.y) * (index_finger_tip.y - wrist.y)
        mag_middle = math.sqrt((middle_finger_tip.x - wrist.x)**2 + (middle_finger_tip.y - wrist.y)**2)
        mag_index = math.sqrt((index_finger_tip.x - wrist.x)**2 + (index_finger_tip.y - wrist.y)**2)
        cos_angle = dot_product / (mag_middle * mag_index)

        # Calculate the angle in degrees
        angle = math.degrees(math.acos(cos_angle))

        # Define the angle range for the peace sign
        peace_sign_angle_range = (100, 160)  # Adjust this range based on testing

        # Check if the angle is within the peace sign angle range
        if peace_sign_angle_range[0] < angle < peace_sign_angle_range[1]:
            return True

    return False

    

cap = cv2.VideoCapture(0)

hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    frame_rgb.flags.writeable = False
    result = hands.process(frame_rgb)
    frame_rgb.flags.writeable = True

    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    if result.multi_hand_landmarks:
        for lms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, lms, mp_hands.HAND_CONNECTIONS,
                                   mp_draw.DrawingSpec(color=(255, 0, 255),thickness=5, circle_radius=5))
            mp_draw.draw_landmarks(frame, lms, mp_hands.HAND_CONNECTIONS, connection_drawing_spec=mp_draw.DrawingSpec((0, 255, 0), thickness=5, circle_radius=4))
      
            # Detect the gesture and display the text output
            if detect_peace_sign(lms):
                cv2.putText(frame, "Peace!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
           
    cv2.imshow("junction2021", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()