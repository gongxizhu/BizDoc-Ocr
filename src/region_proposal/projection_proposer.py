import cv2
import numpy as np
import os


class RegionProposer():
    def __init__(self):
        pass


    def get_test_regions(self, image):
        block_coordinates = []
        gray = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
        retval, binary_gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        text_contours = self.read_text_contours(binary_gray, image)
        for contour in text_contours:
            row_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 1))
            deskew_contour = self.deskew(contour)
            dilated_contour = cv2.dilate(deskew_contour, row_kernel, iterations=1)
            rows = self.read_rows(dilated_contour)
            for row_coord in rows:
                block_coord_list = self.read_blocks(dilated_contour, row_coord)
                block_coordinates.extend(block_coord_list)

        return block_coordinates


    def read_rows(self, contour):
        rows = []
        inLine = False
        start = 0
        count_blank = 0
        height, width = contour.shape[:2]
        projections = np.zeros((height), np.uint8)
        for y in range(0, height):
            for x in range(0, width):
                if contour[y, x] == 255:
                    projections[y] += 1
        #print(projections[:1000])
        #print(np.sum(projections))
        for i in range(0, height):
            if (not inLine and projections[i] > 5):
                inLine = True
                start = i
                count_blank = 0
            elif (count_blank > 0 and projections[i] < 80 and inLine):
                count_blank = 0
                # if (i - start > 3):
                #     rows.append((0, start - 1, width, i - start + 2))
                if (width * (i - start + 2) > width * 20): # remove rect less than 2500
                    rows.append((0, start - 1, width, i - start + 2))
                    inLine = False
            elif (projections[i] < 80):
                count_blank += 1
            elif (i == height - 1 and inLine):
                inLine = False
                if (width * (i - start + 2) > width * 8):  # remove rect less than 2500
                    rows.append((0, start - 1, width, i - start + 2))

        return rows


    def read_blocks(self, contour, row_coordinates):
        blocks = []
        inBlock = False
        start = 0
        count_blank = 0
        height, width = contour.shape[:2]
        projections = np.zeros((width), np.uint8)
        x, y, w, h = row_coordinates
        for xi in range(x, x + w):
            for yi in range(y, y + h):
                if contour[yi, xi] == 255:
                    projections[xi] += 1
        # print(projections)
        for i in range(0, w):
            if (not inBlock and projections[i] > 10):
                inBlock = True
                start = i
                count_blank = 0
            elif (count_blank > 3 and projections[i] < 10 and inBlock):
                inBlock = False
                count_blank = 0
                blocks.append((start - 1, y, i - start + 2, h))
            elif (i == w - 1 and inBlock):
                inBlock = False
                if (i - start > 5):
                    blocks.append((start - 1, y, i - start + 2, h))
            elif (projections[i] < 10):
                count_blank += 1

        return blocks


    def read_text_contours(self, binary_gray, origin_image):
        text_contours = []
        contours_coordinates = []
        # open op to filter the noise
        row_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        row_erosion = cv2.erode(binary_gray, row_kernel, iterations=1)
        row_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 2))
        row_result = cv2.dilate(row_erosion, row_kernel, iterations=1)

        col_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 20))
        col_erosion = cv2.erode(binary_gray, col_kernel, iterations=1)
        col_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 20))
        col_result = cv2.dilate(col_erosion, col_kernel, iterations=1)

        filtered_img = row_result + col_result
        # new_filtered_img = cv2.resize(filtered_img, (800, 600), interpolation=cv2.INTER_CUBIC)
        # while True:
        #     cv2.imshow('test', new_filtered_img)
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        _, contours, _ = cv2.findContours(filtered_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for i in range(0, len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            #cv2.rectangle(origin_image, (x, y), (x + w, y + h), (0, 0, 255), 3)
            area = (w - 8) * (h - 4)
            if (area > 200000 and area < 1000000 and w > 20):
                #print(area)
                #cv2.rectangle(origin_image, (x, y), (x + w, y + h), (0, 0, 255), 3)
                contours_coordinates.append((x, y, w, h))
        # origin_image_new = cv2.resize(origin_image, (800, 600),interpolation=cv2.INTER_CUBIC)
        # while True:
        #     cv2.imshow('test', origin_image_new)
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        contours_coordinates = sorted(contours_coordinates, key=lambda x: x[0])
        contours_coordinates = sorted(contours_coordinates, key=lambda x: x[1])

        for (x, y, w, h) in contours_coordinates:
            cropped_img = origin_image[y + 5:y + h - 10, x + 10:x + w - 20]
            text_contours.append(cropped_img)

        return text_contours


    def _remove_duplicates(self, lines):
        # remove duplicate lines (lines within 10 pixels of eachother)
        ret_lines = []
        for x1, y1, x2, y2 in lines:
            for index, (x3, y3, x4, y4) in enumerate(lines):
                if y1 == y2 and y3 == y4:
                    diff = abs(y1 - y3)
                elif x1 == x2 and x3 == x4:
                    diff = abs(x1 - x3)
                else:
                    diff = 0
                if diff < 10 and diff is not 0:
                    # del lines[index]
                    continue
                ret_lines.append([x1, y1, x2, y2])
        return lines


    def deskew(self, image):
        row_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (300, 5))
        gray = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
        retval, binary_img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        row_dilated = cv2.dilate(binary_img, row_kernel, iterations=1)
        image_canny = cv2.Canny(row_dilated, 5, 15)
        lines = cv2.HoughLines(image_canny, 1, np.pi / 180, 100, 5, 10000)
        if not lines is None:
            lines = np.squeeze(lines)
            sum_angle = 0.0
            count_angle = 0
            for line in lines:
                rho = line[0]
                theta = line[1]
                # print(theta)
                if not ((theta < (np.pi / 4.)) or (theta > (3. * np.pi / 4.0))): # horizontal
                    pt1 = (0, int(rho / np.sin(theta)))
                    pt2 = (image.shape[1], int((rho - image.shape[1] * np.cos(theta)) / np.sin(theta)))
                    #cv2.line(image, pt1, pt2, (255), 1)
                    count_angle += 1
                    sum_angle += theta
            angle = sum_angle / count_angle
            angle = angle / np.pi * 180 - 90
            #print(angle)
            image = self._rotate_image(image, angle)

        return image

    def _rotate_image(self, image, angle):
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        return rotated