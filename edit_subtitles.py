import pathlib
from pathlib import Path
import subprocess
import base64

import ffmpeg
import streamlit as st

# global variables
uploaded_mp4_file = None
uploaded_srt_file = None
uploaded_mp4_file_length = 0
uploaded_srt_file_length = 0
srt_file_path = None
mp4_file_path = None
filename = None
downloadfile = None
download_video_bytes = None

file_type = 'mp4'


@st.experimental_memo
def convert_mp4_to_wav_ffmpeg_bytes2bytes(input_data: bytes) -> bytes:
    """
    It converts mp4 to wav using ffmpeg
    :param input_data: bytes object of a mp4 file
    :return: A bytes object of a wav file.
    """
    # print('convert_mp4_to_wav_ffmpeg_bytes2bytes')

    print(srt_file_path)

    # args = (
    #         ffmpeg
    #         .input('pipe:', format=f"{file_type}")
    #         .output('pipe:', **{'vf': f'subtitles={srt_file_path}'}, format=f"{file_type}")
    #         .global_args('-y')
    #         .get_args()
    #     )

    # args = (ffmpeg
    #         .input('pipe:', format=f"{file_type}")
    #         .output('pipe:', format='wav')
    #         .global_args('-loglevel', 'error')
    #         .get_args()
    #         )

    # args = (ffmpeg
    #         .input('pipe:', format=f"{file_type}", **{'vcodec' : 'libx264'})
    #         .output('pipe:', format='mp4')
    #         .global_args('-loglevel', 'error')
    #         .get_args()
    #         )
   
    # # print(args)
    # proc = subprocess.Popen(
    #     ['ffmpeg'] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # return proc.communicate(input=input_data)[0]


@st.experimental_memo
def on_file_change(uploaded_mp4_file):
#     print(uploaded_mp4_file.getvalue())
    return convert_mp4_to_wav_ffmpeg_bytes2bytes(uploaded_mp4_file.getvalue())


def on_change_callback():
    """
    It prints a message to the console. Just for testing of callbacks.
    """
    print(f'on_change_callback: {uploaded_mp4_file}')


def extract_srt():
    print("extracting SRT file")



# The below code is a simple streamlit web app that allows you to upload an mp4 file
# and then download the converted wav file.
if __name__ == '__main__':
    st.title('Subtitles Editing App')
    st.markdown("""This is a quick example app for using **ffmpeg** on Streamlit Cloud.
    It uses the `ffmpeg` binary and the python wrapper `ffmpeg-python` library.""")


    HERE = Path(__file__).parent
    print(HERE)

    uploaded_mp4_file = st.file_uploader('Upload Your MP4 File', type=[f'{file_type}'], accept_multiple_files=False, on_change=on_change_callback)

    uploaded_srt_file = st.file_uploader('Upload Your SRT File', type=['srt'], accept_multiple_files=False, on_change=extract_srt)

    combine_subtitles_btn = st.button("Write subtitles to video")


    # When mp4 file uploaded
    if uploaded_mp4_file:
        uploaded_mp4_file_length = len(uploaded_mp4_file.getvalue())

        filename = pathlib.Path(uploaded_mp4_file.name).stem
        # if uploaded_mp4_file_length > 0:
        #     st.text(f'Size of uploaded "{uploaded_mp4_file.name}" file: {uploaded_mp4_file_length} bytes')
        #     downloadfile = on_file_change(uploaded_mp4_file)

        # print("filename: ", filename)
        mp4_file_path = HERE / f'./{filename}_binaries.mp4'

        with open(mp4_file_path, 'wb') as binary_file:
            video_bytes = uploaded_mp4_file.getvalue()
            binary_file.write(video_bytes)

        with open(mp4_file_path, "rb") as file:
            download_video_bytes = file.read() # read a byte (a single character in text)
            # print(download_video_bytes)

    # When srt file uploaded
    if uploaded_srt_file:

        # print(len(uploaded_srt_file.getvalue()))

        uploaded_srt_file_length = len(uploaded_srt_file.getvalue())

        srt_file_name = uploaded_srt_file.name

        srt_file_name = srt_file_name.split('.')[0]

        # print(srt_file_name)

        srt_file_path = HERE / f'./{srt_file_name}.txt'

        # print(srt_file_path)

        with open(srt_file_path, 'a') as f:

            for line in uploaded_srt_file:

                decode_b64 = line.decode("utf-8")
                
                f.write(decode_b64)

                # st.write(line)


    # If button is clicked
    if combine_subtitles_btn:

        print(uploaded_mp4_file_length)
        print(uploaded_srt_file_length)

        if uploaded_mp4_file_length > 0 and uploaded_srt_file_length > 0:
            st.text(f'Size of uploaded "{uploaded_mp4_file.name}" file: {uploaded_mp4_file_length} bytes')

            print(srt_file_path)


            print("Burning subtitles..")

            (ffmpeg
            .input("10_seconds.mp4")
            .output("10_seconds.mov", **{'vf': f'subtitles=10_seconds.srt'})
            .global_args('-y')
            .run()
            )


            with open("10_seconds.mov", "rb") as fp:
                btn = st.download_button(
                    label="Download ZIP",
                    data=fp,
                    file_name=f"{filename}_sub.mp4",
                    mime="video/mp4"
                )


            # downloadfile = on_file_change(uploaded_mp4_file)

        else:
            print("No video or srt files updaated")
            st.write("No video or srt files updated")


        # # Check that the srt to text file is created properly
        # with open(srt_file_path) as fp:
        #     lines = fp.readlines()
        #     for line in lines:
        #         print(line)



    st.markdown("""---""")
    if downloadfile:
        length = len(downloadfile)
        if length > 0:
            st.subheader('After combining the video file and subtitles you can download it below')
            button = st.download_button(label=f"Download combined .{file_type} file",
                            data=downloadfile,
                            file_name=f'{filename}_sub.mp4',
                            mime=f'video/mp4')
            st.text(f'Size of "{filename}.{file_type}" file to download: {length} bytes')
    st.markdown("""---""")




# Bump up the upload size with config.toml
# https://stackoverflow.com/questions/64519818/converting-mkv-files-to-mp4-with-ffmpeg-python


# Convert from byte file to mp4 file and store under "here"
