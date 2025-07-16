
import traceback
        
# pytest assignment2-test.py
#Task 2
import csv 

def read_employees(): 
    
    empty_dict = {}
    new_rows = []

    try: 
        with open("../csv/employees.csv") as employee_csv: 
            read_csv = csv.reader(employee_csv)
            for i,row in enumerate(read_csv): 
                if i == 0: 
                    empty_dict["fields"] = row 
                else: 
                    new_rows.append(row)
            empty_dict["rows"] = new_rows
           
    except Exception as e: 
        print("An exception occured:", str(e))
        print(traceback.format_exc())
    return empty_dict

employees = read_employees() 
print(employees)

#Task 3 

def column_index(str):
    return employees["fields"].index(str)

employee_id_column = column_index("employee_id")
#Task 4

def first_name(rowNum): 
    column = column_index("first_name")
    return employees["rows"][rowNum][column]


#Task 5

def employee_find(employee_id): 

    def employee_match(row): 
        return int(row[employee_id_column]) == employee_id

    matches=list(filter(employee_match, employees["rows"]))

    return matches 
#Task 6

def employee_find_2(employee_id): 

    matches = list(filter(lambda row: int(row[employee_id_column]) == employee_id, employees["rows"])) 
    return matches 


#Task 7

def sort_by_last_name(): 

    employees["rows"].sort(key=lambda row: row[column_index("last_name")])
    return employees["rows"]

#Task 8

def employee_dict(row):
    keys = employees["fields"][1:]
    values = row[1:]
    return dict(zip(keys,values))

print_dict = employees["rows"][2]
print(employee_dict(print_dict))

#Task 9

def all_employees_dict(): 

   result = {} 

   rows = employees["rows"]
   
   result = {}
   for row in employees["rows"]:
        employee_id = row[0]
        emp_dict = employee_dict(row)
        result[employee_id] = emp_dict
   return result

#Task 10
import os 
def get_this_value(): 
    return os.getenv("THISVALUE")

#Task 11
import custom_module 
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)

# print(custom_module.secret("Howdy")) 

#Task 12

def read_minutes():

    minutes1 = {}
    with open('../csv/minutes1.csv','r') as fil: 
        csv_reader = csv.reader(fil)
        minutes1['fields'] = next(csv_reader)
        minutes1['rows'] = [tuple(row) for row in csv_reader]

    minutes2 = {}
    with open('../csv/minutes2.csv', 'r') as fil: 
        csv_reader = csv.reader(fil)
        minutes2['fields'] = next(csv_reader)
        minutes2['rows'] = [tuple(row) for row in csv_reader]

    return minutes1, minutes2 

minutes1, minutes2 = read_minutes()
#Task 13

def create_minutes_set(): 
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
    combined_set = set1.union(set2)

    return combined_set 

minutes_set = create_minutes_set()
#Task 14

from datetime import datetime 

def create_minutes_list(): 

    lst_minute = list(minutes_set)

    convert_lst = list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")),lst_minute))

    return convert_lst 

minutes_list = create_minutes_list() 

print(minutes_list)

#Task 15

def write_sorted_list(): 

    global minutes_list 

    minutes_list.sort(key=lambda x: x[1])

    converted_minute = list(map(lambda x: (x[0], x[1].strftime("%B %d, %Y")), minutes_list))

    with open('./minutes.csv','w',newline='') as file: 
        writer = csv.writer(file)
        writer.writerow(minutes1['fields'])
        writer.writerows(converted_minute)

    return converted_minute 
