import cv2, numpy as np

filepath = ''

im = cv2.imread(filepath)
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, im_inv = cv2.threshold(im_gray,127,255,cv2.THRESH_BINARY_INV)
kernel = 1/16*np.array([[1,2,1], [2,4,2], [1,2,1]])
im_blur = cv2.filter2D(im_inv,-1,kernel)
ret, im_res = cv2.threshold(im_blur,127,255,cv2.THRESH_BINARY)
im2, contours, hierarchy = cv2.findContours(im_res, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
result = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w == w_max and w_max >= w_min * 2:# 如果两个轮廓一个是另一个的宽度的2倍以上，我们认为这个轮廓就是包含3个字符的轮廓
        box_left = np.int0([[x,y], [x+w/3,y], [x+w/3,y+h], [x,y+h]])
        box_mid = np.int0([[x+w/3,y], [x+w*2/3,y], [x+w*2/3,y+h], [x+w/3,y+h]])
        box_right = np.int0([[x+w*2/3,y], [x+w,y], [x+w,y+h], [x+w*2/3,y+h]])
        result.append(box_left)
        result.append(box_mid)
        result.append(box_right)
    elif w_max < w_min * 2:
        # 如果两个轮廓，较宽的宽度小于较窄的2倍，我们认为这是两个包含2个字符的轮廓
        box_left = np.int0([[x,y], [x+w/2,y], [x+w/2,y+h], [x,y+h]])
        box_right = np.int0([[x+w/2,y], [x+w,y], [x+w,y+h], [x+w/2,y+h]])
        result.append(box_left)
        result.append(box_right)
    else:
        box = np.int0([[x,y], [x+w,y], [x+w,y+h], [x,y+h]])
        result.append(box)