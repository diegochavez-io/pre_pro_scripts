import os
import subprocess
import math
import random
import uuid

# Parameters for easy configuration
video_file_path = r"G:\My Drive\AI\SGXL_Output\inner_paint-koi_snap_08_670_870_w150_shu_15.mp4"  # Added the drive letter
output_directory = r"G:\My Drive\dataset-footage\SDXL\inner_paint-koi_snap_08_processed_10"
clip_duration_in_seconds = 10  # Change this value to your desired clip length
num_clips_to_export = 10  # Number of random clips to export

def get_video_length(video_file_path):
    if not os.path.exists(video_file_path):
        print(f"The file {video_file_path} does not exist.")
        return 0  # Return 0 if the file does not exist

    command = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_file_path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    try:
        return float(result.stdout)
    except ValueError:
        print(f"Error getting video length. STDOUT: {result.stdout}, STDERR: {result.stderr}")
        return 0  # Return 0 if the output is not a valid float

def splice_video(video_file_path, clip_length, output_dir, num_clips_to_export):
    video_length = get_video_length(video_file_path)
    if video_length == 0:
        return  # Exit the function if the video length is 0

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    used_starts = []

    for i in range(num_clips_to_export):
        while True:
            clip_start = random.uniform(0, video_length - clip_length)
            if all(abs(clip_start - used) > clip_length for used in used_starts):
                break

        used_starts.append(clip_start)
        clip_end = clip_start + clip_length
        random_id = uuid.uuid4().hex[:6]  # Generate a random 6-character identifier
        output_file_path = os.path.join(output_dir, f"random_clip_{i+1}_{random_id}.mp4")

        command = ["ffmpeg", "-i", video_file_path, "-ss", str(clip_start), "-to", str(clip_end), "-c", "copy", output_file_path]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode != 0:
            print(f"Error occurred while cropping the video from {clip_start:.2f} to {clip_end:.2f} seconds. STDERR: {result.stderr}")
        else:
            print(f"Created random clip {i+1} from {clip_start:.2f} to {clip_end:.2f} seconds at {output_file_path}")

# Main execution
splice_video(video_file_path, clip_duration_in_seconds, output_directory, num_clips_to_export)
