class Restaurant():
    """a simple class for restaurants"""
    def __init__(self, restaurant_name, cuisine_type):
        """init the class restaurant"""
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type
        self.number_served = 0
    
    def describe_restaurant(self):
        """describe the name of restaurant"""
        print("Restaurant name is {} and the cuisine type is {}.".format(self.restaurant_name,self.cuisine_type))
    
    def open_restaurant(self):
        """change the restaurant status"""
        print("Restaurant is opened.")
        
    def set_number_served(self, served_number):
        """set the number of people being served"""
        self.number_served = served_number
    
    def increment_number_served(self, increment_number):
        """increase the number served by increment number"""
        self.number_served += increment_number