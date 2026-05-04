from video_main import EmotionAnalysisVideo

emotion_recognizer = EmotionAnalysisVideo(
    face_detector="opencv",
    model_loc="models",
    face_detection_threshold=0.0,
)

emotion_recognizer.emotion_analysis_video(
    video_path=None,
    detection_interval=5,
    save_output=False,
    preview=True,
    output_path="data/output.mp4",
    resize_scale=0.3,
)