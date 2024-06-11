import sqlite3
import streamlit as st

def create_table():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def insert_student(roll_no, name, email, age, gender):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO students (roll_no, name, email, age, gender) VALUES (?, ?, ?, ?, ?)
    ''', (roll_no, name, email, age, gender))
    conn.commit()
    conn.close()

def get_students():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM students')
    rows = cur.fetchall()
    conn.close()
    return rows

def update_student(roll_no, name, email, age, gender):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('''
    UPDATE students SET name = ?, email = ?, age = ?, gender = ? WHERE roll_no = ?
    ''', (name, email, age, gender, roll_no))
    conn.commit()
    conn.close()

def delete_student(roll_no):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('''
    DELETE FROM students WHERE roll_no = ?
    ''', (roll_no,))
    conn.commit()
    conn.close()

def validate_input(name, email, age, gender, roll_no=None):
    if not name:
        st.error('Name cannot be empty')
        return False
    if not email or '@' not in email:
        st.error('Invalid email')
        return False
    if not age.isdigit():
        st.error('Age must be an integer')
        return False
    if gender not in ['Male', 'Female', 'Other']:
        st.error('Gender must be Male, Female, or Other')
        return False
    if roll_no and not (roll_no.startswith("22CSR") and len(roll_no) == 8 and roll_no[5:].isdigit()):
        st.error('Roll No must be in the format 22CSRxxx')
        return False
    return True

def main():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #F0F8FF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title('Student Management System')
    
    create_table()

    menu = ['Add Student', 'Update Student', 'Delete Student', 'View Students']
    choice = st.selectbox('Select Operation', menu)

    if choice == 'Add Student':
        st.subheader('Add Student')
        with st.expander("Add New Student"):
            roll_no = st.text_input('Roll No')
            name = st.text_input('Name')
            email = st.text_input('Email')
            age = st.text_input('Age')
            gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
            submit_button = st.button('Add Student')
        
        if submit_button and validate_input(name, email, age, gender, roll_no):
            insert_student(roll_no, name, email, int(age), gender)
            st.success(f'Student {name} added successfully with Roll No {roll_no}')

    elif choice == 'Update Student':
        st.subheader('Update Student')
        with st.expander("Update Existing Student"):
            roll_no = st.text_input('Roll No')
            name = st.text_input('Name')
            email = st.text_input('Email')
            age = st.text_input('Age')
            gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
            submit_button = st.button('Update Student')
        
        if submit_button and validate_input(name, email, age, gender, roll_no):
            update_student(roll_no, name, email, int(age), gender)
            st.success(f'Student with Roll No {roll_no} updated successfully')

    elif choice == 'Delete Student':
        st.subheader('Delete Student')
        with st.expander("Delete Existing Student"):
            roll_no = st.text_input('Roll No')
            submit_button = st.button('Delete Student')
        
        if submit_button and roll_no:
            delete_student(roll_no)
            st.success(f'Student with Roll No {roll_no} deleted successfully')

    elif choice == 'View Students':
        st.subheader('View Students')
        students = get_students()
        st.table(students)

if __name__ == '__main__':
    main()
