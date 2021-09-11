import cv2
img = cv2.imread('capture_image_40.jpg', 0)
img2 = cv2.imread('capture_image_155.jpg', 0)
cv2.imwrite('huidu1.jpg', img)
cv2.imwrite('huidu2.jpg', img2)