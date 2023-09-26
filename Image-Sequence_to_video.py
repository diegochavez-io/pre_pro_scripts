import os
import subprocess

def convert_images_to_video_robust(image_folder, output_folder, video_name, fps=60):
    # Make sure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")
    else:
        print(f"Output folder already exists: {output_folder}")

    images = sorted([img for img in os.listdir(image_folder) if img.lower().endswith((".png", ".jpg"))])
    print(images[:5])  # Print the first few image names

    if not images:
        print("No images found in the folder.")
        return
    else:
        print(f"Found {len(images)} images in the folder.")

    # Create a text file with the names of all image files
    with open('images.txt', 'w') as f:
        for img in images:
            f.write(f"file '{os.path.join(image_folder, img)}'\n")

    # Adjusted FFmpeg command to use the text file as input
    command = f'ffmpeg -f concat -safe 0 -r {fps} -i images.txt -c:v libx264 -pix_fmt yuv420p "{os.path.join(output_folder, video_name)}"'
    
    # Print the command for verification
    print("Executing command:", command)
    
    # Run the command and capture output and errors
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(process.stdout)
    print(process.stderr)

    print(f"Video saved to: {os.path.join(output_folder, video_name)}")

    # Remove the text file after creating the video
    os.remove('images.txt')

# Define the paths for the new folder
image_folder = r"G:\My Drive\algo-film\delenda_algo_film_shoot_0822\_warp_sd\_dan_comp\03_segment_38_stable_warpfusion_0.23.0_"
output_folder = r"G:\My Drive\AI\StableWarpFusion\images_out"

# Add the folder name and frame rate to the video file name
output_video = '_03_segment_38_2.mp4'  # Ensure the video has the correct extension

# Call the function
convert_images_to_video_robust(image_folder, output_folder, output_video)
