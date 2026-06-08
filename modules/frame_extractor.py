import os
import cv2
import uuid


def frame_extractor(input_dir, output_dir, fps, start=0.0, end=1.0):
    """
    Extract frames from videos in input_dir.

    Parameters:
    - fps: number of frames per second to extract (not dependent on video fps)
    - start: float (0 to 1), start portion of video
    - end: float (0 to 1), end portion of video

    Output:
    - Saves extracted frames as .png in output_dir with unique names
    """

    os.makedirs(output_dir, exist_ok=True)

    video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".webm"}

    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)

        if not os.path.isfile(file_path):
            continue

        ext = os.path.splitext(filename)[1].lower()
        if ext not in video_extensions:
            continue

        cap = cv2.VideoCapture(file_path)

        if not cap.isOpened():
            print(f"Failed to open: {filename}")
            continue

        video_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        start_frame = int(total_frames * start)
        end_frame = int(total_frames * end)

        if end_frame <= start_frame:
            print(f"Invalid range for: {filename}")
            cap.release()
            continue

        frame_interval = max(int(video_fps / fps), 1)

        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        frame_idx = start_frame
        saved_count = 0

        while frame_idx < end_frame:
            ret, frame = cap.read()
            if not ret:
                break

            if (frame_idx - start_frame) % frame_interval == 0:
                unique_name = f"{uuid.uuid4().hex[:12]}.png"
                save_path = os.path.join(output_dir, unique_name)
                cv2.imwrite(save_path, frame)
                saved_count += 1

            frame_idx += 1

        cap.release()

        print(f"{filename}: extracted {saved_count} frames")