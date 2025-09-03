import cv2
import numpy as np

def get_color(b, g, r):
    colors = {
        'Red':    (0, 0, 255),
        'Green':  (0, 255, 0),
        'Blue':   (255, 0, 0),
        'Yellow': (0, 255, 255),
        'Black':  (0, 0, 0),
        'White':  (255, 255, 255),
        'Gray':   (128, 128, 128),
    }
    min_dist = 9999
    for name, (cb, cg, cr) in colors.items():
        dist = ((b-cb)**2 + (g-cg)**2 + (r-cr)**2) ** 0.5
        if dist < min_dist:
            min_dist = dist
            color = name
    return color

img = cv2.imread('test.jpg')
img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, threshold = cv2.threshold(img_g, 234, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

black = (0, 0, 0)
font = cv2.FONT_HERSHEY_COMPLEX

for i, contour in enumerate(contours):
    if i == 0:
        continue

    approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
    cv2.drawContours(img, [contour], 0, black, 3)

    x, y, w, h = cv2.boundingRect(approx)
    ratio = w / float(h)


    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.drawContours(mask, [contour], -1, 255, -1)

    # get mean BGR color inside contour
    mean_color = cv2.mean(img, mask=mask)
    b, g, r = mean_color[:3]

    color = get_color(b, g, r)


    sides = len(approx)
    if sides == 3:
        shape = 'Triangle'
    elif sides == 4:
        if 0.95 <= ratio <= 1.05:
            shape = 'Square'
        else:
            shape = 'Rectangle'
        
    elif sides == 5:
        shape = 'Pentagon'
    else:
        shape = 'Circle'
    cv2.putText(img, f"a {color} {shape}", (x,y - 10), font, 0.8, black, 2)


resized = cv2.resize(img, (1000, 600))
cv2.imshow('Shapes', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
