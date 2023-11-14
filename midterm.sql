#DDL statements

use midterm;

#Student table
create table STUDENT(
	Name varchar (100),
	Student_number int (100) primary key,
	Class int (100),
	Major varchar (100)
);

#Course table
create table COURSE(
Course_name varchar (100),
Course_number varchar (100) primary key,
Credit_hours int (100),
Department varchar (100)
);

#Section table
create table SECTION(
	Section_identifier int (100) primary key,
	Course_number varchar (100),
	Semester varchar (100),
	Year int (100),
	Instructor varchar (100),
    Foreign key (Course_number) references course (Course_number)
);

#Grade report table
create table GRADE_REPORT(
Student_number int (100),
Section_identifier int (100),
Grade varchar (100),
primary key (Student_number, Section_identifier),
foreign key (Student_number) references STUDENT(Student_number),
foreign key (Section_identifier) references SECTION(Section_identifier)
);

#Prerequisite Table
create table PREREQUISITE(
Course_number varchar (100),
Prerequisite_number varchar (100) primary key,
Foreign key (Course_number) references course (Course_number),
Foreign key (Prerequisite_number) references course (Course_number)
);



#DML statements

insert into STUDENT(Name, Student_number, Class, Major)
values 
('Smith','17','1','CS'),
('Brown','8','2','CS');

insert into COURSE(Course_name, Course_number, Credit_hours, Department)
values 
('Intro to Computer Science','CS1310','4','CS'),
('Data Structures','CS3320','4','CS'),
('Discrete Mathematics','MATH2410','3','MATH'),
('Database','CS3380','3','CS');

insert into SECTION(Section_identifier, Course_number, Semester, Year, Instructor)
values 
('85', 'MATH2410','Fall','07','King'),
('92', 'CS1310','Fall','07','Anderson'),
('102', 'CS3320','Spring','08','Knuth'),
('112', 'MATH2410','Fall','08','Chang'),
('119', 'CS1310','Fall','08',' Anderson'),
('135', 'CS3380','Fall','08','Stone');

insert into GRADE_REPORT(Student_number, Section_identifier, Grade)
values 
('17','112','B'),
('17','119','C'),
('8','85','A'),
('8','92','A'),
('8','102','B'),
('8','135','A');

insert into PREREQUISITE(Course_number, Prerequisite_number)
values 
('CS3380','CS3320'),
('CS3380','MATH2410'),
('CS3320','CS1310');

