from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
import mysql.connector.errors
import json

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'midterm'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '9280'

mysql = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '9280',
    database = 'midterm'
)

# Set secret key for sessions (used by flash messages)
app.secret_key = 'secretkey'

@app.route('/')
def index():
    cursor = mysql.cursor()
    
    cursor.execute("SELECT * FROM STUDENT")
    students = cursor.fetchall()
        
    cursor.execute("SELECT * FROM COURSE")
    courses = cursor.fetchall()
        
    cursor.execute("SELECT * FROM SECTION")
    sections = cursor.fetchall()
        
    cursor.execute("SELECT * FROM GRADE_REPORT")
    grade_reports = cursor.fetchall()
        
    cursor.execute("SELECT * FROM PREREQUISITE")
    prerequisites = cursor.fetchall() 
    
    students_json = json.dumps(students)
    cursor.close()
    
    return render_template('index.html', students=students_json, courses=courses, sections=sections, grade_reports=grade_reports, prerequisites=prerequisites)

@app.route('/students/<int:id>')
def student_grades(id):
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM STUDENT WHERE Student_number = %s", [id])
    student = cursor.fetchone()
    print(student)
    cursor.execute("""
            SELECT c.Course_name, c.Course_number, s.Section_identifier, s.Instructor,
                   c.Credit_hours, s.Semester, s.Year, g.Grade
            FROM COURSE c
            JOIN SECTION s ON c.Course_number = s.Course_number
            JOIN GRADE_REPORT g ON s.Section_identifier = g.Section_identifier
            WHERE g.Student_number = %s
        """, [id])
    grades = cursor.fetchall()
    print(grades)
    return render_template('studentgrade.html', student=student, grades=grades)

@app.route('/courses/<course_id>')
def course_details(course_id):
    print(course_id)
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM COURSE WHERE Course_number = %s", [course_id])
    course = cursor.fetchone()
    print(course)
    cursor.execute("SELECT Prerequisite_number FROM PREREQUISITE WHERE Course_number = %s", [course_id])
    prerequisites = cursor.fetchall()
    print(prerequisites)
    cursor.close()
    return render_template('course.html', course=course, prerequisites=prerequisites)

@app.route('/sections/<section_id>')
def section(section_id):
    return section_id

@app.route('/students/all')
def all_students():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM STUDENT")
    students = cursor.fetchall()
    print(students)
    return render_template('allstudents.html', students=students)

@app.route('/courses/all')
def all_courses():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM COURSE")
    courses = cursor.fetchall()
    print(courses)
    cursor.execute("SELECT Course_number, Prerequisite_number FROM PREREQUISITE")
    prerequisite= cursor.fetchall()
    print(prerequisite)

    prerequisites = {}
    for row in prerequisite:
        course_number, prerequisite_number = row
        if course_number not in prerequisites:
            prerequisites[course_number] = []
        prerequisites[course_number].append(prerequisite_number)
        
    print(prerequisites)
    return render_template('allcourses.html', courses=courses, prerequisites=prerequisites)

@app.route('/instructors/<instructor_name>')
def instructor_info(instructor_name):
    print(instructor_name)
    cursor = mysql.cursor()
    cursor.execute("SELECT DISTINCT Instructor FROM SECTION WHERE Instructor = %s", [instructor_name])
    instructor = cursor.fetchone()
    print(instructor)
    cursor.execute("""    
            SELECT
                sec.Course_number, cor.Course_name
            FROM SECTION sec
            LEFT JOIN COURSE cor ON sec.Course_number = cor.Course_number
            WHERE sec.Instructor = %s
            """, [instructor_name])

    teach_courses = cursor.fetchall()
    print(teach_courses)
    cursor.close()
    return render_template('instructor.html', instructor=instructor, teach_courses=teach_courses)


if __name__ == "__main__":
    app.run(debug=True)
