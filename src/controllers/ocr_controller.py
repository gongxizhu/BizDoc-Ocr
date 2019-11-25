from ocr.tesseract_ocr import *
from region_proposal.projection_proposer import *
from region_proposal.pixel_link_proposer import *
import cv2
import xlwt
from PyQt5.QtCore import *


class OCRController:
    __ocr = None
    __region_proposer = None
    __pixel_link_proposer = None
    __signal = pyqtSignal()

    def __init__(self):
        self.__ocr = TesseractOcr()
        self.__region_proposer = RegionProposer()
        self.__pixel_link_proposer = PixelLinkProposer()


    def read_text_to_xls(self, image_path, signal=None):
        block_coordinates = []
        xlsx_path = image_path.replace('.jpg', '.xls', 1)
        print(xlsx_path)
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
        retval, binary_gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        text_contours = self.__region_proposer.read_text_contours(binary_gray, image)
        row_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 2))
        xlsx_book = xlwt.Workbook(encoding='utf-8', style_compression=0)

        for sheet_id, cropped_img in enumerate(text_contours):
            sheet = xlsx_book.add_sheet('result_' + str(sheet_id), cell_overwrite_ok=True)
            deskew_contour = self.__region_proposer.deskew(cropped_img)
            gray_contour = cv2.cvtColor(deskew_contour, cv2.COLOR_RGBA2GRAY)
            retval, cropped_img_binary = cv2.threshold(gray_contour, 127, 255, cv2.THRESH_BINARY_INV)
            # while True:
            #     cv2.imshow('test', dilated_contour)
            #     if cv2.waitKey(1) & 0xFF == ord('q'):
            #         break
            rows = self.__region_proposer.read_rows(cropped_img_binary)
            # print(rows)
            dilated_contour = cv2.dilate(cropped_img_binary, row_kernel, iterations=1)
            for row_id, row_coord in enumerate(rows):
                x, y, w, h = row_coord
                #cv2.rectangle(cropped_img, (x, y), (x + w, y + h), (0, 0, 255), 1)
                block_coord_list = self.__region_proposer.read_blocks(dilated_contour, row_coord)
                text_of_row = ''
                for block_coord in block_coord_list:
                    (x, y, w, h) = block_coord
                    #print(x, y, w, h)
                    if (x < 0): x = 0
                    if (y < 0): y = 0
                    img_to_ocr = cropped_img[y:y + h, x:x + w]
                    text = self.__ocr.read_text(img_to_ocr)
                    text_of_row += text + ' '
                    #cv2.rectangle(cropped_img, (x, y), (x + w, y + h), (0, 0, 255), 1)
                print(text_of_row)
                #signal.emit(text_of_row)
                sheet.write(row_id, 0, text_of_row)
            # cropped_img = cv2.resize(cropped_img, (450, 900), interpolation=cv2.INTER_CUBIC)
            # while True:
            #     cv2.imshow('test', cropped_img)
            #     if cv2.waitKey(1) & 0xFF == ord('q'):
            #         break
        xlsx_book.save(xlsx_path)

    def read_sparse_text(self, image):
        print('Start to detect')
        bboxes = self.__pixel_link_proposer.get_text_regions(image)
        response = ''
        for bbox in bboxes:
            points = np.reshape(bbox, [4, 2])
            cnts = util.img.points_to_contours(points)
            # np.shape(points)
            # print(cnts)
            crop = util.img.get_contour_region_in_rect(image, points)
            text = self.__ocr.read_text(crop)
            util.img.draw_contours(image, contours=cnts, idx=-1, color=util.img.COLOR_BGR_YELLOW, border_width=4)
            response = response + ' ' + text
        cv2.imwrite(r'C:\my_repo\BizDoc-Ocr\test_1_result.jpg', image)
        print('End of detection')
        return response

    def get_detected_image(self, image):
        print('Start to detect')
        bboxes = self.__pixel_link_proposer.get_text_regions(image)
        response = ''
        for bbox in bboxes:
            points = np.reshape(bbox, [4, 2])
            cnts = util.img.points_to_contours(points)
            util.img.draw_contours(image, contours=cnts, idx=-1, color=util.img.COLOR_BGR_YELLOW, border_width=4)
        # cv2.imwrite(r'C:\my_repo\BizDoc-Ocr\test_1_result.jpg', image)
        print('End of detection')
        return image

if __name__ == '__main__':
    controller = OCRController()
    img_path = r'C:\my_repo\BizDoc-Ocr\dataset\img3.jpg'
    controller.read_text_to_xls(img_path)
    mode = cv2.IMREAD_COLOR
    # image = cv2.imread(r'C:\my_repo\BizDoc-Ocr\volvo.jpg', mode)
    #image = cv2.imread(r'C:\my_repo\BizDoc-Ocr\test_1_reverse.jpg', mode)
    #result = controller.read_sparse_text(image)
    #print(result)