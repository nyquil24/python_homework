

#Task 1 

def hello():
    return "Hello!"

#Task 2 
def greet(name): 
    return f"Hello, {name}!"

#Task 3 

def calc(a,b,operation="multiply"): 
    
    if operation == "add":     
        return a + b  
          
    elif operation == "subtract":     
        return a - b 
    
    elif operation == "divide":
        
        try: 
            quotient = a/b
        except ZeroDivisionError:
            print("You can't divide by 0!")
        else:
            return quotient
    
    elif operation == "multiply": 
       return a * b 
    
    else: 
        return "Default: " 


#Task 4

def data_type_conversion(value, type):
    
    try: 
        if type == "int": 
            return int(value)
        elif type == "float":
            return float(value)
        elif type == "str":
            return str(value)
        else: 
            return "Invalid data type"
    except ValueError: 
        return f"You can't convert {value} into a {type}"
    except TypeError:
        return f"You can't convert {value} into a {type}"

#Task 5

def grade(*args): 
    try:
        average = sum(args)/len(args)
        
        if average > 90: 
            return "A"
        elif 80 <= average <= 89:
            return "B"
        elif 70 <= average <= 79:
            return "C"
        elif 60 <= average <= 69:
            return "D"
        elif average < 60: 
            return "F"
        else: 
            return "Invalid data" 
    
    except ValueError: 
        return f"Invalid data was provided"
    except TypeError:
        return f"Invalid data was provided"

#Task 6 

def repeat(string, count): 
    new_string = ""
        
    for i in range(count): 
        new_string += string
        
    return new_string 

#Task 7

def student_scores(position,**kwargs): 
    
    if position == "best":
        
        lst = ""
        
        for key, value in kwargs.items(): 
            
            if key[value] > key[value - 1]:
                lst += key 
            else: 
                continue 
            
        return lst
            
            
    else: 
        sum = 0 
        
        for value in kwargs.values(): 
            sum += value
        mean = sum/len(value +1) 

        return mean


#Task 8

def titleize(string):

    little = ["a","on","an","the", "of", "and", "is", "in"]
    
    new_string = string.split()

    for i, string in enumerate(new_string):
        if i == 0 or i == len(new_string) - 1: 
            new_string[i] = string.capitalize() 
        elif string not in little: 
            new_string[i] = string.capitalize()
        else: 
            new_string[i] =  string.lower()

    return " ".join(string)         


#Task 9

def hangman(secret, guess):

    hang = []

    for letter in secret: 
        if letter in guess: 
           hang.append(letter)
        else:
            hang.append("_") 
    return hang         

#Task 10

def pig_latin(word): 
    
    vowel = ['A','E','I','O','U','a','e','i','o','u']

    if word[0] in vowel:
        latin = word + "ay"
    
    elif word[0:2] == "qu":
        latin = word[3:]  + word[0:2] +  "ay"
        
    elif word[1:3] == "qu": 
        latin = word[3:]  + word[0:3] + "ay"
    
    elif word[0] not in vowel: 
        latin = word[1:] + word[0] + "ay"

    return latin 
    


