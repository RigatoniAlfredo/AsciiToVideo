# AsciiVideo
Square font courtesy of Wouter van Oortmerssen: http://strlen.com/square/.

Tested using FFmpeg version 3.2.10 (very specifically, this version: http://snapshot.debian.org/archive/debian/20180602T224521Z/pool/main/f/ffmpeg/ffmpeg_3.2.10-1%7Edeb9u1_amd64.deb) and Python version 3.5.3 on Debian 9.

Before running for the first time, run `pip install -r requirements.txt` to install required third-party packages.

## HOW TO USE

Required Arguments:

*-i/--input*: Specifies the video to be converted.

Optional Arguments:

*-s/--size*: Specifies the width (in pixels) of the final output video. Defaults to 1280.

*-f/--font-size*: Specifies the font size to be used for the ASCII characters. Defaults to 12.

*-c/--color*: If passed, output the final video in color.

*-a/--audio*: If passed, include audio in the final video.

*--vp9*: If passed, output WEBM using the VP9. Otherwise, outputs in VP8.
