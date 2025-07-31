
import csv 

with open("../csv/employees.csv", newline='') as file: 
    reader = csv.reader(file)
    lists = list(reader)

    employee_names = [row[0] + " " + row[1] for row in lists[1:]]
    print(employee_names)

    letter_e = [name for name in employee_names if 'e' in name.lower()]
    print(letter_e)