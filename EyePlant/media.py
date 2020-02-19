import config
import pygame
from PIL import Image


# 加载图片
image_frame = Image.open("image/frame.png").convert('RGBA')
image_frame = image_frame.resize((640, 480), Image.ANTIALIAS)
image_sun = Image.open("image/sun.png").convert('RGBA')
image_sun = image_sun.resize((40, 40), Image.ANTIALIAS)
image_bomb = Image.open("image/bomb.png").convert('RGBA')
image_bomb = image_bomb.resize((40, 40), Image.ANTIALIAS)
image_heart = Image.open("image/heart.png").convert('RGBA')
image_heart = image_heart.resize((40, 40), Image.ANTIALIAS)
image_success = Image.open("image/success.png").convert('RGBA')
# image_success = image_success.resize((40,40),Image.ANTIALIAS)
image_failure = Image.open("image/failure.png").convert('RGBA')
# image_failure  = image_failure.resize((40,40),Image.ANTIALIAS)
image_eye = Image.open("image/eye.png").convert('RGBA')
image_eye = image_eye.resize((10, 10), Image.ANTIALIAS)
img_list = [image_sun, image_bomb, image_heart, image_frame, image_success,
            image_failure, image_eye]

# 加载音乐
pygame.mixer.init()
sun_sound = pygame.mixer.Sound('sound/water.wav')
bomb_sound = pygame.mixer.Sound('sound/bomb.wav')
heart_sound = pygame.mixer.Sound('sound/heart.ogg')
victory_sound = pygame.mixer.Sound('sound/victory.wav')
failure_sound = pygame.mixer.Sound('sound/failure.ogg')
# forge_sound = pygame.mixer.Sound('sound/forge.ogg')
# 音效列表
sound_list = [sun_sound, bomb_sound, heart_sound]


# 贴图
def paste(image, g_manager, pos, type_num):
    if type_num != -1:
        attach_image = img_list[type_num]
    else:
        attach_image = Image.open("image/tree%dimg/tree%d.png" % (g_manager.level, g_manager.idx)).convert('RGBA')
        attach_image = attach_image.resize((int(attach_image.size[0] / 2), int(attach_image.size[1] / 2)),
                                           Image.ANTIALIAS)
        pos = config.POS_LIST[g_manager.level]

    r, g, b, a = attach_image.split()
    image.paste(attach_image, pos, mask=a)
    return image


# 播放背景音乐
def main_theme():
    # 加载文件
    pygame.mixer.music.load('sound/school.mp3')
    # 播放
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.5)


def stop_theme():
    pygame.mixer.music.stop()
