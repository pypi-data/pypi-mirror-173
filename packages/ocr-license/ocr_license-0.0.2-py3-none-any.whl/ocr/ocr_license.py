import cv2
from paddleocr import PaddleOCR

class OcrLicense:
    def __init__(self) -> None:
        self.paddleocr = PaddleOCR(use_angle_cls="False", lang="japan", show_log=False)
        
    def containsNumber(self, str):
        for character in str:
            if character.isdigit():
                return True
        return False

    def convert_full_width(self, s):
        '''
        Convert all ASCII characters to the full-width counterpart.
        '''
        HALF2FULL = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
        HALF2FULL[0x20] = 0x3000
        return str(s).translate(HALF2FULL)
    
    def inference_single(self, img_path, license_type):
        output = {"name":"", "address":""}
        img = cv2.imread(img_path)
        _, w, _ = img.shape
        result = self.paddleocr.ocr(img, det=True, cls=False)

        if license_type == "driver_license":
            result = result[-1]
            for i in range(len(result)):
                ocr_res = result[i][1][0]
                box = result[i][0]
                if ("氏名" in ocr_res or "氏" in ocr_res or "名" in ocr_res) and (len(ocr_res) == 2):
                    for j in range(len(result)):
                        if i == j:
                            continue
                        mid_point = (box[0][1] + box[3][1]) / 2
                        if (
                            mid_point > result[j][0][1][1]
                            and mid_point < result[j][0][2][1]
                            and not self.containsNumber(result[j][1][0])
                        ):
                            output["name"] += self.convert_full_width(result[j][1][0])

                if ("住所" in ocr_res or "住" in ocr_res or "所" in ocr_res) and (len(ocr_res) == 2):
                    for j in range(len(result)):
                        if i == j:
                            continue
                        mid_point = (box[0][1] + box[3][1]) / 2
                        if (
                            mid_point > result[j][0][1][1]
                            and mid_point < result[j][0][2][1]
                        ):
                            output["address"] += self.convert_full_width(result[j][1][0])
                if output["name"] != "" and output["address"] != "":
                    break

        if license_type == "my_number_card":
            result = result[-1]
            for i in range(len(result)):
                ocr_res = result[i][1][0]
                box = result[i][0]
                if ("氏名" in ocr_res or "氏" in ocr_res or "名" in ocr_res) and (len(ocr_res) == 2):
                    for j in range(len(result)):
                        if i == j:
                            continue
                        mid_point = (box[0][1] + box[3][1]) / 2
                        if (
                            mid_point > result[j][0][1][1]
                            and mid_point < result[j][0][2][1]
                        ):
                            output["name"] += self.convert_full_width(result[j][1][0])

                if ("住所" in ocr_res or "住" in ocr_res or "所" in ocr_res) and (len(ocr_res) == 2):
                    for j in range(len(result)):
                        if i == j:
                            continue
                        mid_point = (box[0][1] + box[3][1]) / 2
                        if (
                            mid_point > result[j][0][1][1] 
                            and mid_point < result[j][0][2][1] 
                            and result[j][0][0][0] < int(w-w/6)
                        ):
                            output["address"] += self.convert_full_width(result[j][1][0])
                if output["name"] != "" and output["address"] != "":
                    break

        return output

