import sqlite3
from users import User

conn = sqlite3.connect('users.db')
#conn = sqlite3.connect(':memory:')

c = conn.cursor()

#c.execute("""CREATE TABLE pyUsers(
#           pyUserName text,
#          pyPassword text
#           )""") 

# Function to insert credentials
def insert_user(usr):
    with conn:
        c.execute("INSERT INTO pyUsers VALUES (:UserLogin, :PW)", {'UserLogin':usr.UserLogin, 'PW':usr.PW})


def get_userName(usr):
    with conn:
        c.execute("SELECT pyUserName FROM pyUsers WHERE pyUserName =:usr", {'usr':usr.UserLogin})
        return c.fetchone()

def get_PassW(u_passw):
    with conn:
        c.execute("SELECT pyPassword FROM pyUsers WHERE pyPassword =:u_passw",{'u_passw':u_passw.PW})
        return c.fetchone()


temp_user = User('a','a')

insert_user(temp_user)

print(get_userName(temp_user))
print(get_PassW(temp_user))

conn.close()

