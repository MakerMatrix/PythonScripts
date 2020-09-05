#!/usr/bin/python3

from PIL import Image
import sys

# Variables to track whether the conversion is gray to color, or color to gray
G2C = 0
C2G = 1

try:
	infile = sys.argv[1]
	outfile = sys.argv[2]
except:
	print ("Usage: " + sys.argv[0] + " inFile outFile")
	exit()

inImg = Image.open(infile)
print( infile + " is " + str(inImg.size) + " " + inImg.mode)

inType = inImg.mode
if inType == "RGB" or inType == "RGBA":
	inImg = inImg.convert("RGB")
	converting = C2G
elif inType == "LA" or inType == "L":
	inImg = inImg.convert("L")
	converting = G2C
else:
	print( "You did not supply a suitable image.\nRGB, RGB/alpha, ")
	print( "8-bit grayscale or 8-bit grayscale/alpha are supported.")
	exit()

if converting == C2G:
	rgbPixels = inImg.load()
	outImg = Image.new("L", (inImg.width*3, inImg.height))
	grayPixels = outImg.load()
	for x in range(inImg.width):
		for y in range(outImg.height):
			for channel in range(3):
				newPixel = (rgbPixels[x, y][channel])
				grayPixels[((x*3)+channel), y] = newPixel
				
elif converting == G2C:
	grayPixels = inImg.load()
	outImg = Image.new("RGB", (int(inImg.width/3), inImg.height))
	rgbPixels = outImg.load()
	for x in range(outImg.width):
			inX = x * 3
			for y in range(outImg.height):
				newPixel = (grayPixels[inX, y],
							grayPixels[inX+1, y],
							grayPixels[inX+2, y])
				rgbPixels[x, y] = newPixel

outImg.save(outfile)
