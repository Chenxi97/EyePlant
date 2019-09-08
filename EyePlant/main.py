#眼部检测
from eyedetect import *
#游戏控制
from game import *
#媒体文件管理
from media import *
#库和游戏参数
from configure import *
		
		
def run_game():
    
    #眼部检测器
    eye_detector = Eye()
    #游戏管理器
    g_manager = Game_manager()
    #物体管理器
    o_manager = Object_manager()
    #贴图器
    img_dealer = Image_dealer()
    #音乐播放器
    music_player = Music()

    #打开本地摄像头，设置分辨率
    cap=cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    
    #设定窗口尺寸、位置
    cv2.namedWindow(WIN_NAME,0);
    cv2.moveWindow(WIN_NAME,500,100)
    cv2.resizeWindow(WIN_NAME, 960, 720);
    
    
    #播放背景音乐
    music_player.main_theme()
    
    #大循环，实现关卡
    for i in range(0,LEVEL_NUM):
        
        #新开一个线程，每秒产生一个新的物体
        object_generator = Thread_task(o_manager)
        t = threading.Thread(target=object_generator.run,args=(g_manager,))
        t.start()

        while True:
            #从摄像头中读取画面
            ret,img_color=cap.read()

            #翻转图片
            img_color = cv2.flip(img_color,1,dst=None) 

            #得到眼部位置
            img,eyes_list=eye_detector.detect(img_color)

            #转为RGB图片，方便贴图
            image = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
            
            #眼部贴图
            for eye in eyes_list:
                image = img_dealer.paste(image,g_manager,(eye[0]-5,eye[1]-5),6)

            #满足通关条件后将不再触发道具，仅播放生长动画
            if g_manager.growing_flag ==1:
                g_manager.idx+=1
            else:
                #检测碰撞并更新物体
                ob_list = o_manager.update_object(eyes_list)
                for ob in ob_list:
                    music_player.sound_list[ob.object_type].play()
                    g_manager.catch_object(ob.object_type)
                #显示物体图像    
                for ob in o_manager.object_list:
                    image = img_dealer.paste(image,g_manager,(ob.x-20,ob.y-20),ob.object_type)
            #植物动画
            image = img_dealer.paste(image,g_manager,(208,40),-1)

            #加入背景图
            image = img_dealer.paste(image,g_manager,(0,0),3)

            #转回BGR图片，用以显示
            img = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)

            #显示生命值和阳光数
            cv2.putText(img,'%d' % g_manager.sunshine,(583,80),cv2.FONT_HERSHEY_COMPLEX,1,(52,83,114),1)
            cv2.putText(img,'%d' % g_manager.life,(583,33),cv2.FONT_HERSHEY_COMPLEX,1,(0, 0 ,255),1)
            cv2.putText(img,'Level %d' % (i+1),(250,33),cv2.FONT_HERSHEY_COMPLEX,1,(0, 0 ,255),1)

            #显示最终图片 
            cv2.imshow('EyePlant', img)

            #生长动画播放完毕，进入下一关
            if g_manager.idx == g_manager.end_idx:
                image = img_dealer.paste(image,g_manager,(230,180),4)
                img = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)
                cv2.putText(img,'0',(583,80),cv2.FONT_HERSHEY_COMPLEX,1,(52,83,114),1)
                cv2.putText(img,'%d' % g_manager.life,(583,33),cv2.FONT_HERSHEY_COMPLEX,1,(0, 0 ,255),1)
                cv2.putText(img,'Level %d' % (i+1),(250,33),cv2.FONT_HERSHEY_COMPLEX,1,(0, 0 ,255),1)
                cv2.imshow(WIN_NAME, img)
                #forge_sound.play()
                music_player.victory_sound.play()
                cv2.waitKey(3500)
                break

            #生命值为零,退出
            if g_manager.alive_flag == 0:
                g_manager.finish_flag = 1
                image = img_dealer.paste(image,g_manager,(230,180),5)
                img = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)
                cv2.putText(img,'%d' % g_manager.sunshine,(583,80),cv2.FONT_HERSHEY_COMPLEX,1,(52,83,114),1)
                cv2.putText(img,'%d' % g_manager.life,(583,33),cv2.FONT_HERSHEY_COMPLEX,1,(0, 0 ,255),1)
                cv2.putText(img,'Level %d' % (i+1),(250,33),cv2.FONT_HERSHEY_COMPLEX,1,(0, 0 ,255),1)
                cv2.imshow(WIN_NAME, img)
                #forge_sound.play()
                music_player.failure_sound.play()
                cv2.waitKey(5500)
                break

            #如果按下键盘上的ESC就关闭窗口
            if cv2.waitKey(1) & 0xFF==27:
                g_manager.finish_flag = 1
                break

        #中断线程
        object_generator.terminate()
        
        #失败或通关则游戏结束,否则进入下一关
        if g_manager.finish_flag == 1 or g_manager.level==3:
            break;
        else:
            g_manager.upgrade(o_manager)
    
    
    #停止播放背景音乐
    pygame.mixer.music.stop() 
    #释放摄像头资源
    cap.release()
    #关闭窗口
    cv2.destroyAllWindows()
    #返回值
    return g_manager.finish_flag


class mainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 设置GUI窗口的位置和尺寸
        self.setGeometry(510, 140, 960, 720)
        self.setWindowTitle('EyePlant')
        
        #载入背景图片
        window_pale = QPalette() 
        window_pale.setBrush(self.backgroundRole(),QBrush(QPixmap("image/ui/main.png"))) 
        self.setPalette(window_pale)
        
        #应用图标
        self.setWindowIcon(QIcon('image/icon.png'))

        #创建三个按钮
        self.bt1 = QPushButton('',self)
        self.bt1.setGeometry(QRect(575, 280, 211, 67))
        self.bt2 = QPushButton('',self)
        self.bt2.setGeometry(QRect(575, 400, 211, 67))
        self.bt3 = QPushButton('',self)
        self.bt3.setGeometry(QRect(575, 520, 211, 67))
        
        #按钮图像
        self.bt1.setStyleSheet("QPushButton{border-image: url(image/ui/button1.png)}"
                                       "QPushButton:hover{border-image: url(image/ui/button1_1.png)}" 
                                  "QPushButton:pressed{border-image: url(image/ui/button1_2.png)}")
        self.bt2.setStyleSheet("QPushButton{border-image: url(image/ui/button2.png)}"
                                       "QPushButton:hover{border-image: url(image/ui/button2_1.png)}" 
                                  "QPushButton:pressed{border-image: url(image/ui/button2_2.png)}")
        self.bt3.setStyleSheet("QPushButton{border-image: url(image/ui/button3.png)}"
                                       "QPushButton:hover{border-image: url(image/ui/button3_1.png)}" 
                                  "QPushButton:pressed{border-image: url(image/ui/button3_2.png)}")
        
        #点击“开始游戏”
        self.bt1.clicked.connect(self.begin)
        
        #点击“游戏说明”
        self.bt2.clicked.connect(self.introduction)
        
        #点击“关于我们”
        self.bt3.clicked.connect(self.about)
        
    windowList = []
    def introduction(self):
        child = childWindow('Introduction','image/introduction.png')
        self.windowList.append(child)
        self.close()
        child.show()
        
    def about(self):
        child = childWindow('About','image/introduction.png')
        self.windowList.append(child)
        self.close()
        child.show()
        
    def begin(self):
        tag = run_game()
        qwin = queryWindow(tag)
        self.windowList.append(qwin)
        self.close()
        qwin.show()
            
            
class childWindow(QWidget):
    
    def __init__(self,name,src):
        super().__init__()
        self.initUI(name,src)

    def initUI(self,name,src):
        # 设置GUI窗口的位置和尺寸
        self.setGeometry(710, 140, 534, 720)
        self.center()
        self.setWindowTitle(name)
    
        #应用图标
        self.setWindowIcon(QIcon('image/icon.png'))
        
        #载入背景图片
        window_pale = QPalette() 
        window_pale.setBrush(self.backgroundRole(),QBrush(QPixmap(src))) 
        self.setPalette(window_pale)
        
    windowList = []
    def closeEvent(self, event):
        the_window = mainWindow()
        self.windowList.append(the_window)
        the_window.show()
        event.accept()
    
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,  
        (screen.height() - size.height()) / 2)
        
class queryWindow(QWidget):
    
    def __init__(self,tag):
        super().__init__()
        self.initUI(tag)

    def initUI(self,tag):
        # 设置GUI窗口的位置和尺寸
        self.resize(421, 360)
        self.center()
        name = 'You Win!' if tag==0 else 'You Lose.'
        self.setWindowTitle(name)
    
        #应用图标
        self.setWindowIcon(QIcon('image/icon.png'))
        
        #载入背景图片
        window_pale = QPalette() 
        if tag==0:
            window_pale.setBrush(self.backgroundRole(),QBrush(QPixmap('image/ui/inform_s.jpg'))) 
        else:
            window_pale.setBrush(self.backgroundRole(),QBrush(QPixmap('image/ui/inform_f.jpg'))) 
        self.setPalette(window_pale)
        
        #按钮
        self.bt1 = QPushButton('',self)
        self.bt1.setGeometry(QRect(50, 240, 136, 63))
        self.bt2 = QPushButton('',self)
        self.bt2.setGeometry(QRect(240, 240, 136, 63))
        
        self.bt1.setStyleSheet("QPushButton{border-image: url(image/ui/return.png)}"
                                       "QPushButton:hover{border-image: url(image/ui/return_1.png)}" 
                                  "QPushButton:pressed{border-image: url(image/ui/return_2.png)}")
        if tag ==0:
            self.bt2.setStyleSheet("QPushButton{border-image: url(image/ui/continue.png)}"
                                           "QPushButton:hover{border-image: url(image/ui/continue_1.png)}" 
                                      "QPushButton:pressed{border-image: url(image/ui/continue_2.png)}")
        else:
            self.bt2.setStyleSheet("QPushButton{border-image: url(image/ui/restart.png)}"
                                           "QPushButton:hover{border-image: url(image/ui/restart_1.png)}" 
                                      "QPushButton:pressed{border-image: url(image/ui/restart_2.png)}")

        #点击“返回”
        self.bt1.clicked.connect(self.tomain)
        #点击“继续”
        self.bt2.clicked.connect(self.begin)
        
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,  
        (screen.height() - size.height()) / 2)
        
    windowList = []
    def tomain(self, event):
        the_window = mainWindow()
        self.windowList.append(the_window)
        self.close()
        the_window.show()
        
    def begin(self):
        tag = run_game()
        the_window = queryWindow(tag)
        self.windowList.append(the_window)
        self.close()
        the_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = mainWindow()
    win.show()
    exit(app.exec_())