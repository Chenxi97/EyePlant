from configure import *


class drop_object:
    
    def __init__(self,speed,radius,object_type):
        self.speed = speed
        self.radius = radius
        self.x = random.randint(120,520)
        self.y = UP_LINE
        #'sunshine':0,'bomb':1,'life':2,
        self.object_type = object_type
        
    #向下移动speed个单位
    def move(self):
        self.y+=self.speed
        
    #检测是否与眼睛重合
    def is_collision(self,pos_list):
        for pos in pos_list:
            dis = math.hypot(self.x-pos[0],self.y-pos[1])
            if dis <= self.radius:
                return True
        return False
    
    #检测是否触底
    def is_bottom(self):
         return True if self.y>BOTTOM_LINE else False
        

class Game_manager:
    
    def __init__(self):
        self.level = 0
        self.speed = SPEED_LIST[self.level]
        self.rate = RATE_LIST[self.level]
        self.life = LIFE_NUMBER
        self.sunshine = 0
        self.alive_flag = 1
        self.growing_flag =0
        self.idx = IDX_LIST[self.level][0]
        self.end_idx = IDX_LIST[self.level][1]
        self.finish_flag = 0

    def catch_object(self,object_type):
        if object_type==0:
            self.sunshine+=1
            if self.sunshine>=MAX_SUN:
                self.growing_flag=1
                
        elif object_type==1:
            self.life-=1
            if self.life<=0:
                self.alive_flag=0
        else:
            self.life+=1
            
    def upgrade(self,o_manager):
        self.level += 1
        self.speed = SPEED_LIST[self.level]
        self.rate = RATE_LIST[self.level]
        self.idx = IDX_LIST[self.level][0]
        self.end_idx = IDX_LIST[self.level][1]
        self.sunshine = 0
        self.growing_flag = 0
        o_manager.clear()
        
class Object_manager:
    
    def __init__(self):
        self.object_list=[]
        
    #'sunshine':0,'bomb':1,'life':2,
    def create_object(self,g_manager):
        object_type = self.__random_index(g_manager.rate)
        new_object = drop_object(g_manager.speed,RADIUS,object_type)
        self.object_list.append(new_object)
    
    def __random_index(self,rate):
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
 
    def update_object(self,pos_list):
        
        #删除触底物体
        while(len(self.object_list)>0 and self.object_list[0].is_bottom()):
            del(self.object_list[0])
            
        #处理碰撞物体
        ob_list=[]
        new_object_list=[]
        for ob in self.object_list:
            if ob.is_collision(pos_list):
                ob_list.append(ob)
            else:
                new_object_list.append(ob)
        self.object_list = new_object_list
        
        #所有物体向下移动
        for ob in self.object_list:
            ob.move()
            
        return ob_list

    
    def clear(self):
        self.object_list.clear()
    
class Thread_task:
    
    def __init__(self,o_manager):
        self.__running = True
        self.job = o_manager

    def terminate(self):
        self.__running = False

    def run(self, g_manager):
        while self.__running:
            self.job.create_object(g_manager)
            time.sleep(TIME_INTERVAL_LIST[g_manager.level])