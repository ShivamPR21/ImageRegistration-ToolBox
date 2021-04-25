import os

import cv2 as cv
import imutils
import numpy as np
import matplotlib.pyplot as plt


def align_images(image, template, maxFeatures=500, keepPercent=0.2,
                 matching_method=cv.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING,
                 feature_method='orb'):

    cache_path = 'static/uploads/cache/'

    # convert both the input image and template to grayscale
    imageGray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    templateGray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

    # use ORB to detect keypoints and extract (binary) local
    # invariant features
    kpsA, kpsB = None, None
    descsA, descsB = None, None
    if feature_method == 'orb':
        orb = cv.ORB_create(maxFeatures)
        (kpsA, descsA) = orb.detectAndCompute(imageGray, None)
        (kpsB, descsB) = orb.detectAndCompute(templateGray, None)
    elif feature_method == 'sift':
        sift = cv.SIFT_create(maxFeatures)
        (kpsA, descsA) = sift.detectAndCompute(imageGray, None)
        (kpsB, descsB) = sift.detectAndCompute(templateGray, None)
    elif feature_method == 'surf':
        surf = cv.xfeatures2d.SURF_create(maxFeatures)
        (kpsA, descsA) = surf.detectAndCompute(imageGray, None)
        (kpsB, descsB) = surf.detectAndCompute(templateGray, None)
    elif feature_method == 'brief':
        star = cv.xfeatures2d.StarDetector_create()
        brief = cv.xfeatures2d.BriefDescriptorExtractor_create()

        # find the keypoints with STAR
        kpsA = star.detect(imageGray, None)
        # compute the descriptors with BRIEF
        kpsA, descsA = brief.compute(imageGray, kpsA)

        # find the keypoints with STAR
        kpsB = star.detect(templateGray, None)
        # compute the descriptors with BRIEF
        kpsB, descsB = brief.compute(templateGray, kpsB)

    # match the features
    # method = cv.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
    matcher = cv.DescriptorMatcher_create(matching_method)
    matches = matcher.match(descsA, descsB, None)

    # sort the matches by their distance (the smaller the distance,
    # the "more similar" the features are)
    matches = sorted(matches, key=lambda x: x.distance)
    # keep only the top matches
    keep = int(len(matches) * keepPercent)
    matches = matches[:keep]
    # check to see if we should visualize the matched keypoints
    # if debug:

    matchedVis = cv.drawMatches(image, kpsA, template, kpsB, matches, None)
    matchedVis = imutils.resize(matchedVis, width=1000)
    cv.imwrite(os.path.join(cache_path, 'feature.png'), matchedVis)

    # allocate memory for the keypoints (x, y)-coordinates from the
    # top matches -- we'll use these coordinates to compute our
    # homography matrix
    ptsA = np.zeros((len(matches), 2), dtype="float")
    ptsB = np.zeros((len(matches), 2), dtype="float")
    # loop over the top matches
    for (i, m) in enumerate(matches):
        # indicate that the two keypoints in the respective images
        # map to each other
        ptsA[i] = kpsA[m.queryIdx].pt
        ptsB[i] = kpsB[m.trainIdx].pt

    # compute the homography matrix between the two sets of matched
    # points
    (H, mask) = cv.findHomography(ptsA, ptsB, method=cv.RANSAC)
    # use the homography matrix to align the images
    (h, w) = template.shape[:2]
    aligned = cv.warpPerspective(image, H, (w, h))
    # return the aligned image

    cv.imwrite(os.path.join(cache_path, 'final.png'), aligned)
    return aligned


if __name__ == '__main__':
    image = cv.imread('../static/uploads/cache/2.jpeg')
    tmplate = cv.imread('../static/uploads/cache/1.jpeg')

    aligned = align_images(image, tmplate, debug=True,
                           matching_method=cv.DESCRIPTOR_MATCHER_BRUTEFORCE_SL2,
                           feature_method='brief')

    cv.imwrite('../static/uploads/cache/final.jpeg', aligned)

    print('Done')
