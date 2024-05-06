# Voxify
Video to transcription

Converts a video to audio, returns the transcription from audio

Requirements
* requirements.txt
* ffmpeg installed

Resources
* https://medium.com/@markmikeobrien/whisper-python-for-video-transcription-83db8b890359

Build
* Using pyinstaller
* pyinstaller --noconfirm --onedir --add-data "venv\Lib\site-packages\whisper;whisper\" main.py
* onedir to get _internal folder with necessary libs
* noconfirm cause I got tired of typing yes to confirm overwrite of dist folder