import math
import random
import threading
import time

import cv2
import numpy as np
from PIL import Image

import config
import eyedetect
import media


class DropObject:

    def __init__(self, speed, radius, object_type):
        self.speed = speed
        self.radius = radius
        self.x = random.randint(120, 520)
        self.y = config.UP_LINE
        # 'sunshine':0,'bomb':1,'life':2,
        self.object_type = object_type

    # 向下移动speed个单位
    def move(self):
        self.y += self.speed

    # 检测是否与眼睛重合
    def is_collision(self, pos_list):
        for pos in pos_list:
            dis = math.hypot(self.x - pos[0], self.y - pos[1])
            if dis <= self.radius:
                return True
        return False

    # 检测是否触底
    def is_bottom(self):
        return True if self.y > config.BOTTOM_LINE else False


class GameManager:

    def __init__(self):
        self.level = 0
        self.speed = config.SPEED_LIST[self.level]
        self.rate = config.RATE_LIST[self.level]
        self.life = config.LIFE_NUMBER
        self.sunshine = 0
        self.alive_flag = 1
        self.growing_flag = 0
        self.idx = config.IDX_LIST[self.level][0]
        self.end_idx = config.IDX_LIST[self.level][1]
        self.finish_flag = 0

    def catch_object(self, object_type):
        if object_type == 0:
            self.sunshine += 1
            if self.sunshine >= config.MAX_SUN:
                self.growing_flag = 1

        elif object_type == 1:
            self.life -= 1
            if self.life <= 0:
                self.alive_flag = 0
        else:
            self.life += 1

    def upgrade(self, o_manager):
        self.level += 1
        self.speed = config.SPEED_LIST[self.level]
        self.rate = config.RATE_LIST[self.level]
        self.idx = config.IDX_LIST[self.level][0]
        self.end_idx = config.IDX_LIST[self.level][1]
        self.sunshine = 0
        self.growing_flag = 0
        o_manager.clear()


class ObjectManager:

    def __init__(self):
        self.object_list = []

    # 'sunshine':0,'bomb':1,'life':2,
    def create_object(self, g_manager):
        object_type = self.__random_index(g_manager.rate)
        new_object = DropObject(g_manager.speed, config.RADIUS, object_type)
        self.object_list.append(new_object)

    @staticmethod
    def __random_index(rate):
        # 参数rate为list<int>
        # 返回概率事件的下标索引
        start = 0
        index = 0
        randnum = random.randint(1, sum(rate))

        for index, scope in enumerate(rate):
            start += scope
            if randnum <= start:
                break
        return index

    def update_object(self, pos_list):

        # 删除触底物体
        while len(self.object_list) > 0 and self.object_list[0].is_bottom():
            del (self.object_list[0])

        # 处理碰撞物体
        ob_list = []
        new_object_list = []
        for ob in self.object_list:
            if ob.is_collision(pos_list):
                ob_list.append(ob)
            else:
                new_object_list.append(ob)
        self.object_list = new_object_list

        # 所有物体向下移动
        for ob in self.object_list:
            ob.move()

        return ob_list

    def clear(self):
        self.object_list.clear()


class ThreadTask:

    def __init__(self, o_manager):
        self.__running = True
        self.job = o_manager

    def terminate(self):
        self.__running = False

    def run(self, g_manager):
        while self.__running:
            self.job.create_object(g_manager)
            time.sleep(config.TIME_INTERVAL_LIST[g_manager.level])


