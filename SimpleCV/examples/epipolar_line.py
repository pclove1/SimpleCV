#!/usr/bin/python

from SimpleCV import *

img1 = Image("../sampleimages/stereo_view1.png")
img2 = Image("../sampleimages/stereo_view2.png")

cam = StereoCamera()
F, matched_pts1, matched_pts2 = cam.findFundamentalMat(img1, img2)

mapper = StereoMapper()
resultImg = img1.sideBySide(img2)
eps = np.spacing(1)

# # draw the matchings for debugging
# for pt1, pt2 in zip(matched_pts1, matched_pts2):
#   pt2[0] += img1.width
#   c = Color().getRandom()
#   resultImg.drawLine(pt1, pt2, color=c)
#   resultImg.drawCircle(pt1, 5, color=c)
#   resultImg.drawCircle(pt2, 5, color=c)    

for pt1, pt2 in zip(matched_pts1, matched_pts2):
    c1 = Color().getRandom() # in img1
    c2 = Color().getRandom() # in img2

    # draw the epipolar lines in img1 and its corresponding point in img2
    line1 = mapper.eline(pt2, 2, F)
    resultImg.drawCircle((img1.width + pt2[0], pt2[1]), 3, color=c2)
    
    if abs(line1[0]) < eps: # horizontal line
        y = line1[2]/line1[1]
        resultImg.drawLine((0, y), (img1.width-1, y), color=c)
    elif abs(line1[1]) < eps: # vertical line
        x = line1[2]/line1[0]
        resultImg.drawLine1((x, 0), (x, img1.height-1), color=c)
    else:
        resultImg.drawLine((0, -line1[2]/line1[1]), 
                           (img1.width-1, -(line1[2]+line1[0]*(img1.width-1))/line1[1]), 
                           color=c1)

    # draw the epipolar lines in img2 and its corresponding point in img1
    line2 = mapper.eline(pt1, 1, F)
    resultImg.drawCircle(pt1, 3, color=c1)
    
    if abs(line2[0]) < eps: # horizontal line
        y = line2[2]/line2[1]
        resultImg.drawLine((img1.width, y), (img1.width + img2.width - 1, y), color=c)
    elif abs(line2[1]) < eps: # vertical line
        x = line2[2]/line2[0]
        resultImg.drawLine((img1.width + x, 0), (img1.width + x, img1.height-1), color=c)
    else:
        resultImg.drawLine((img1.width, -line2[2]/line2[1]), 
                           (img1.width+img2.width-1, -(line2[2]+line2[0]*(img2.width-1))/line2[1]), 
                           color=c2)
resultImg.save('epipolar_line_example.png')
