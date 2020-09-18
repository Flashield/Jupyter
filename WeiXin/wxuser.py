import time
import random

class WxUser():
    """微信用户"""
    def __init__(self, user_id):
        self.menu = []
        self.user_id = user_id
        self.act_time = int(time.time())
        self.answer = ''
        self.correct_cnt = 0
        
    def game_calc(self, game_input):
        """运算游戏"""
        
        max_num = 9 * int(self.correct_cnt/3+1)
        num_1 = random.randint(1,max_num)
        num_2 = random.randint(1,max_num)
        if game_input == 'b':
            self.rep_text = '{} + {} = ?'.format(num_1, num_2)
            self.answer = num_1 + num_2
        elif game_input.isdigit() and self.answer:
            if int(float(game_input)) == float(game_input) and int(float(game_input)) == self.answer:
                self.answer = num_1 + num_2
                self.correct_cnt += 1
                self.rep_text = 'Correct! \n连胜{}局 \nNext:\t {} + {} = ?\t'.format(self.correct_cnt,num_1,num_2)
                
            else:
                self.correct_cnt = 0
                self.rep_text = 'Wrong, correct answer is {}! \n \
                连胜{}局，Next:\t {} + {} = ?'.format(self.answer,self.correct_cnt,num_1,num_2)
                self.answer = num_1 + num_2
                
        elif game_input == 'q':
            self.menu.pop()
            self.rep_text = 'You have quited the game!'
        else:
            self.rep_text = 'Please input the correct command!'
        return self.rep_text
    