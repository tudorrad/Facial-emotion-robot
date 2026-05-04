# ---- coding: utf-8 ----
# ===================================================
# Author: Susanta Biswas
# ===================================================
"""Description: Class with methods to do emotion analysis
on video or webcam feed.

Usage: python video_main"""
# ===================================================
import sys
import time
from typing import Dict, List

import cv2
import numpy as np
import os
import motors

from emotion_analyzer.emotion_detector import EmotionDetector
from emotion_analyzer.logger import LoggerFactory
from emotion_analyzer.media_utils import (
    annotate_emotion_stats,
    annotate_warning,
    convert_to_rgb,
    draw_bounding_box_annotation,
    draw_emoji,
    get_video_writer,
)
from emotion_analyzer.validators import path_exists

# Load the custom logger
logger = None
try:
    logger_ob = LoggerFactory(logger_name=__name__)
    logger = logger_ob.get_logger()
    logger.info("{} loaded...".format(__name__))
    # set exception hook for uncaught exceptions
    sys.excepthook = logger_ob.uncaught_exception_hook
except Exception as exc:
    raise exc


class EmotionAnalysisVideo:
    """Class with methods to do emotion analysis on video or webcam feed."""

    emoji_foldername = "emojis"

    def __init__(
        self,
        face_detector: str = "dlib",
        model_loc: str = "models",
        face_detection_threshold: float = 0.8,
        emoji_loc: str = "data",
    ) -> None:

        try:
            motors.setup()
            print("GPIO Pins Initialized Successfully")
        except Exception as e:
            print(f"Warning: Could not initialize motors: {e}")

        # construct the path to emoji folder
        self.emoji_path = os.path.join(emoji_loc, EmotionAnalysisVideo.emoji_foldername)
        # Load the emojis
        self.emojis = self.load_emojis(emoji_path=self.emoji_path)

        self.emotion_detector = EmotionDetector(
            model_loc=model_loc,
            face_detection_threshold=face_detection_threshold,
            face_detector=face_detector,
        )

    def emotion_analysis_video(
        self,
        video_path: str = None,
        detection_interval: int = 15,
        save_output: bool = False,
        preview: bool = False,
        output_path: str = "data/output.mp4",
        resize_scale: float = 0.5,
    ) -> None:

        # if video_path is None:
        # If no video source is given, try
        # switching to webcam
        video_path = 0 if video_path is None else video_path

        #if not path_exists(video_path):
            #raise FileNotFoundError

        cap, video_writer = None, None

        try:
            # FORCE TCP STREAM CONNECTION
            cap = cv2.VideoCapture('tcp://127.0.0.1:8888', cv2.CAP_FFMPEG)
            # To save the video file, get the opencv video writer
            video_writer = get_video_writer(cap, output_path)
            frame_num = 1

            t1 = time.time()
            logger.info("Enter q to exit...")

            emotions = []

            last_emotion = "neutral"

            """while True:
                status, frame = cap.read()
                if not status:
                    print("ERROR: Camera read failed! Status is False.")

                if not status:
                    break

                try:
                    # Flip webcam feed so that it looks mirrored
                    if video_path == 0:
                        frame = cv2.flip(frame, 2)

                    if frame_num % detection_interval == 0:
                        # Scale down the image to increase model
                        # inference time.
                        smaller_frame = convert_to_rgb(
                            cv2.resize(frame, (0, 0), fx=resize_scale, fy=resize_scale)
                        )
                        # Detect emotion
                        emotions = self.emotion_detector.detect_emotion(smaller_frame)

                        if emotions and len(emotions) > 0:
                            current_emotion = emotions[0]['emotion']
                            print(f">>> AI DECISION: {current_emotion}") # Check Terminal B for this!
                            
                            if current_emotion == "happy":
                                motors.forward()
                            elif current_emotion in ["sad", "angry", "fear"]:
                                motors.backward()
                            else:
                                motors.stop()
                        else:
                            # No face detected in this check
                            motors.stop()

                    # Annotate the current frame with emotion detection data
                    frame = self.annotate_emotion_data(emotions, frame, resize_scale)

                    if save_output:
                        video_writer.write(frame)
                    if preview:
                        cv2.imshow("Preview", cv2.resize(frame, (680, 480)))

                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("q"):
                        break
                
                except Exception as exc:
                    raise exc
                frame_num += 1"""
            
            #NEW WHILE LOOP
            # Add this right before the while loop starts
            last_emotion = "none"
            print("--- AI LOOP STARTING ---")

            last_emotion = "none"
            last_direction = "clockwise"

            while True:
                status, frame = cap.read()
                if not status:
                    break

                try:
                    if video_path == 0:
                        frame = cv2.flip(frame, 2)

                    if frame_num % detection_interval == 0:
                        # REMAINS ESSENTIAL: Resize for speed
                        smaller_frame = convert_to_rgb(
                            cv2.resize(frame, (0, 0), fx=resize_scale, fy=resize_scale)
                        )
                        
                        # Detect emotions and store in local 'emotions' variable
                        emotions = self.emotion_detector.detect_emotion(smaller_frame)

                        if emotions and len(emotions) > 0:
                            detection_width = smaller_frame.shape[1]

                            bbox = emotions[0]['bbox']
                            face_center_x = (bbox[0] + bbox[2]) / 2

                            relative_pos = face_center_x / detection_width
                            
                            if relative_pos < 0.35:
                                last_direction = "left"
                            elif relative_pos > 0.65:
                                last_direction = "right"
                            else:
                                last_direction = "center"

                            print(f"DEBUG: Pos: {relative_pos:.2f} | Side: {last_direction}")
                            
                            current_emotion = emotions[0]['emotion'].lower()
                            if current_emotion != last_emotion:
                                print(f">>> TARGET FOUND: {current_emotion} at {last_direction}")
                                last_emotion = current_emotion
                                
                                if current_emotion == "happy":
                                    motors.forward(speed=80)
                                elif current_emotion in ["sad", "angry", "fear"]:
                                    motors.backward(speed=80)
                                else:
                                    motors.stop()
                        else:
                            if last_emotion != "searching":
                                print(f">>> TARGET LOST: Spinning {last_direction} to recover...")
                                last_emotion = "searching"

                            if last_direction == "left":
                                motors.spin_left(speed=60)
                            else:
                                motors.spin_right(speed=60)

                    # Draw the square using the 'emotions' variable
                    frame = self.annotate_emotion_data(emotions, frame, resize_scale)

                    if preview:
                        cv2.imshow("Preview", cv2.resize(frame, (680, 480)))

                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                
                except Exception as exc:
                    print(f"CRITICAL ERROR in loop: {exc}")
                    motors.stop()
                    raise exc
                frame_num += 1

            t2 = time.time()
            logger.info("Time:{}".format((t2 - t1) / 60))
            logger.info("Total frames: {}".format(frame_num))
            logger.info("Time per frame: {}".format((t2 - t1) / frame_num))

        except Exception as exc:
            raise exc
        finally:
            cv2.destroyAllWindows()
            cap.release()
            video_writer.release()


    def load_emojis(self, emoji_path: str = "data//emoji") -> List:
        emojis = {}

        # list of given emotions
        EMOTIONS = [
            "Angry",
            "Disgusted",
            "Fearful",
            "Happy",
            "Sad",
            "Surprised",
            "Neutral",
        ]

        # store the emoji coreesponding to different emotions
        for _, emotion in enumerate(EMOTIONS):
            emoji_path = os.path.join(self.emoji_path, emotion.lower() + ".png")
            emojis[emotion] = cv2.imread(emoji_path, -1)

        logger.info("Finished loading emojis...")

        return emojis


    def annotate_emotion_data(
        self, emotion_data: List[Dict], image, resize_scale: float
    ) -> None:

        # draw bounding boxes for each detected person
        for data in emotion_data:
            image = draw_bounding_box_annotation(
                image, data["emotion"], int(1 / resize_scale) * np.array(data["bbox"])
            )

        # If there are more than one person in frame, the emoji can be shown for
        # only one, so show a warning. In case of multiple people the stats are shown
        # for just one person
        WARNING_TEXT = "Warning ! More than one person detected !"

        if len(emotion_data) > 1:
            image = annotate_warning(WARNING_TEXT, image)

        if len(emotion_data) > 0:
            # draw emotion confidence stats
            image = annotate_emotion_stats(emotion_data[0]["confidence_scores"], image)
            # draw the emoji corresponding to the emotion
            image = draw_emoji(self.emojis[emotion_data[0]["emotion"]], image)
            
        return image


if __name__ == "__main__":
    import os

    # SAMPLE USAGE
    from emotion_analyzer.media_utils import load_image_path

    ob = EmotionAnalysisVideo(
        face_detector="dlib",
        model_loc="models",
        face_detection_threshold=0.0,
    )

    img1 = load_image_path("data/sample/1.jpg")
    ob.emotion_analysis_video(
        video_path="data/sample/test3.mp4",
        detection_interval=1,
        save_output=True,
        preview=False,
        output_path="data/output.mp4",
        resize_scale=0.5,
    )