def run_game():
    # 眼部检测器
    eye_detector = eyedetect.EyeDetector()
    # 游戏管理器
    g_manager = GameManager()
    # 物体管理器
    o_manager = ObjectManager()

    # 打开本地摄像头，设置分辨率
    cap = cv2.VideoCapture(0)
    cap.set(3, config.IMG_RES[0])
    cap.set(4, config.IMG_RES[1])

    # 设定窗口尺寸、位置
    cv2.namedWindow(config.WIN_NAME, 0)
    cv2.moveWindow(config.WIN_NAME, 500, 100)
    cv2.resizeWindow(config.WIN_NAME, 960, 720)

    # 播放背景音乐
    media.main_theme()

    # 大循环，实现关卡
    for i in range(0, config.LEVEL_NUM):

        # 新开一个线程，每秒产生一个新的物体
        object_generator = ThreadTask(o_manager)
        t = threading.Thread(target=object_generator.run, args=(g_manager,))
        t.start()

        while True:
            # 从摄像头中读取画面
            ret, img_color = cap.read()

            # 翻转图片
            img_color = cv2.flip(img_color, 1, dst=None)

            # 得到眼部位置
            img, eyes_list = eye_detector.detect(img_color)

            # 转为RGB图片，方便贴图
            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            # 眼部贴图
            for eye in eyes_list:
                image = media.paste(image, g_manager, (eye[0] - 5, eye[1] - 5), 6)

            # 满足通关条件后将不再触发道具，仅播放生长动画
            if g_manager.growing_flag == 1:
                g_manager.idx += 1
            else:
                # 检测碰撞并更新物体
                ob_list = o_manager.update_object(eyes_list)
                for ob in ob_list:
                    media.sound_list[ob.object_type].play()
                    g_manager.catch_object(ob.object_type)
                # 显示物体图像
                for ob in o_manager.object_list:
                    image = media.paste(image, g_manager, (ob.x - 20, ob.y - 20), ob.object_type)
            # 植物动画
            image = media.paste(image, g_manager, (208, 40), -1)

            # 加入背景图
            image = media.paste(image, g_manager, (0, 0), 3)

            # 转回BGR图片，用以显示
            img = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)

            # 显示生命值和阳光数
            cv2.putText(img, '%d' % g_manager.sunshine, (583, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (52, 83, 114), 1)
            cv2.putText(img, '%d' % g_manager.life, (583, 33), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
            cv2.putText(img, 'Level %d' % (i + 1), (250, 33), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)

            # 显示最终图片
            cv2.imshow('EyePlant', img)

            # 生长动画播放完毕，进入下一关
            if g_manager.idx == g_manager.end_idx:
                image = media.paste(image, g_manager, (230, 180), 4)
                img = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
                cv2.putText(img, '0', (583, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (52, 83, 114), 1)
                cv2.putText(img, '%d' % g_manager.life, (583, 33), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
                cv2.putText(img, 'Level %d' % (i + 1), (250, 33), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
                cv2.imshow(config.WIN_NAME, img)
                # forge_sound.play()
                media.victory_sound.play()
                cv2.waitKey(3500)
                break

            # 生命值为零,退出
            if g_manager.alive_flag == 0:
                g_manager.finish_flag = 1
                image = media.paste(image, g_manager, (230, 180), 5)
                img = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
                cv2.putText(img, '%d' % g_manager.sunshine, (583, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (52, 83, 114), 1)
                cv2.putText(img, '%d' % g_manager.life, (583, 33), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
                cv2.putText(img, 'Level %d' % (i + 1), (250, 33), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
                cv2.imshow(config.WIN_NAME, img)
                # forge_sound.play()
                media.failure_sound.play()
                cv2.waitKey(5500)
                break

            # 如果按下键盘上的ESC就关闭窗口
            if cv2.waitKey(1) & 0xFF == 27:
                g_manager.finish_flag = 1
                break

        # 中断线程
        object_generator.terminate()

        # 失败或通关则游戏结束,否则进入下一关
        if g_manager.finish_flag == 1 or g_manager.level == 3:
            break
        else:
            g_manager.upgrade(o_manager)

    # 停止播放背景音乐
    media.stop_theme()

    # 释放摄像头资源
    cap.release()
    # 关闭窗口
    cv2.destroyAllWindows()
    # 返回值给用户窗口
    return g_manager.finish_flag
