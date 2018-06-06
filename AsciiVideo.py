import sys
import cv2
import os
import glob
import subprocess
import re
from optparse import OptionParser
from PIL import Image, ImageFont, ImageDraw
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor

'''Number of cores to use for multi-core processes (half of what your CPU has)'''
cores = int(cpu_count() / 2)

'''Function that converts single image to an image made up of only ASCII characters'''
def imgToAscii(filename):
    '''Opens input image, scales it down so the characters display well in the final image, loads the image as an array
    of pixels, and creates a new array of pixels that represents the input image in grayscale'''
    image = Image.open(filename)
    image.thumbnail((128, 128))
    imagePixels = image.load()
    grayscaleArray = [[(0, 0, 0) for x in range(image.size[0])] for y in range(image.size[1])]
    for y in range(len(grayscaleArray)):
        for x in range(len(grayscaleArray[0])):
            coordinate = imagePixels[x,y]
            color = 0.21*coordinate[0]+0.72*coordinate[1]+0.07*coordinate[2]
            grayscaleArray[y][x] = (color, color, color)

    '''Creates an array of ASCII characters which represents the grayscale version of the input image'''
    asciiArray = [["" for x in range(image.size[0])] for y in range(image.size[1])]
    for y in range(len(asciiArray)):
        for x in range(len(asciiArray[0])):
            color = grayscaleArray[y][x][0]
            if(color <= 30):
                asciiArray[y][x] = "@"
            elif(color > 30 and color <= 55):
                asciiArray[y][x] = "%"
            elif(color > 55 and color <= 80):
                asciiArray[y][x] = "#"
            elif(color > 80 and color <= 105):
                asciiArray[y][x] = "*"
            elif(color > 105 and color <= 130):
                asciiArray[y][x] = "+"
            elif(color > 130 and color <= 155):
                asciiArray[y][x] = "="
            elif(color > 155 and color <= 180):
                asciiArray[y][x] = "-"
            elif(color > 180 and color <= 205):
                asciiArray[y][x] = ":"
            elif(color > 205 and color <= 230):
                asciiArray[y][x] = "."
            else:
                asciiArray[y][x] = " "
    characters = []
    for y in range(len(asciiArray)):
        line = ""
        for x in range(len(asciiArray[0])):
            line = line + asciiArray[y][x]
        characters.append(line)
    
    '''Loads a square monospaced font, determines the width and height necessary to draw the characters to an image,
    determines the height of each individual line, creates a new image to draw the characters to, and draws the
    characters to that image'''
    font = os.path.abspath(os.path.join(os.getcwd(), os.pardir, "square.ttf"))
    squareFont = ImageFont.truetype(font, int(options.fontsize), encoding="unic")
    textWidth = squareFont.getsize(characters[0])[0]
    textHeight = squareFont.getsize(characters[0])[1]*len(characters)
    lineHeight = squareFont.getsize(characters[0])[1]
    asciiImage = Image.new("RGB", (textWidth, textHeight), (255, 255, 255))
    draw = ImageDraw.Draw(asciiImage)
    yCoord = 0
    for y in range(len(characters)):
        draw.text((0,yCoord), characters[y], font=squareFont, fill="#000000")
        yCoord = yCoord + lineHeight

    '''Saves the final image at the user-specified size'''
    i = re.findall(r"\d+", filename)
    i = int(i[0])
    asciiImage.thumbnail((int(options.imageSize), int(options.imageSize)))
    asciiImage.save("output%d.jpg" % (i + 1), "JPEG")
    os.remove(filename)
    print("Frame %d created" % (i + 1))

'''Sets up an option parser, adds options, and parses them'''
parser = OptionParser()
parser.add_option("-i", "--input", dest="filename")
parser.add_option("-s", "--size", dest="imageSize")
parser.add_option("-f", "--font-size", dest="fontsize")
parser.add_option("-a", "--audio", dest="audio")
(options, args) = parser.parse_args()

'''Opens input video and splits it up into its individual frames'''
video = cv2.VideoCapture(options.filename)
count = 1
success = True
try:
    os.chdir(os.path.abspath(os.path.join(os.getcwd(), "frames")))
except:
    os.mkdir("frames")
    os.chdir(os.path.abspath(os.path.join(os.getcwd(), "frames")))
while success:
    success, image = video.read()
    cv2.imwrite("frame%d.jpg" % count, image)
    count += 1
os.remove("frame%d.jpg" % (count - 1))

'''Runs the imgToAscii function on each frame of the input video, uses half of CPU's available cores'''
filenames = os.listdir()
with ProcessPoolExecutor(cores) as pool:
    pool.map(imgToAscii, filenames)

'''Writes ASCII frames to an MP4, then uses ffmpeg to convert that MP4 to a WEBM'''
fps = video.get(cv2.CAP_PROP_FPS)
frame1 = cv2.imread("output2.jpg")
height, width, layers = frame1.shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
outputVideo = cv2.VideoWriter("output.mp4", fourcc, fps, (width, height))
for i in range(len(os.listdir())):
    img = cv2.imread("output%d.jpg" % (i + 1))
    outputVideo.write(img)
outputVideo.release()
video.release()
cv2.destroyAllWindows()
outputWEBM = os.path.abspath(os.path.join(os.getcwd(), os.pardir, "output.webm"))
if(int(options.audio) == 1):
    subprocess.call("ffmpeg -i %s -vn -acodec libvorbis -threads %d audio.ogg" % (options.filename, cores), shell=True)
    subprocess.call("ffmpeg -i output.mp4 -i audio.ogg -c:v libvpx-vp9 -crf 31 -b:v 0 -threads %d %s" % (cores, outputWEBM), shell=True)
else:
    subprocess.call("ffmpeg -i output.mp4 -c:v libvpx-vp9 -crf 31 -b:v 0 -threads %d %s" % (cores, outputWEBM), shell=True)
os.remove("output.mp4")
for f in glob.glob("output*.jpg"):
    os.remove(f)