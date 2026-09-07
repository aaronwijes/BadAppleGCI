import cv2
import numpy as np
from PIL import Image
import os
import json

# --- Configuration ---
OUTPUT_IMAGE_FOLDER = "bad_apple_frames"
FRAME_RATE = 30  # Match the target frame rate of the Pico project

# The final viewable size of the 7x7 video/images
OUTPUT_WIDTH = 480
OUTPUT_HEIGHT = 480

def get_video_filename():
    """Prompts the user for a video file and validates it."""
    while True:
        filename = input("Enter the name of the video file (e.g., my_video.mp4): ")
        if os.path.exists(filename):
            return filename
        print(f"Error: File '{filename}' not found. Please make sure it's in the same folder as the script.")

def main():
    """
    Main function to process the video and create an 7x7 preview version.
    """
    frames = {}
    cache = {}
    video_source = get_video_filename()

    print(f"Opening video file: {video_source}")
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # --- Create directories ---
    if not os.path.exists(OUTPUT_IMAGE_FOLDER):
        os.makedirs(OUTPUT_IMAGE_FOLDER)
    print(f"Will export image frames to: ./{OUTPUT_IMAGE_FOLDER}/")

    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break # End of video

        # --- Process the frame to 7x7 monochrome ---
        img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img_pil = img_pil.resize((7, 7), Image.LANCZOS)
        img_pil = img_pil.convert('1', dither=Image.FLOYDSTEINBERG)

        # --- Write raw array data ---
        frames[f"{frame_count:05d}"] = np.array(img_pil).astype(np.uint8).tolist()


        # --- Write frame cache data ---
        frame_array = frames[f"{frame_count:05d}"]
        if str(frame_array) in cache:
            if f"{frame_count:05d}" not in cache[str(frame_array)]:
                cache[str(frame_array)].append(f"{frame_count:05d}")
        else:
            cache[str(frame_array)] = [f"{frame_count:05d}"]

        # --- Scale up for viewing ---
        processed_frame_np = np.array(img_pil).astype(np.uint8) * 255
        scaled_frame = cv2.resize(processed_frame_np, (OUTPUT_WIDTH, OUTPUT_HEIGHT), interpolation=cv2.INTER_NEAREST)
        
        # Save the scaled-up grayscale frame directly
        image_filename = os.path.join(OUTPUT_IMAGE_FOLDER, f"frame_{frame_count:05d}.png")
        cv2.imwrite(image_filename, scaled_frame)

        frame_count += 1
        print(f"Processing frame {frame_count}...")

    # Release everything when the job is done
    cap.release()
    cv2.destroyAllWindows()

    open("frames.json", "w").write(json.dumps(frames, indent=2))
    open("cache.json", "w").write(json.dumps(cache, indent=2))

    print("\nConversion complete!")
    print(f"Image frames saved in ./{OUTPUT_IMAGE_FOLDER}/")
    print(f"Frame data saved in ./frames.json")
    print(f"Duplicate frame data saved in ./cache.json")

if __name__ == "__main__":
    main()
