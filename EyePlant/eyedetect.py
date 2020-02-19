import cv2
import dlib
import numpy as np


class EyeDetector:

    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('dlib/shape_predictor_68_face_landmarks.dat')

    def detect(self, img):
        # 取灰度
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # 人脸数rects
        rects = self.detector(img_gray, 0)
        eyes_list = []
        for i in range(len(rects)):
            landmarks = np.matrix([[p.x, p.y] for p in self.predictor(img, rects[i]).parts()])

            # 计算眼睛中心的位置
            left_pos = (int(sum(landmarks[36:42][:, 0]) / 6), int(sum(landmarks[36:42][:, 1]) / 6))
            right_pos = (int(sum(landmarks[42:48][:, 0]) / 6), int(sum(landmarks[42:48][:, 1]) / 6))
            # 标识眼部
            # cv2.circle(img, left_pos, 5, color=(0, 0, 255))
            # cv2.circle(img, right_pos, 5, color=(0, 0, 255))

            # 加入列表
            eyes_list.append(left_pos)
            eyes_list.append(right_pos)

        # 返回处理后的图片和两眼的中心位置坐标
        return img, eyes_list
