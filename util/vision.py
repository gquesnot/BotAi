import cv2
import numpy as np

from util.hswfilter import HsvFilter


class Vision:
    # constants
    TRACKBAR_WINDOW = "Trackbars"

    # properties
    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None

    # constructor
    def __init__(self, hsv=True,method=cv2.TM_CCOEFF_NORMED):
        self.hsv_filter = HsvFilter()
        # load the image we're trying to match
        # https://docs.opencv2.org/4.2.0/d4/da8/group__imgcodecs.html

        # Save the dimensions of the needle image
        #self.needle_w = self.needle_img.shape[1]
        #self.needle_h = self.needle_img.shape[0]
        self.hsv = hsv
        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method

    def find(self, haystack_img, threshold=0.5, max_results=10):
        # run the OpenCV2 algorithm
        result = cv2.matchTemplate(haystack_img, self.needle_img, self.method)

        # Get the all the positions from the match result that exceed our threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        #print(locations)

        # if we found no results, return now. this reshape of the empty array allows us to
        # concatenate together results without causing an error
        if not locations:
            return np.array([], dtype=np.int32).reshape(0, 4)

        # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
        # locations by using groupRectangles().
        # First we need to create the list of [x, y, w, h] rectangles
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
        # Apply group rectangles.
        # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
        # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
        # in the result. I've set eps to 0.5, which is:
        # "Relative difference between sides of the rectangles to merge them into a group."
        rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        #print(rectangles)

        # for performance reasons, return a limited number of results.
        # these aren't necessarily the best results.
        if len(rectangles) > max_results:
            print('Warning: too many results, raise the threshold.')
            rectangles = rectangles[:max_results]

        return rectangles

    # given a list of [x, y, w, h] rectangles returned by find(), convert those into a list of
    # [x, y] positions in the center of those rectangles where we can click on those found items
    def get_click_points(self, rectangles):
        points = []

        # Loop over all the rectangles
        for (x, y, w, h) in rectangles:
            # Determine the center position
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            # Save the points
            points.append((center_x, center_y))

        return points

    # given a list of [x, y, w, h] rectangles and a canvas image to draw on, return an image with
    # all of those rectangles drawn
    def draw_rectangles(self, haystack_img, rectangles):
        # these colors are actually BGR
        line_color = (0, 255, 0)
        line_type = cv2.LINE_4

        for (x, y, w, h) in rectangles:
            # determine the box positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw the box
            cv2.rectangle(haystack_img, top_left, bottom_right, line_color, lineType=line_type)

        return haystack_img

    # given a list of [x, y] positions and a canvas image to draw on, return an image with all
    # of those click points drawn on as crosshairs
    def draw_crosshairs(self, haystack_img, points):
        # these colors are actually BGR
        marker_color = (255, 0, 255)
        marker_type = cv2.MARKER_CROSS

        for (center_x, center_y) in points:
            # draw the center point
            cv2.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)

        return haystack_img

    # create gui window with controls for adjusting arguments in real-time
    def init_control_gui(self):
        cv2.namedWindow(self.TRACKBAR_WINDOW, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)

        # required callback. we'll be using getTrackbarPos() to do lookups
        # instead of using the callback.

        def nothing(position):
            pass
        # create trackbars for bracketing.
        # OpenCV2 scale for HSV is H: 0-179, S: 0-255, V: 0-255


        cv2.createTrackbar('HMin', self.TRACKBAR_WINDOW, self.hsv_filter.hMin, 179, nothing)
        cv2.createTrackbar('SMin', self.TRACKBAR_WINDOW, self.hsv_filter.sMin, 255, nothing)
        cv2.createTrackbar('VMin', self.TRACKBAR_WINDOW, self.hsv_filter.vMin, 255, nothing)
        cv2.createTrackbar('HMax', self.TRACKBAR_WINDOW, self.hsv_filter.hMax, 179, nothing)
        cv2.createTrackbar('SMax', self.TRACKBAR_WINDOW, self.hsv_filter.sMax, 255, nothing)
        cv2.createTrackbar('VMax', self.TRACKBAR_WINDOW, self.hsv_filter.vMax, 255, nothing)


        # trackbars for increasing/decreasing saturation and value
        cv2.createTrackbar('SAdd', self.TRACKBAR_WINDOW, self.hsv_filter.sAdd, 255, nothing)
        cv2.createTrackbar('SSub', self.TRACKBAR_WINDOW, self.hsv_filter.sSub, 255, nothing)
        cv2.createTrackbar('VAdd', self.TRACKBAR_WINDOW, self.hsv_filter.vAdd, 255, nothing)
        cv2.createTrackbar('VSub', self.TRACKBAR_WINDOW, self.hsv_filter.vSub, 255, nothing)
        cv2.createTrackbar('cannyOn', self.TRACKBAR_WINDOW, 0, 1, nothing)
        cv2.createTrackbar('cannyKernel', self.TRACKBAR_WINDOW, 1, 10, nothing)
        cv2.createTrackbar('cannyRatio', self.TRACKBAR_WINDOW, 1, 10, nothing)
        cv2.createTrackbar('LowThreshold', self.TRACKBAR_WINDOW, 1, 200, nothing)
        cv2.createTrackbar('MaxThreshold', self.TRACKBAR_WINDOW, 1, 200, nothing)
        cv2.createTrackbar('BlurOn', self.TRACKBAR_WINDOW, 0, 1, nothing)
        cv2.createTrackbar('BlurKernel', self.TRACKBAR_WINDOW, 1, 200, nothing)

        cv2.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, 179)
        cv2.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, 255)
        cv2.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, 255)
        cv2.setTrackbarPos('LowThreshold', self.TRACKBAR_WINDOW, 1)
        cv2.setTrackbarPos('MaxThreshold', self.TRACKBAR_WINDOW, 100)
        cv2.setTrackbarPos('BlurOn', self.TRACKBAR_WINDOW, 0)
        cv2.setTrackbarPos('BlurKernel', self.TRACKBAR_WINDOW, 3)
        cv2.setTrackbarPos('cannyRatio', self.TRACKBAR_WINDOW, 3)
        cv2.setTrackbarPos('cannyKernel', self.TRACKBAR_WINDOW, 3)



    # returns an HSV filter object based on the control GUI values
    def get_hsv_filter_from_controls(self):

        # Get current positions of all trackbars
        #print(self.hsv_filter.__dict__)
        self.hsv_filter.hMin = cv2.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
        self.hsv_filter.sMin = cv2.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
        self.hsv_filter.vMin = cv2.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
        self.hsv_filter.hMax = cv2.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
        self.hsv_filter.sMax = cv2.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
        self.hsv_filter.vMax = cv2.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
        self.hsv_filter.sAdd = cv2.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
        self.hsv_filter.sSub = cv2.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
        self.hsv_filter.vAdd = cv2.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
        self.hsv_filter.vSub = cv2.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)
        self.hsv_filter.cannyOn = cv2.getTrackbarPos('cannyOn', self.TRACKBAR_WINDOW)
        self.hsv_filter.cannyKernel = cv2.getTrackbarPos('cannyKernel', self.TRACKBAR_WINDOW)
        self.hsv_filter.cannyRatio = cv2.getTrackbarPos('cannyRatio', self.TRACKBAR_WINDOW)

        self.hsv_filter.lowThreshold = cv2.getTrackbarPos('LowThreshold', self.TRACKBAR_WINDOW)
        self.hsv_filter.maxThreshold = cv2.getTrackbarPos('MaxThreshold', self.TRACKBAR_WINDOW)
        self.hsv_filter.blurOn = cv2.getTrackbarPos('BlurOn', self.TRACKBAR_WINDOW)
        self.hsv_filter.blurKernel = cv2.getTrackbarPos('BlurKernel', self.TRACKBAR_WINDOW)

        if self.hsv_filter.blurKernel == 0:
            self.hsv_filter.blurKernel = 1
        if self.hsv_filter.cannyKernel == 0:
            self.hsv_filter.cannyKernel = 1

        return self.hsv_filter

    # given an image and an HSV filter, apply the filter and return the resulting image.
    # if a filter is not supplied, the control GUI trackbars will be used
    def apply_hsv_filter(self, original_image, hsv_filter=None):
        # convert image to HSV
        if self.hsv:
            hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
        else:
            hsv= original_image

        # if we haven't been given a defined filter, use the filter values from the GUI
        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()
        # add/subtract saturation and value
        h, s, v = cv2.split(hsv)
        s = self.shift_channel(s, hsv_filter.sAdd)
        s = self.shift_channel(s, -hsv_filter.sSub)
        v = self.shift_channel(v, hsv_filter.vAdd)
        v = self.shift_channel(v, -hsv_filter.vSub)
        hsv = cv2.merge([h, s, v])

        # Set minimum and maximum HSV values to display
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
        # Apply the thresholds
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(hsv, hsv, mask=mask)

        # convert back to BGR for imshow() to display it properly
        if self.hsv:
            img = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)
        else:
            img = result

        if hsv_filter.cannyOn == 1 and hsv_filter.blurOn == 1:
            srcGray = None
            detected_edges = None
            img = cv2.GaussianBlur(img, (hsv_filter.blurKernel, hsv_filter.blurKernel), 3)
            img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            img = cv2.Canny(img, hsv_filter.lowThreshold, hsv_filter.lowThreshold * hsv_filter.cannyRatio, hsv_filter.cannyKernel)
        elif hsv_filter.cannyOn == 1:
            srcGray = None
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.Canny(img, hsv_filter.lowThreshold,
                                       hsv_filter.lowThreshold * hsv_filter.cannyRatio, hsv_filter.cannyKernel)
        elif hsv_filter.blurOn == 1:

            img = cv2.GaussianBlur(img, (hsv_filter.blurKernel, hsv_filter.blurKernel), 3)

        return img

    # apply adjustments to an HSV channel
    # https://stackoverflow.com/questions/49697363/shifting-hsv-pixel-values-in-python-using-numpy
    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c

    def centeroid(self, point_list):
        point_list = np.asarray(point_list, dtype=np.int32)
        length = point_list.shape[0]
        sum_x = np.sum(point_list[:, 0])
        sum_y = np.sum(point_list[:, 1])
        return [np.floor_divide(sum_x, length), np.floor_divide(sum_y, length)]

