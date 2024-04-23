import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np

# Global variables
drawing = False  # True if mouse is pressed

# Mouse callback function
def draw_mask(event, x, y, flags, param):
    global drawing, mask, image

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        cv2.circle(mask, (x, y), 5, (255, 255, 255), -1)
        cv2.circle(image, (x, y), 5, (255, 255, 255), -1)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.circle(mask, (x, y), 5, (255, 255, 255), -1)
            cv2.circle(image, (x, y), 5, (255, 255, 255), -1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(mask, (x, y), 5, (255, 255, 255), -1)
        cv2.circle(image, (x, y), 5, (255, 255, 255), -1)

# Main progran start
# Create a Tkinter window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Open a file dialog box to select an image file
file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])

# Read the selected image file using OpenCV
image1 = cv2.imread(file_path)
#image1 = cv2.imread('abraham.jpg')
#Make a copy of the original image to draw the mask
image = image1.copy()
# Create a mask(BW) base image from original image
mask = np.zeros_like(image)
cv2.namedWindow('Draw Mask')
cv2.setMouseCallback('Draw Mask', draw_mask)

while True:
    cv2.imshow('Draw Mask', image)
    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # Press 'Esc' to exit
        cv2.destroyAllWindows()
        break

# Convert the mask to grayscale
mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
# Restore the image in the mask areas based on the adjacent pixels
restoredImage = cv2.inpaint(image1 , mask_gray , 3, cv2.INPAINT_TELEA)

cv2.imshow("Original",image1)
cv2.imshow("Mask Img",mask)
cv2.imshow("Restored Image", restoredImage) 
cv2.waitKey(0)

cv2.destroyAllWindows()

