import pathlib
import subprocess

import ffmpeg
import streamlit as st

# global variables
uploaded_mp4_file = None
uploaded_mp4_file_length = 0
filename = None
downloadfile = None

file_type = 'mp4'


@st.experimental_memo
def convert_mp4_to_wav_ffmpeg_bytes2bytes(input_data: bytes) -> bytes:
    """
    It converts mp4 to wav using ffmpeg
    :param input_data: bytes object of a mp4 file
    :return: A bytes object of a wav file.
    """
    # print('convert_mp4_to_wav_ffmpeg_bytes2bytes')
    args = (
            ffmpeg
            .input('pipe:', format=f"{file_type}")
            .output('pipe:', **{'vf': f'subtitles={sub1}'})
            .global_args('-y')
            .get_args()
        )

#     args = (ffmpeg
#             .input('pipe:', format=f"{file_type}")
#             .output('pipe:', format='wav')
#             .global_args('-loglevel', 'error')
#             .get_args()
#             )
   
    # print(args)
    proc = subprocess.Popen(
        ['ffmpeg'] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return proc.communicate(input=input_data)[0]


@st.experimental_memo
def on_file_change(uploaded_mp4_file):
    print(uploaded_mp4_file.getvalue())
    return convert_mp4_to_wav_ffmpeg_bytes2bytes(uploaded_mp4_file.getvalue())


def on_change_callback():
    """
    It prints a message to the console. Just for testing of callbacks.
    """
    print(f'on_change_callback: {uploaded_mp4_file}')


# The below code is a simple streamlit web app that allows you to upload an mp4 file
# and then download the converted wav file.
if __name__ == '__main__':
    st.title('Subtitles Editing App')
    st.markdown("""This is a quick example app for using **ffmpeg** on Streamlit Cloud.
    It uses the `ffmpeg` binary and the python wrapper `ffmpeg-python` library.""")

    uploaded_mp4_file = st.file_uploader('Upload Your MP4 File', type=[f'{file_type}'], on_change=on_change_callback)

    if uploaded_mp4_file:
        uploaded_mp4_file_length = len(uploaded_mp4_file.getvalue())
        filename = pathlib.Path(uploaded_mp4_file.name).stem
        if uploaded_mp4_file_length > 0:
            st.text(f'Size of uploaded "{uploaded_mp4_file.name}" file: {uploaded_mp4_file_length} bytes')
            downloadfile = on_file_change(uploaded_mp4_file)

    st.markdown("""---""")
    if downloadfile:
        length = len(downloadfile)
        if length > 0:
            st.subheader('After conversion to WAV you can download it below')
            button = st.download_button(label="Download .wav file",
                            data=downloadfile,
                            file_name=f'{filename}.wav',
                            mime='audio/wav')
            st.text(f'Size of "{filename}.wav" file to download: {length} bytes')
    st.markdown("""---""")
