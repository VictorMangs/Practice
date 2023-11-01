# Laina Posner
# VT, ECE 5444
# HW 4, the Pavlidis contour extractor, the Gauss area estimation method and Discrete Curve Evolution

from contextlib import nullcontext
import os
import cv2
from cv2 import FlannBasedMatcher
from cv2 import contourArea
import numpy as np
from regex import I
import matplotlib.pyplot as plt


# 5pts, Load, binarize and write image
# 10pts, Contour extraction (your Pavlidis function)
# 10pts, Area estimation from contour points (your Gauss area function)
# 10pts, Point removal from contour (your OnePassDCE function)
# 5pts, Proper console output

# ------------------------------------------------------------------------------

# a. Load the image and convert to grayscale. 

pathname = "C:/Users/Victor2021/Downloads/"
os.chdir(pathname) # changing directory

png = ".png"
filename = "US" # filename input options:  "US" , "hand" 
img_filename = filename + png

img = cv2.imread(img_filename)
# copy = cv2.imread(img_filename)

gray_img = cv2.imread(img_filename, 0)
# gray_copy = cv2.imread(img_filename, 0)

# ------------------------------------------------------------------------------

# b. Convert to a binary image using Otsu’s thresholding method (you may use cv2.thresold()). 
# Note that I want the hand and the continental US to be foreground (white). 

# # # used to binarize the image based on pixel intensities
# # # input -> grayscale imange and a threshold, output -> binary img
# # # intensity of a pixel in the input image > than a threshold, output pixel is marked as white (foreground),
# # # manually specify the threshold value. Otsu is a good example of auto thresholding
# Set total number of bins in the histogram

blur = cv2.GaussianBlur(gray_img,(5,5),0)

thresh, imgresult = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)   
#                            (source, thresholdValue, maxVal, thresholdingTechnique)  

# cv2.imwrite(pathname + filename + 'otsu.png',otsuimgresult)
cv2.imshow(filename + ' otsu', imgresult)
# print(otsuimgresult)
# ------------------------------------------------------------------------------

# c. Since the object may, in general, touch the edge of the binary image and this can be complicated 
# to handle in the contour tracing, fill the first and last rows and the first and last columns of the 
# binary image with black. Thus, we have put a one-pixel black boundary around the remainder 
# of the image. 

height = img.shape[0] # y
width = img.shape[1] # x
# print(height, width) # 531, 494 (hand)

for h in (range(width)): #img[y,x]
    # print(h)
    imgresult[0][h-1] = 0
    imgresult[height-1][h-1] = 0

for w in (range(height)):
    imgresult[w-1][0] = 0
    imgresult[w-1][width-1] = 0

# cv2.imshow("value",imgresult)

# ------------------------------------------------------------------------------

# d. Write out the binarized image to a file. 

cv2.imwrite(pathname + filename + 'binary.png',imgresult)

# ------------------------------------------------------------------------------

# e. Find a point on the edge of the object. 
# You can assume that the edge is the first white pixel on the line halfway down the image. 

y_start = int((imgresult.shape[0]) / 2)
x_start = 0
count = 0

for i in reversed(range(width)):
    if imgresult[y_start][i] == 255:
        x_start = i
    count +=1

start = [y_start,x_start]
print("start point",start)

# ------------------------------------------------------------------------------

# f. Call your own Pavlidis function to extract the contour of the object. 

# 255 = white
# 0 = blackaa
# img[y][x]
rotate = []
direction = 0
# point =[]
contour = []

# p1 = [y_start+1,x_start-1] # left
# p2 = [y_start+1,x_start] # middle 
# p3 = [y_start+1,x_start+1] # right

x = x_start # 139
y = y_start # 266
point = [0,0]
count = 0
while start != point:
    if direction == 0:
        p1 = [y+1,x-1] # left
        p2 = [y+1,x] # middle 
        p3 = [y+1,x+1] # right
        count+=1
        print('0', count)
        # print('direction0')
        # print(imgresult[p1[0], p1[1]])
        if imgresult[p1[0], p1[1]] == 255:
            point = p1
            y = p1[0]
            x = p1[1]
            contour.append([y,x])
            direction = 3
            print('0-p1', p1)
        elif imgresult[p2[0], p2[1]] == 255:
            point = p2
            y = p2[0]
            x = p2[1]
            contour.append([y,x])
            direction = 0
            print('0-p2', p1)
        elif imgresult[p3[0], p3[1]] == 255:
            point = p3
            y = p3[0]
            x = p3[1]
            contour.append([y,x])
            direction = 0
            print('0-p3', p1)
        else:
            direction = 1
    elif direction == 1:
        p1 = [y+1,x+1]# left
        p2 = [y,x+1] # middle 
        p3 = [y-1,x+1] # right
        count+=1
        print('1', count)

        #print('direction1')
        if imgresult[p1[0], p1[1]] == 255:
            point = p1
            y = p1[0]
            x = p1[1]
            contour.append([y,x])
            direction = 0
            print('1-p1', p1)
        elif imgresult[p2[0], p2[1]] == 255:
            point = p2
            y = p2[0]
            x = p2[1]
            contour.append([y,x])
            direction = 1
            print('1-p2', p1)
        elif imgresult[p3[0], p3[1]] == 255:
            point = p3
            y = p3[0]
            x = p3[1]
            contour.append([y,x])
            direction = 1
            print('1-p3', p1)
        else:
            direction = 2
    elif direction == 2:
        p1 = [y-1,x+1]# left
        p2 = [y-1,x] # middle 
        p3 = [y-1,x-1] # right
        count+=1
        print('2', count)

        #print('direction2')
        if imgresult[p1[0], p1[1]] == 255:
            point = p1
            y = p1[0]
            x = p1[1]
            contour.append([y,x])
            direction = 1
            print('2-p1', p1)
        elif imgresult[p2[0], p2[1]] == 255:
            point = p2
            y = p2[0]
            x = p2[1]
            contour.append([y,x])
            direction = 2
            print('2-p2', p1)
        elif imgresult[p3[0], p3[1]] == 255:
            point = p3
            y = p3[0]
            x = p3[1]
            contour.append([y,x])
            direction = 2
            print('2-p3', p1)
        else:
            direction = 3
    elif direction == 3:
        p1 = [y-1,x-1]# left
        p2 = [y,x-1] # middle 
        p3 = [y+1,x-1] # right
        count+=1
        print('3', count)
        # print('direction3')
        if imgresult[p1[0], p1[1]] == 255:
            point = p1
            y = p1[0]
            x = p1[1]
            contour.append([y,x])
            direction = 2
            print('3-p1', p1)
        elif imgresult[p2[0], p2[1]] == 255:
            point = p2
            y = p2[0]
            x = p2[1]
            contour.append([y,x])
            direction = 3
            print('3-p2', p1)
        elif imgresult[p3[0], p3[1]] == 255:
            point = p3
            y = p3[0]
            x = p3[1]
            contour.append([y,x])
            direction = 3
            print('3-p3', p1)
        else:
            direction = 0
    else:
        print("you broke it")

print('POINTSSSS')
print(contour)


x = [point[0] for point in contour]
y = [point[1] for point in contour]

plt.plot(x, y)
plt.show()
