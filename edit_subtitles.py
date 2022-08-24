import pathlib
from pathlib import Path
import subprocess
import base64

import ffmpeg
import streamlit as st

import webbrowser
from random import randint

import zipfile
from zipfile import ZipFile

# global variables
uploaded_mp4_file = None
uploaded_srt_file = None
uploaded_mp4_file_length = 0
uploaded_srt_file_length = 0
uploaded_video_file_path = None
srt_file_path = None
mp4_file_path = None
filename = None
downloadfile = None
download_video_bytes = None
edited_video_file_path = None

file_type = ['mp4','mov']



# Check states
# print("subtitling state:", st.session_state.subtitling_state)
# print("load state:", st.session_state.load_state)


@st.experimental_memo
def convert_mp4_to_wav_ffmpeg_bytes2bytes(input_data: bytes) -> bytes:
    """
    It converts mp4 to wav using ffmpeg
    :param input_data: bytes object of a mp4 file
    :return: A bytes object of a wav file.
    """

    # print(srt_file_path)

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


    # Session state to prevent disappearing texts
    if "load_state" not in st.session_state:
        st.session_state.load_state = False


    # Session state for file uploads
    if 'key' not in st.session_state:

        st.session_state.key = str(randint(1000, 100000000))

        print(st.session_state.key)
        

    mp4_placeholder = st.empty()
    srt_placeholder = st.empty()

    uploaded_mp4_file = mp4_placeholder.file_uploader('Upload Your MP4 File', type=file_type, accept_multiple_files=False, on_change=on_change_callback, key=st.session_state.key)

    uploaded_srt_file = srt_placeholder.file_uploader('Upload Your SRT File', type=['srt'], accept_multiple_files=False, on_change=extract_srt, key=st.session_state.key + '1')


    combine_subtitles_btn = st.button("Write subtitles to video")

#     if st.button("New video"):

#         if 'key' not in st.session_state:

#             st.session_state.key = str(randint(1000, 100000000))

#             print(st.session_state.key)

#         else:

#             st.session_state.key = str(randint(1000, 100000000))

#             print(st.session_state.key)
            
#         # Empty all placeholders
#         mp4_placeholder.empty()
#         srt_placeholder.empty()

#         uploaded_mp4_file = mp4_placeholder.file_uploader('Upload Your MP4 File', type=file_type, accept_multiple_files=False, on_change=on_change_callback, key=st.session_state.key + '2')

