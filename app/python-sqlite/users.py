
class User:
    """Template for username and password"""

    def __init__(self,un, pw):
        self.UserLogin = un
        self.PW = pw
    
    @property
    def returnUser(self):
        return UserLogin
    
    @property
    def returnPassw(self):
        return PW