#!/usr/bin/python3
#
# Copyright 2020 Jarrod A. Smith (MakerMatrix)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