#         uploaded_srt_file = srt_placeholder.file_uploader('Upload Your SRT File', type=['srt'], accept_multiple_files=False, on_change=extract_srt, key=st.session_state.key + '3')
   


    # When mp4 file uploaded
    if uploaded_mp4_file:
        
        st.write("video uploaded")
        
        uploaded_mp4_file_length = len(uploaded_mp4_file.getvalue())

        filename = pathlib.Path(uploaded_mp4_file.name).stem

        mp4_file_path = HERE / f'./{filename}_binaries.mp4'

        # Update the edited video file path global variable
        edited_video_file_path = HERE / f'./{filename}_edited.mov'

        with open(mp4_file_path, 'wb') as binary_file:
            video_bytes = uploaded_mp4_file.getvalue()
            binary_file.write(video_bytes)

        with open(mp4_file_path, "rb") as file:
            download_video_bytes = file.read()

    # When srt file uploaded
    if uploaded_srt_file:
        
        st.write("subtitles uploaded")

        # print(len(uploaded_srt_file.getvalue()))

        uploaded_srt_file_length = len(uploaded_srt_file.getvalue())

        srt_file_name = uploaded_srt_file.name

        srt_file_name = srt_file_name.split('.')[0]

        # print(srt_file_name)

        srt_file_path = HERE / f'./{srt_file_name}.txt'

        # print(srt_file_path)

        with open(srt_file_path, 'w') as f:

            f.write("")

            f.close()

        with open(srt_file_path, 'a') as f:

            for line in uploaded_srt_file:

                decode_b64 = line.decode("utf-8")
                
                f.write(decode_b64.rstrip() + '\n')

                # st.write(line)


    # If button is clicked
    if combine_subtitles_btn or st.session_state.load_state:
        st.session_state.load_state = True

        print(uploaded_mp4_file_length)
        print(uploaded_srt_file_length)

        if uploaded_mp4_file_length > 0 and uploaded_srt_file_length > 0:
            st.text(f'Size of uploaded "{uploaded_mp4_file.name}" file: {uploaded_mp4_file_length} bytes')

            print(srt_file_path)

            uploaded_video_file_path = HERE / f'./{filename}.mov'

            print(uploaded_video_file_path)

            # Session state to prevent disappearing texts
            if "subtitling_state" not in st.session_state:

                print("Subtitling for the first time!")

                st.session_state.subtitling_state = True

            if st.session_state.subtitling_state:

                print("Burning subtitles..")

                (ffmpeg
                .input(mp4_file_path)
                .output(f'{uploaded_video_file_path}', **{'vf': f'subtitles={filename}.txt'})
                .global_args('-y')
                .run()
                )


                # with open(uploaded_video_file_path, "rb") as fp:
                #     btn = st.download_button(
                #         label="Download converted mp4 file",
                #         data=fp,
                #         file_name=f"{filename}_sub.mp4",
                #         mime="video/mp4"
                #     )

                col1, col2 = st.columns(2)


                video_file = open(uploaded_video_file_path, 'rb')

                video_bytes = video_file.read()

                # Insert video
                with col1:
                    st.video(video_bytes)


                # Insert text editor
                with col2:

                    subtitles = []

                    with open(srt_file_path) as f:

                        for line in f:

                            subtitles.append(line)

                        subtitles = ''.join(subtitles)

                    print(subtitles)

                    txt = st.text_area('Subtitles', subtitles, height=500)                                      

                if st.button("update_subtitles") or st.session_state.subtitling_state == False:
                    
                    # Set the new state for subtitling to false, so that I don't rewrite the old videos
                    st.session_state.subtitling_state = False  


                    st.write("Subtitles updated!")

                    new_srt_file_path = HERE / f'{filename}_edited.srt'

                    # Update the SRT file and update video
                    with open(new_srt_file_path, 'w') as f:

                        f.write(txt)

                        print(txt)

                    print("Burning subtitles..")


                    (ffmpeg
                    .input(mp4_file_path)
                    .output(f'{edited_video_file_path}', **{'vf': f'subtitles={filename}_edited.srt'})
                    .global_args('-y')
                    .run()
                    )


                    # Update the new video and subtitle files

                    col1, col2 = st.columns(2)

                    video_file = open(edited_video_file_path, 'rb')

                    video_bytes = video_file.read()

                    # Insert video
                    with col1:
                        st.video(video_bytes)

                    new_srt_file_path = HERE / f'{filename}_edited.srt'


                    # Insert text editor
                    with col2:

                        subtitles = []

                        with open(new_srt_file_path) as f:

                            for line in f:

                                subtitles.append(line)

                            subtitles = ''.join(subtitles)

                        print(subtitles)

                        txt = st.text_area('Subtitles', subtitles, height=500)

                    # Initialise new zipfile

                    zf = zipfile.ZipFile(f'{filename}_sub_edited.zip', "w")

                    zf.write(edited_video_file_path)

                    zf.write(new_srt_file_path)

                    zf.close()

                    with open(f'{filename}_sub_edited.zip', "rb") as fp:
                        btn = st.download_button(
                            label="Download ZIP",
                            data=fp,
                            file_name=f'{filename}_sub_edited.zip',
                            mime="application/zip"
                        )



                    # with open(edited_video_file_path, "rb") as fp:
                    #     btn = st.download_button(
                    #         label="Download edited mp4 file",
                    #         data=fp,
                    #         file_name=f"{filename}_sub_edited.mp4",
                    #         mime="video/mp4"
                    #     )


                    # with open(srt_file_path) as fp2:
                    #         btn = st.download_button(
                    #         label="Download edited srt file",
                    #         data=fp2,
                    #         file_name=f"{filename}_edited.srt",
                    #         mime="text/srt"
                    #     )
                    

        else:
            print("No video or srt files updated")
            st.write("No video or srt files updated")


# Bump up the upload size with config.toml
# https://stackoverflow.com/questions/64519818/converting-mkv-files-to-mp4-with-ffmpeg-python
# Zip both files together
# Allow display of the new file (ese try-except)
# Insert more if-else, boolean statements to ensure that code don't keep rerunning
