import cv2
import time
import os
import ffmpeg
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def video_to_frames(input_loc, output_loc):
    """Function to extract frames from input video file
    and save them as separate frames in an output directory.
    Args:
        input_loc: Input video file.
        output_loc: Output directory to save the frames.
    Returns:
        None
    """
    try:
        os.makedirs(output_loc, exist_ok = True)
    except OSError:
        pass
    # Log the time
    time_start = time.time()
    # Start capturing the feed
    cap = cv2.VideoCapture(input_loc)
    # Find the number of frames
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print ("Number of frames: ", video_length)
    count = 0
    print ("Converting video..\n")
    # Start converting the video
    while cap.isOpened():
        # Extract the frame
        ret, frame = cap.read()
        # Write the results back to output location.
        cv2.imwrite(output_loc + "/%#05d.jpg" % (count+1), frame)
        count = count + 1
        # If there are no more frames left
        if (count > (video_length-1)):
            # Log the time again
            time_end = time.time()
            # Release the feed
            cap.release()
            # Print stats
            print ("Done extracting frames.\n%d frames extracted" % count)
            print ("It took %d seconds forconversion." % (time_end-time_start))
            break

#fetch total number of frames in the video and the frame rate
def get_video_metadata(video_path):
    video = cv2.VideoCapture(video_path)
    #total number of frames
    total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    #frame rate
    fps = video.get(cv2.CAP_PROP_FPS)
    return (total,fps)

#stitch frames at the original fps to form the source video
def stitch_video(frame_path, fps):
    (
        ffmpeg
        .input(f'{frame_path}/*.jpg', pattern_type='glob', framerate=fps)
        .output('stitched_video.mp4')
        .run()
    )

#extract audio from the video file
def extract_audio(video_path, audio_path):
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)

#concatenate the audio and the stitched video to form the original video
def concat_audio_video(video_path, audio_path, output_path)
    input_video = ffmpeg.input(video_path)
    input_audio = ffmpeg.input(audio_path)

    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(output_path).run()

#trim videos to a desired duration
def trim_videos(input_video_folder, start_duration, end_duration, target_folder):
    #duration in seconds
    videos = os.listdir(input_video_folder)
    for vid in videos:
        try:
            orig_name,ext = os.path.splitext(vid)
            new_name = f'trimmed_{orig_name}{ext}'
            ffmpeg_extract_subclip(f'{input_video_folder}/{vid}', start_duration, end_duration, targetname=f'{target_folder}/{new_name}')
        except Exception as e:
            os.rename(os.path.join(input_video_folder,vid), os.path.join(target_folder, vid))
            print(e)
            print(vid)


