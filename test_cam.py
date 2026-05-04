import cv2

print("Scanning camera indices...")

# Try indices 0 through 4
for index in range(5):
    print(f"\n--- Testing Camera Index {index} ---")
    cap = cv2.VideoCapture(index, cv2.CAP_V4L2)

    if not cap.isOpened():
        print(f"Result: Failed to open.")
    else:
        # Try to read a frame
        ret, frame = cap.read()
        if ret:
            print(f"Result: SUCCESS! Found a working camera.")
            print(f"Resolution: {frame.shape[1]}x{frame.shape[0]}")
            cap.release()
            break
        else:
            print(f"Result: Opened, but returned empty frame (No Data).")
        cap.release()