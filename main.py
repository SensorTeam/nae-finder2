"""
==================================================================
AUTHOR: HIEN VU
LAST MODIFIED: 20-04-18
==================================================================
Locates potential eyeshine signals from an image
INPUT: image (.jpg .png .tiff) containing eyeshine signal
OUTPUT: number of detected pairs, .jpg file with potential eyeshine 
			circled, saved as `image-name_circled.jpg`
USAGE: execute from terminal
			`python3 main.py -i path-to-image`
==================================================================
"""

from find_eye import *
from find_pairs import *
from get_colour import *
import argparse
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the normal image file")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])
orig = image.copy()
new = image.copy()

# find potential eyes (appropriate size and shape)
contours = find_eye(image)

# find pairs (signal duality and signal orientation)
[con_pairs, pair_det] = find_pairs(image, contours)
num_pairs = len(con_pairs)

# results
fname = os.path.basename(args["image"])
print("SEARCHED " + str(fname))
print("FOUND " + str(num_pairs) + " PAIR/S")

# set of colours for labelling pairs
colours = [(255,0,0),(0,0,255),(0,255,0),(255,255,0),(255,0,255),
				(0,255,255),(100,200,100),(100,0,200),(200,100,200),(200,100,100)]
i=0
# circle around the pairs found in the image
for pair in con_pairs:
	i+=1
	col = colours[i%10]
	if len(pair)==2:
		for eye in pair:
			(cX, cY), radius = cv2.minEnclosingCircle(eye)
			cv2.circle(new, (int(cX), int(cY)), int(radius+8), col, 5)
	else:
		pass
# save circled image
cv2.imwrite(fname[0:-4]+"_circled.jpg", new)

