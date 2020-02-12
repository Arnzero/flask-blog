import sqlite3
from employee import Employee

#conn = sqlite3.connect('employee.db')
# uses RAM to recreate the instance each time
conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute("""CREATE TABLE employees (
            first text,
            last text,
            pay integer
            )""")

# with conn: commits for us
def insert_emp(emp):
    with conn:
         c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': emp.first, 'last': emp.last, 'pay': emp.pay})


def get_emps_by_name(lastname):
    c.execute("SELECT * FROM employees WHERE last=:last", {'last':lastname})
    return c.fetchall()


def update_pay(emp,pay):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                    {'first': emp.first, 'last':emp.last, 'pay':pay})

def remove_emp(emp):
    print('we insdie remove')
    with conn:
        c.execute("DELETE from employees WHERE first = :first AND last = :last",
            {'first': emp.first, 'last': emp.last})


emp_1 = Employee('John', 'Haro', 20)
emp_2 = Employee('Jane', 'Haro', 220)


#print(emp_1.first)
#print(emp_1.last)
#print(emp_1.pay)

# below  we have replaced hardcoding with funs above
"""
#using this is bad practice
#c.execute("INSERT INTO employees VALUES ('{}', '{}', {})".format(empl_1.first, emp_1.last, emp_1.pay))
# Option 1 
c.execute("INSERT INTO employees VALUES (?,?,?)", (emp_1.first, emp_1.last, emp_1.pay))
conn.commit()

# Option 2
c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': emp_2.first, 'last': emp_2.last, 'pay': emp_2.pay})
conn.commit()

#bad practice
c.execute("SELECT * FROM employees WHERE last='Haro'")
print(c.fetchall())
# Option 1
c.execute("SELECT * FROM employees WHERE last=?", ('Haro',))

print(c.fetchall())

c.execute("SELECT * FROM employees WHERE last=:last", {'last':'Haro'})
print(c.fetchall())

# options to grab tuple data fetchone(), fetchmany() fetchall()
"""

insert_emp(emp_1)
insert_emp(emp_2)

emps = get_emps_by_name('Haro')

print(emps)
print("after")


update_pay(emp_2, 1)
remove_emp(emp_1)

print(emps)

conn.close()