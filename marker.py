
import argparse
import cv2 
from opencv_paint_chinese import putChineseText

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")

ap.add_argument("-t", "--text", required=True,
	help="text to overlay over the picture")

ap.add_argument("-c", "--coordinate", required=False,
	help="coordinate to overlay the text, in x, y format ")

ap.add_argument("-size", "--size", required=False,
	help="font size ")

ap.add_argument("-displayOnly", "--displayOnly", required=False,
	help="Display Only, no output")

ap.add_argument("-gui", "--gui", required=False,
	help="Launch GUI")


args = ap.parse_args()
# load the image, convert it to grayscale, blur it slightly,
# and threshold it

#print (args.image + ":" + args.text)

if args.gui:


image = cv2.imread(args.image)

x=1000
y=1400

pt = (x,y)

if args.coordinate:
	#print (args.coordinate.split(','))
	pt = (int(args.coordinate.split(',')[0]), int(args.coordinate.split(',')[1]))

size=150
if args.size:
	size = int(args.size)

#cv2.putText (image, args["text"], (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 5.0, (0, 0, 0), 1 )
image = putChineseText (image, args.text, pt, (0, 0, 0), 'jf-openhuninn-1.1.ttf', size)

if args.displayOnly:
	cv2.namedWindow ('frame', cv2.WINDOW_FREERATIO)
	cv2.imshow ('frame',image  )
	cv2.waitKey()
else:
	name = args.image.split('.')
	output_filename =  name[0] + '('+args.text+')' + "." + name[1]
	#print (output_filename)
	cv2.imwrite(output_filename, image)

