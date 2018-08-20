# SenseHawk Technologies Assignment - 1
# Name - Abhinandan Dogra

import cv2
import numpy as np
import sys
import argparse

def zoom(path, x_pivot, y_pivot, scale):

	img = cv2.imread(path)

	# Creating a window with size of original image around pivot point.
	
	top_left_x = int(int(x_pivot) - (float(1)/float(scale) * float(1)/float(2) * img.shape[1]))
	top_left_y = int(int(y_pivot) - (float(1)/float(scale) * float(1)/float(2) * img.shape[0]))

	bottom_right_x = int(top_left_x + (float(1)/float(scale) * img.shape[1]))
	bottom_right_y = int(top_left_y + (float(1)/float(scale) * img.shape[0]))


	# If the window goes out of scope of original image size, it is adjusted by this
	if (top_left_x < 0):
		bottom_right_x = bottom_right_x - top_left_x
		top_left_x = 0
	if (top_left_y < 0):
		bottom_right_y = bottom_right_y - top_left_y
		top_left_y = 0

	if (bottom_right_x > img.shape[1]):
		top_left_x = top_left_x - (bottom_right_x - img.shape[1])
		bottom_right_x = img.shape[1]
	if (bottom_right_y > img.shape[0]):
		top_left_y = top_left_y - (bottom_right_y - img.shape[0])
		bottom_right_y = img.shape[0]


	# Fetting ROI (Region of Interest)
	roi = img[top_left_y:bottom_right_y, top_left_x:bottom_right_x,:]

	# Take width and height of ROI
	width1 = (roi.shape[1])-1
	height1 = (roi.shape[0])-1

	# Take width and height of Original Image
	width2 = img.shape[1]
	height2 = img.shape[0]

	# Calculate Width Ratio and Height Ratio 
	width_ratio = float(width1)/float(width2)
	height_ratio = float(height1)/float(height2)

	# Count to keep track of number of elements stored in the array
	count=0

	# Initialize new image's list
	new=[]

	# Bilinear interpolation for 3 channels (B,G,R) of the image
	for i in range((height2)):
		for j in range((width2)):
			x = int(width_ratio*j)
			y = int(height_ratio*i)
			x_diff = (width_ratio*j) - x
			y_diff = (height_ratio*i) - y

			# The neighbouring co-ordinates are compared
			# Checking extreme coordinates
			if (x>=(width1-1) or y>=(height1-1)):
				A_blue = roi[y][x][0]
				A_red = roi[y][x][1]
				A_green = roi[y][x][2]
			else:
				A_blue = roi[y][x][0]
				A_red = roi[y][x][1]
				A_green = roi[y][x][2]

			if ((x+1)>=(width1-1) or (y>=(height1-1))):
				B_blue = roi[y][x][0]
				B_red = roi[y][x][1]
				B_blue = roi[y][x][2]
			else:
				B_blue = roi[y+1][x][0] & 0xff
				B_red = roi[y+1][x][1]
				B_green = roi[y+1][x][2]
			if (x>=(width1-1) or ((y+1)>=(height1-1))):
				C_blue = roi[y][x][0]
				C_red = roi[y][x][1]
				C_green = roi[y][x][2]
			else:
				C_blue = roi[y][x+1][0] & 0xff
				C_red = roi[y][x+1][1]
				C_green = roi[y][x+1][2]
			if ((x+1)>=(width1-1) or (y+1)>=(height1-1)):
				D_blue = roi[y][x][0] & 0xff
				D_red = roi[y][x][1]
				D_green = roi[y][x][2]
			else:
				D_blue = roi[y+1][x+1][0] & 0xff
				D_red = roi[y+1][x+1][1]
				D_green = roi[y+1][x+1][2]

			# Combining all the different channels into overall 3 channels
			newimg_blue = (int) ( (A_blue * (1 - x_diff) * (1 - y_diff)) + (B_blue * (x_diff) * (1 - y_diff)) + (C_blue * (y_diff)*(1 - x_diff)) + (D_blue * (x_diff*y_diff)))
			newimg_red = (int) ( (A_red * (1 - x_diff) * (1 - y_diff)) + (B_red * (x_diff) * (1 - y_diff)) + (C_red * (y_diff)*(1 - x_diff)) + (D_red * (x_diff*y_diff)))
			newimg_green = (int) ( (A_green * (1 - x_diff) * (1 - y_diff)) + (B_green * (x_diff) * (1 - y_diff)) + (C_green * (y_diff)*(1 - x_diff)) + (D_green * (x_diff*y_diff)))				

			# Adding the values into the array
			newrow=int(count/(width2))
			newcol=count%(width2)
			newimg = [newimg_blue,newimg_red,newimg_green]
			if(newcol == 0):
				new.append([])
			new[newrow].append(newimg)
			count+=1

	final_img = np.uint8(new)

	# Return Final image
	return final_img

if __name__=="__main__":
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", help="Path to input image", required=True)
        ap.add_argument("-p", "--pivot-point", help="Pivot point coordinates x, y separated by comma (,)", required=True)
        ap.add_argument("-s", "--scale", help="Scale to zoom", type=int, required=True)
        args = vars(ap.parse_args())

        path = args["image"]
        x, y = map(int, args["pivot_point"].split(","))
        scale = args["scale"]
        image = cv2.imread(path)
        image = image.tolist()

        print('Zooming, Cropping, Writing in progress!!')
        final_img = zoom(path, x, y, scale)
        cv2.imwrite("zoomed_image.png", final_img)







        
