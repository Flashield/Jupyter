from E_9_12_1 import User

class Admin(User):
    """a child class of user"""
    def __init__(self, first_name, last_name, gender, age):
        """init class of Admin"""
        super().__init__(first_name, last_name, gender, age)
        self.privileges = ["can add post", "can delete post", "can ban user"]
    
    def show_privileges(self):
        """show Admin privileges"""
        print(",".join(self.privileges))