# AsciiVideo
Square font courtesy of Wouter van Oortmerssen: http://strlen.com/square/.

Tested using FFmpeg version 3.2.10 (very specifically, this version: http://snapshot.debian.org/archive/debian/20180602T224521Z/pool/main/f/ffmpeg/ffmpeg_3.2.10-1%7Edeb9u1_amd64.deb) and Python version 3.5.3 on Debian 9.

Before running for the first time, run `pip install -r requirements.txt` to install required third-party packages.


##HOW TO USE

Arguments:

*-i/--input*: Specifies the video to be converted.

*-s/--size*: Specifies the width (in pixels) of the final output video.

*-f/--font-size*: Specifies the font size to be used for the ASCII characters.

*-a/--audio*: Determines whether or not to include audio in the final video. If set to `1`, includes audio. If set to any other number, does not include audio.


I find that a size of 1280 and a font size of 12 works well.
