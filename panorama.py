import cv2
import os

# Defining paths for video input and frame extraction output
video_path = "C:/Users/mahed/OneDrive/Desktop/Fringecore/video.mp4"
frames_dir = "extracted_frames"

# Create a directory to store extracted frames
if not os.path.exists(frames_dir):
    os.makedirs(frames_dir)
    
# Frame Processing

def frame_processing(frame):
    #Resizing the frame
    frame = cv2.resize(frame, (1280, 720))
    #Using color consistency with LAB color
    lab = cv2.cvtColor(frame,cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    return cv2.cvtColor(lab, cv2. COLOR_LAB2BGR)

# Creating Function to extract frames from the video at regular intervals
def frames(video_path, frames_dir, frame_interval=20):
    print("Starting frame extraction...")
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return []

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    saved_frames = []

    for frame_idx in range(0, total_frames, frame_interval):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            print(f"Warning: Unable to read frame at index {frame_idx}.")
            continue

        frame_path = os.path.join(frames_dir, f"frame_{frame_idx:04d}.jpg")
        cv2.imwrite(frame_path, frame)
        saved_frames.append(frame_path)

    cap.release()
    print(f"Extracted {len(saved_frames)} frames successfully.")
    return saved_frames

# Function to stitch frames into a panorama
def create_panorama(image_files):
    print("Starting panorama stitching...")
    images = []

    for img_path in image_files:
        img = cv2.imread(img_path)
        if img is not None:
            images.append(img)
        else:
            print(f"Warning: Unable to load image {img_path}.")

    if not images:
        print("Error: No valid images for stitching.")
        return None

    stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
    status, panorama = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        print("Panorama stitching completed successfully.")
        return panorama
    else:
        print(f"Error during stitching: Status Code {status}")
        return None

# Main workflow
if __name__ == "__main__":
    print("Processing video for panoramic image generation...")

    # Extract frames from the video
    frame_interval = 30  # Adjust as needed for better stitching
    frame_files = frames(video_path, frames_dir, frame_interval=frame_interval)

    if frame_files:
        # Create a panorama from the extracted frames
        panorama = create_panorama(frame_files)

        if panorama is not None:
            output_path = "C:/Users/mahed/OneDrive/Desktop/Fringecore/panorama.jpg"
            cv2.imwrite(output_path, panorama)
            print(f"Panorama saved successfully at: {output_path}")
        else:
            print("Panorama creation failed. Please check the frames and try again.")
    else:
        print("No frames were extracted. Please check the video path and settings.")
