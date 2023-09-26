import cv2
import os
import random
import zipfile

# Parameters
source_folder = r"G:\My Drive\algo-film\delenda_algo_film_shoot_0822"  # Folder containing all the video files
image_count = 150  # Number of images to extract per video
zip_output = False  # Set to True if you want to zip the output folder

# Create a single folder for all extracted frames
output_folder = os.path.join(source_folder, "extracted_frames")
os.makedirs(output_folder, exist_ok=True)

# Function to extract frames from a video file and save them as images
def extract_frames(video_path, image_count):
    vidcap = cv2.VideoCapture(video_path)
    vidcap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('C', 'Y', 'U', 'V'))  # Set the encoding
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    if image_count > total_frames:
        print(f"Number of frames to extract from {video_path} is greater than the total frames in the video. Extracting {total_frames} frames instead.")
        image_count = total_frames

    if image_count == 0:
        print(f"No frames to extract from {video_path}.")
        return

    # Calculate a minimum distance between the frames
    min_distance = total_frames // image_count

    # Generate a list of frame numbers ensuring the minimum distance
    frames_to_extract = sorted([random.randint(i * min_distance, (i + 1) * min_distance - 1) for i in range(image_count)])

    success, image = vidcap.read()
    count = 0
    while success:
        if count in frames_to_extract:
            # Save the image with a name that includes the original video filename for clarity
            cv2.imwrite(os.path.join(output_folder, f"{os.path.splitext(os.path.basename(video_path))[0]}_frame{count}.jpg"), image)
            frames_to_extract.remove(count)
        success, image = vidcap.read()
        count += 1

# Function to zip the output folder
def zip_folder(output_folder):
    zipf = zipfile.ZipFile(f"{output_folder}.zip", 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(output_folder, '..')))
    zipf.close()

# Main function to process the videos
def main():
    for video_file in os.listdir(source_folder):
        if video_file.endswith(('.mp4', '.mov', '.avi', '.mkv')):  # Add other video formats if needed
            video_path = os.path.join(source_folder, video_file)
            print(f"Extracting frames from {video_path}...")
            extract_frames(video_path, image_count)
    
    # Zip the output folder if zip_output is True
    if zip_output:
        zip_folder(output_folder)

if __name__ == "__main__":
    main()
