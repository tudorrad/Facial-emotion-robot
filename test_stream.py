import cv2

print("Attempting to connect to Camera Stream at tcp://127.0.0.1:8888...")

# We use FFmpeg backend to help read the network stream
cap = cv2.VideoCapture('tcp://127.0.0.1:8888', cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("ERROR: Could not connect to stream!")
else:
    print("SUCCESS: Stream connected!")
    ret, frame = cap.read()
    if ret:
        print(f"Received a frame! Size: {frame.shape}")
        cv2.imwrite("test_image.jpg", frame)
        print("Saved test_image.jpg")
    else:
        print("Connected, but received empty data.")

cap.release()