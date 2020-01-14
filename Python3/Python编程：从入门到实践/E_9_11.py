class User():
    """a class for user"""
    def __init__(self, first_name, last_name, gender, age):
        """init the user instance"""
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.age = age
        self.login_attempts = 0
    
    def describe_user(self):
        """describe the user infomation"""
        print("User Name: {} {}".format(self.last_name, self.first_name))
        print("Gender: {}".format(self.gender))
        print("Age: {}".format(self.age))
        
    def greet_user(self):
        """say Hello to user"""
        print("Hello, {} {}".format(self.last_name.title(), self.first_name.title()))
        
    def increment_login_attempts(self):
        """increase login attempts by 1"""
        self.login_attempts += 1
    
    def reset_login_attempts(self):
        """reset login attempts to 0"""
        self.login_attempts = 0

class Admin(User):
    """a child class of user"""
    def __init__(self, first_name, last_name, gender, age):
        """init class of Admin"""
        super().__init__(first_name, last_name, gender, age)
        self.privileges = ["can add post", "can delete post", "can ban user"]
    
    def show_privileges(self):
        """show Admin privileges"""
        print(",".join(self.privileges))
