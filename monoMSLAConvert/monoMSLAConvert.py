#!/usr/bin/python3
#
# Copyright 2020 Photonsters
# Jarrod A. Smith (MakerMatrix)
#
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

# Parse the command line
try:
	infile = sys.argv[1]
	outfile = sys.argv[2]
except:
	print ("Usage: " + sys.argv[0] + " <inFile> <outFile>")
	exit(1)

# Open the input image
try:
	inImg = Image.open(infile)
except:
	print( "ERROR: Could not open " + infile + " for reading.")
	exit(1)

# Get the input image type and decide which way we will convert it
inType = inImg.mode
if inType == "RGB" or inType == "RGBA":
	inImg = inImg.convert("RGB")
	converting = "C2G"
	print("Converting", inImg.size, "RGB-encoded grayscale image to full-resolution gray.") 
elif inType == "LA" or inType == "L":
	inImg = inImg.convert("L")
	converting = "G2C"
	print("Converting", inImg.size, "full-resolution grayscale image to RGB-encoded grays.")
else:
	print( "You did not supply a suitable image.\nRGB, RGB/alpha, ")
	print( "8-bit grayscale or 8-bit grayscale/alpha are supported.")
	exit()

# Do an rgb-encoded to grayscale conversion
if converting == "C2G":
	rgbPixels = inImg.load() # Create a pixel access object
	# Create empty grayscale output image with the converted X-dimension
	outImg = Image.new("L", (inImg.width*3, inImg.height))
	grayPixels = outImg.load() # Create a pixel object for converted output
	for x in range(inImg.width):  # Loop over the columns
		for y in range(outImg.height):  # Loop over the rows
			for channel in range(3):  # Loop over this pixel's R, G, B channels
				# Build a gray pixel from the current channel's value
				newPixel = (rgbPixels[x, y][channel])
				# Assign the new gray pixel into the correct full-res index
				grayPixels[((x*3)+channel), y] = newPixel
# Do a grayscale to rgb-encoded conversion				
elif converting == "G2C":
	grayPixels = inImg.load() # Pixel access object
	# Create empty RGB output image with the converted X-dimension
	outImg = Image.new("RGB", (int(inImg.width/3), inImg.height)) #
	rgbPixels = outImg.load() # Create pixel object for converted output
	for x in range(outImg.width): # Loop over the output columns
		inX = x * 3 # The input X-dimension is 3x the output rgb X-dimension.
		for y in range(outImg.height):  # Loop over the rows
			# Build a new rgb-encoded pixel from the next three gray pixels
			newPixel = (grayPixels[inX, y],
					grayPixels[inX+1, y],
					grayPixels[inX+2, y])
			rgbPixels[x, y] = newPixel # Assign the rgb-encoded pixel

# Save the converted image
try:
	outImg.save(outfile)
except:
	print( "ERROR: Could not open " + outfile + " for writing.")
	exit(1)
