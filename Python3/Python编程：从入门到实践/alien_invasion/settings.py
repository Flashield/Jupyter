class Settings():
    """存储《外星人入侵》的所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        # 飞船的运行速度(飞船的运行速度为什么不放在飞船的类中呢？)
        self.ship_speed_factor = 1.5
        self.ship_limit = 1

        # 子弹设置
        self.bullet_speed_factor = 10
        self.bullet_width = 500
        self.bullet_height = 15
        self.bullet_color = 255, 60, 60
        self.bullets_allowed = 3

        # 外星人设置
        self.alien_speed_factor = 1.8
        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右移，为-1表示向左移。
        # 这样用乘法就可以实现按方向移动了
        self.fleet_direction = 1

        # 游戏状态设置(运行速度)
        self.speedup_scale = 1.5
        # 外星人分数
        self.points_scale = 1.5

        # 游戏等级
        self.game_level = 1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变换的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 10
        self.alien_speed_factor = 1
        # fleet_direction为1表示向右移，为-1表示向左移。
        # 这样用乘法就可以实现按方向移动了
        self.fleet_direction = 1

        # 记分
        self.alien_points = 50

        # 游戏等级
        self.game_level = 1

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        #self.bullet_speed_factor *= self.speedup_scale

        # 提高得分速度
        self.alien_points = int(self.alien_points * self.points_scale)

        # 提高游戏等级
        self.game_level += 1
        #print(self.game_level)
