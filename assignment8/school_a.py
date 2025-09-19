#%%
import sqlite3
#%%
# Connect to a new SQLite database
with  sqlite3.connect("../db/school.db") as conn:  # Create the file here, so that it is not pushed to GitHub!
    print("Database created and connected successfully.")

# The "with" statement closes the connection at the end of that block.  You could close it explicitly with conn.close(), but in this case
# the "with" statement takes care of that.
#%% 
    cursor = conn.cursor() 

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        student_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        age INTEGER,
        major TEXT
    )
    """)
#%%
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Courses (
        course_id INTEGER PRIMARY KEY,
        course_name TEXT NOT NULL UNIQUE,
        instructor_name TEXT
    )
    """)
#%%
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Enrollments (
        enrollment_id INTEGER PRIMARY KEY,
        student_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES Students (student_id),
        FOREIGN KEY (course_id) REFERENCES Courses (course_id)
    )
    """)

    print("Tables created successfully.")
# %%

# Connect to the databas

# Insert sample data into tables
cursor.execute("INSERT INTO Students (name, age, major) VALUES ('Alice', 20, 'Computer Science')")
cursor.execute("INSERT INTO Students (name, age, major) VALUES ('Bob', 22, 'History')") 
cursor.execute("INSERT INTO Students (name, age, major) VALUES ('Charlie', 19, 'Biology')") 
cursor.execute("INSERT INTO Courses (course_name, instructor_name) VALUES ('Math 101', 'Dr. Smith')")
cursor.execute("INSERT INTO Courses (course_name, instructor_name) VALUES ('English 101', 'Ms. Jones')") 
cursor.execute("INSERT INTO Courses (course_name, instructor_name) VALUES ('Chemistry 101', 'Dr. Lee')") 

conn.commit() 
# If you don't commit the transaction, it is rolled back at the end of the with statement, and the data is discarded.
print("Sample data inserted successfully.")
# %%
