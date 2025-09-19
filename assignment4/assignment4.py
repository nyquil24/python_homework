


#%%
import pandas as pd 
#%%
data = {
    'Name':['Alice','Bob','Charlie'], 
    'Age':[25,30,35], 
    'City':['New York','Los Angeles','Chicago']
}
task1_data_frame = pd.DataFrame(data)
print(task1_data_frame)
#%%
task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]
print(task1_with_salary)


# %%
task1_older = task1_with_salary.copy()
task1_older['Age'] = task1_older['Age'] + 1 
print(task1_older)
# %%
task1_older.to_csv("employees.csv")
#%%
task2_employees = pd.read_csv("employees.csv")
# %%
import json 
new_employees = [
    {"Name": "Eve", "Age":28, "City": "Miami", "Salary": 600000}, 
    {"Name": "Frank", "Age": 40, "City":"Seattle", "Salary":965000}
]
with open("additional_employees.json", "w") as f: 
    json.dump(new_employees, f, indent=4)
#%%
json_employees = pd.read_json("additional_employees.json")
print(json_employees)
# %%
more_employees = pd.concat([json_employees,task2_employees], ignore_index=True)
print(more_employees)
# %%
first_three = more_employees.head(3)
print(first_three)
# %%
last_two = more_employees.tail(2)
print(last_two)
# %%
employee_shape = more_employees.shape
print(employee_shape)
# %%
more_employees.info()
# %%
dirty_data = pd.read_csv("dirty_data.csv")
print(dirty_data)
# %%
clean_data = dirty_data.copy() 
#%% 
# Remove any duplicat rows from the DataFrame 
clean_data = clean_data.drop_duplicates()
print(clean_data)
# %%
# Convert Age to numeric and handle missing values 
clean_data["Age"] = pd.to_numeric(clean_data['Age'], errors='coerce')
print(clean_data)
# %%
# Convert Salary to numeric and replace known placeholders
import numpy as np 
clean_data['Salary'] = clean_data['Salary'].replace(['unknown', 'n/a'], np.nan)
clean_data['Salary'] = pd.to_numeric(clean_data['Salary'], errors='coerce')
# %%
# Fill missing numeric values (fillna). 
clean_data["Age"] = clean_data['Age'].fillna(clean_data['Age'].mean())
clean_data['Salary'] = clean_data['Salary'].fillna(clean_data['Salary'].median())
print(clean_data)
#%%
# Convert to datetime
clean_data['Hire Date'] = pd.to_datetime(clean_data['Hire Date'])
print(clean_data)
# %%
# Strip extra whitespace as uppercase 
clean_data['Name'] = clean_data['Name'].str.strip()
clean_data['Name'] = clean_data['Name'].str.upper()
clean_data['Department'] = clean_data['Department'].str.strip()
clean_data['Department'] = clean_data['Department'].str.upper()
# %%
print(clean_data)
# %%
