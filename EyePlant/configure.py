import numpy as np
import cv2
import time
import dlib
from PIL import Image
import math
import pygame
import threading
import random
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys


#关卡数
LEVEL_NUM = 4

#窗口名称
WIN_NAME = 'EyePlant'

#产生物体的时间间隔
TIME_INTERVAL_LIST = [1,1,0.5,0.5]

#物体y坐标的上下限
BOTTOM_LINE = 400
UP_LINE = 50

#速度表
SPEED_LIST = [6,7,8,9]

#物体出现概率表
RATE_LIST = [[60,35,5],[40,56,4],[30,67,3],[20,78,2]]

#通关需要的阳光个数
MAX_SUN = 10

#物体半径
RADIUS = 20

#初始生命
LIFE_NUMBER = 3

#植物动画索引
IDX_LIST = [[990,1178],[1970,2108],[374,491],[4974,5110]]

#植物粘贴位置
POS_LIST = [(208,40),(230,75),(220,60),(210,40)]