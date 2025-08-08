import json

# Section A: Class Design and Implementation

class Person: 

    # Represents a person with basic information.

    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        
       # Prints the person's details.
        
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Address: {self.address}")

    def to_dict(self):
        
        # Converts the Person object to a dictionary.
        
        return {
            "name": self.name,
            "age": self.age,
            "address": self.address
        }

class Student(Person):
    
    # Represents a student, inheriting from Person.
    
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}  # {"Math": "A"}
        self.courses = []  # ["Physics"]

    def add_grade(self, subject, grade):
        
      #  Adds or updates the grade for a subject.
        
        self.grades[subject] = grade

    def enroll_course(self, course):
        """
        Enrolls the student in a specified course.
        """
        if course not in self.courses:
            self.courses.append(course)

    def display_student_info(self):
        
        # Prints all student details.
        
        print("Student Information:")
        super().display_person_info()
        print(f"ID: {self.student_id}")
        print(f"Enrolled Courses: {', '.join(self.courses)}")
        print(f"Grades: {self.grades}")

    def to_dict(self):
        
        # Converts the Student object to a dictionary for saving.
        
        person_dict = super().to_dict()
        person_dict.update({
            "student_id": self.student_id,
            "grades": self.grades,
            "courses": self.courses
        })
        return person_dict

class Course:
    
    # Represents a course.
    
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []  # List of student IDs

    def add_student(self, student_id):
        """
        Adds a student's ID to the course.
        """
        if student_id not in self.students:
            self.students.append(student_id)

    def display_course_info(self, all_students):
        
        # Prints course details and the names of enrolled students.
        
        print("Course Information:")
        print(f"Course Name: {self.course_name}")
        print(f"Code: {self.course_code}")
        print(f"Instructor: {self.instructor}")
        
        student_names = [s.name for s in all_students if s.student_id in self.students]
        print(f"Enrolled Students: {', '.join(student_names)}")

    def to_dict(self):
        
        # Converts the Course object to a dictionary for saving.
        
        return {
            "course_name": self.course_name,
            "course_code": self.course_code,
            "instructor": self.instructor,
            "students": self.students
        }

# Section B: System Functionalities

class StudentManagementSystem:
    
    # Manages the overall student and course data.
    
    def __init__(self):
        self.students = {}  # student_id: Student object
        self.courses = {}   # course_code: Course object

    def add_new_student(self, name, age, address, student_id):
        
        # Creates and stores a new Student object.
        
        if student_id in self.students:
            print(f"Error: Student with ID {student_id} already exists.")
            return

        new_student = Student(name, age, address, student_id)
        self.students[student_id] = new_student
        print(f"Student {name} (ID: {student_id}) added successfully.")

    def add_new_course(self, course_name, course_code, instructor):
        
        # Creates and stores a new Course object.
        
        if course_code in self.courses:
            print(f"Error: Course with code {course_code} already exists.")
            return

        new_course = Course(course_name, course_code, instructor)
        self.courses[course_code] = new_course
        print(f"Course {course_name} (Code: {course_code}) created with instructor {instructor}.")

    def enroll_student_in_course(self, student_id, course_code):
        
        # Enrolls a student in a course if both exist.
        
        if student_id not in self.students:
            print(f"Error: Student with ID {student_id} not found.")
            return
        if course_code not in self.courses:
            print(f"Error: Course with code {course_code} not found.")
            return

        student = self.students[student_id]
        course = self.courses[course_code]

        student.enroll_course(course.course_name)
        course.add_student(student_id)
        print(f"Student {student.name} (ID: {student_id}) enrolled in {course.course_name} (Code: {course_code}).")

    def add_grade_for_student(self, student_id, course_code, grade):
       
        # Assigns/updates a grade for a student in a specific course.
        
        if student_id not in self.students:
            print(f"Error: Student with ID {student_id} not found.")
            return
        if course_code not in self.courses:
            print(f"Error: Course with code {course_code} not found.")
            return

        student = self.students[student_id]
        course = self.courses[course_code]

        if course.course_name not in student.courses:
            print(f"Error: Student {student.name} is not enrolled in {course.course_name}.")
            return
        
        student.add_grade(course.course_name, grade)
        print(f"Grade {grade} added for {student.name} in {course.course_name}.")

    def display_student_details(self, student_id):
        
        # Displays all details for a given student.
        
        if student_id not in self.students:
            print(f"Error: Student with ID {student_id} not found.")
            return
        
        self.students[student_id].display_student_info()

    def display_course_details(self, course_code):
        
        # Displays all details for a given course.
        
        if course_code not in self.courses:
            print(f"Error: Course with code {course_code} not found.")
            return
        
        # Pass a list of all student objects to the course method for name lookup
        self.courses[course_code].display_course_info(self.students.values())

    def save_data(self, filename="data.json"):
        
        # Saves student and course data to a JSON file.
        
        data = {
            "students": {sid: s.to_dict() for sid, s in self.students.items()},
            "courses": {cc: c.to_dict() for cc, c in self.courses.items()}
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print("All student and course data saved successfully.")

    def load_data(self, filename="data.json"):
        
        # Loads student and course data from a JSON file.
        
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            
            # Reconstruct student objects
            self.students = {}
            for sid, s_data in data["students"].items():
                student = Student(s_data["name"], s_data["age"], s_data["address"], s_data["student_id"])
                student.grades = s_data["grades"]
                student.courses = s_data["courses"]
                self.students[sid] = student

            # Reconstruct course objects
            self.courses = {}
            for cc, c_data in data["courses"].items():
                course = Course(c_data["course_name"], c_data["course_code"], c_data["instructor"])
                course.students = c_data["students"]
                self.courses[cc] = course
            
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No data file found. Starting with empty data.")
        except json.JSONDecodeError:
            print("Error: Invalid JSON data in file.")

# Main CLI loop
if __name__ == "__main__":
    sms = StudentManagementSystem()
    
    while True:
        print("\n==== Student Management System ====")
        print("1. Add New Student")
        print("2. Add New Course")
        print("3. Enroll Student in Course")
        print("4. Add Grade for Student")
        print("5. Display Student Details")
        print("6. Display Course Details")
        print("7. Save Data to File")
        print("8. Load Data from File")
        print("0. Exit")
        
        option = input("Select Option: ")
        
        if option == '1':
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            address = input("Enter Address: ")
            student_id = input("Enter Student ID: ")
            sms.add_new_student(name, age, address, student_id)
            
        elif option == '2':
            course_name = input("Enter Course Name: ")
            course_code = input("Enter Course Code: ")
            instructor = input("Enter Instructor Name: ")
            sms.add_new_course(course_name, course_code, instructor)
            
        elif option == '3':
            student_id = input("Enter Student ID: ")
            course_code = input("Enter Course Code: ")
            sms.enroll_student_in_course(student_id, course_code)
            
        elif option == '4':
            student_id = input("Enter Student ID: ")
            course_code = input("Enter Course Code: ")
            grade = input("Enter Grade: ")
            sms.add_grade_for_student(student_id, course_code, grade)

        elif option == '5':
            student_id = input("Enter Student ID: ")
            sms.display_student_details(student_id)
            
        elif option == '6':
            course_code = input("Enter Course Code: ")
            sms.display_course_details(course_code)
            
        elif option == '7':
            sms.save_data()
            
        elif option == '8':
            sms.load_data()
            
        elif option == '0':
            print("Exiting Student Management System. Goodbye!")
            break
            
        else:
            print("Invalid option. Please try again.")