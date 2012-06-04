#!/usr/bin/python

from SimpleCV import *

img1 = Image("../sampleimages/stereo_view1.png")
img2 = Image("../sampleimages/stereo_view2.png")

cam = StereoCamera()
H, matched_pts1, matched_pts2 = cam.findHomography(img1, img2)

mapper = StereoMapper()
resultImg = img1.sideBySide(img2)

# # draw the matchings for debugging
# for pt1, pt2 in zip(matched_pts1, matched_pts2):
#   pt2[0] += img1.width
#   c = Color().getRandom()
#   resultImg.drawLine(pt1, pt2, color=c)
#   resultImg.drawCircle(pt1, 5, color=c)
#   resultImg.drawCircle(pt2, 5, color=c)    


# generate random 200 points in image 1
rand_X = np.random.rand(200) * img1.width
rand_Y = np.random.rand(200) * img1.height

for x, y in zip(rand_X, rand_Y):
    c = Color().getRandom()

    # draw the random point in image 1 
    resultImg.drawCircle((x, y), 3, color=c)

    # draw the corresponding point in image 2
    corres_pt = mapper.projectPoint((x, y), 1, H)
    resultImg.drawCircle((img1.width + corres_pt[0], corres_pt[1]), 3, color=c)
resultImg.save('project_point_example.png')
