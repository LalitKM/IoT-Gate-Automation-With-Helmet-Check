import cv2
import label_image

size = 4

im = cv2.imread("testimage.jpg")
im=cv2.flip(im,1,0) #Flip to act as a mirror
mini = cv2.resize(im, (int(im.shape[1]/size), int(im.shape[0]/size)))
FaceFileName = "testimage.jpg"
text = label_image.main(FaceFileName)
text = text.title()
font = cv2.FONT_HERSHEY_TRIPLEX
cv2.putText(im, text,(80,100), font, 2, (0,0,255), 2)
# Show the image
cv2.imshow('Capture', im)
key = cv2.waitKey(10)
# if Esc key is press then break out of the loop
if key == 27: #The Esc key
    exit(0)
