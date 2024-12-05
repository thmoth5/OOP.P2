from abc import ABC, abstractmethod

class AbstractCourse(ABC):
    @abstractmethod
    def create_course(self, name, code, credit_hours=3, max_students=25, priority="Normal"):
        pass

    @abstractmethod
    def enroll_student(self):
        pass

    @abstractmethod
    def show_course(self):
        pass


class Course(AbstractCourse):
    def create_course(self, name, code, credit_hours=3, max_students=25, priority="Normal"):
        self.name = name
        self.code = code
        self.credit_hours = credit_hours
        self.max_students = max_students
        self.enrolled_students = 0
        self.priority = priority
        self.attendance = {}

    def enroll_student(self):
        if self.enrolled_students < self.max_students:
            self.enrolled_students += 1
            return True
        else:
            print(f"Alert: {self.name} is full.")  # Alert if the course is full
            return False

    def mark_attendance(self, student_id, present=True):
        if student_id not in self.attendance:
            self.attendance[student_id] = []
        self.attendance[student_id].append(present)

    def show_attendance(self):
        return self.attendance

    def show_course(self):
        return f"{self.name} ({self.code}), Priority: {self.priority}, Credit Hours: {self.credit_hours}, Enrolled: {self.enrolled_students}/{self.max_students}"


class Student:
    id_counter = 1
    ID_PREFIX = "UOB-"
    def __init__(self):
        self.id = None
        self.name = None
        self.classes = []
        self.__grades = {}
        self.activity_log = []
        self.max_classes = 5

    def set_student(self, name):
        self.id = f"{Student.ID_PREFIX}{Student.id_counter:04d}"
        Student.id_counter += 1
        self.name = name
        self.__grades = {}

    def enroll_in_class(self, course):
        # Check for schedule conflicts
        for existing_course in self.classes:
            if existing_course == course:
                return f"Error: Conflict with {existing_course.name}."

        if len(self.classes) >= self.max_classes:
            return "Error: You have reached the maximum number of classes."
        elif course.code in [c.code for c in self.classes]:
            return f"Error: You are already enrolled in {course.code}."
        else:
            success = course.enroll_student()
            if success:
                self.classes.append(course)
                self.log_activity(f"Enrolled in {course.name}.")
                return f"Successfully enrolled in {course.name}!"
            else:
                return f"Error: {course.name} is full."

    def log_activity(self, activity):
        self.activity_log.append(activity)

    def show_activity_log(self):
        return "\n".join(self.activity_log)

    def drop_class(self, course_code):
        for course in self.classes:
            if course.code == course_code:
                self.classes.remove(course)
                course.enrolled_students -= 1
                self.log_activity(f"Dropped {course.name}.")
                return f"Successfully dropped {course.name}."
        return "Error: Course not found."

    def show_student(self):
        enrolled_courses = ', '.join([course.code for course in self.classes])
        return (f"ID: {self.id}, Name: {self.name}, Enrolled Classes: {enrolled_courses}")
    def __repr__(self):
        return f"{self.name}, id is {self.id}"

class Schedule:
    def create_schedule(self):
        self.courses = {
            "Sunday": [Course(), Course(), Course(), Course()],
            "Monday": [Course(), Course(), Course(), Course()],
            "Tuesday": [Course(), Course(), Course(), Course()],
            "Wednesday": [Course(), Course(), Course(), Course()]
        }
        self.schedule_times = ["8:30 AM - 10:30 AM", "10:30 AM - 12:30 PM", "12:30 PM - 2:30 PM", "2:30 PM - 4:30 PM"]

        # Add courses to the schedule
        self.courses["Sunday"][0].create_course("Data Structures", "CS101", priority="High")
        self.courses["Sunday"][1].create_course("AI", "CS102")
        self.courses["Sunday"][2].create_course("Web Development", "CS103")
        self.courses["Sunday"][3].create_course("Mathematics", "CS104")
        self.courses["Monday"][0].create_course("Machine Learning", "CS105")
        self.courses["Monday"][1].create_course("Cyber Security", "CS106")
        self.courses["Monday"][2].create_course("Cloud Computing", "CS107")
        self.courses["Monday"][3].create_course("Game Development", "CS108")
        self.courses["Tuesday"][0].create_course("Databases", "CS109")
        self.courses["Tuesday"][1].create_course("Networks", "CS110")
        self.courses["Tuesday"][2].create_course("Operating Systems", "CS111")
        self.courses["Tuesday"][3].create_course("Algorithms", "CS112")
        self.courses["Wednesday"][0].create_course("Software Engineering", "CS113")
        self.courses["Wednesday"][1].create_course("Web Design", "CS114")
        self.courses["Wednesday"][2].create_course("Mobile Apps", "CS115")
        self.courses["Wednesday"][3].create_course("Big Data", "CS116")

    def display_schedule(self, day):
        schedule_str = f"Schedule for {day}:\n"
        courses = self.courses.get(day, [])

        if courses:
            for i in range(len(courses)):
                time = self.schedule_times[i]
                course = courses[i]
                schedule_str += f"{time}: {course.show_course()}\n"
        else:
            schedule_str += "No courses available.\n"

        return schedule_str

    def set_holiday(self, day):
        if day in self.courses:
            self.courses[day] = []
            return f"Holiday set for {day}."
        return "Invalid day."

    def __getitem__(self, time):
        for day, courses in self.courses.items():
            for i, course in enumerate(courses):
                if self.schedule_times[i] == time:
                    return course
        return None


student1 = Student()
student1.set_student("Ali")


schedule = Schedule()
schedule.create_schedule()

# Display the schedule for Sunday
print(schedule.display_schedule("Sunday"))

# Enroll the student in a course
course_to_enroll = schedule.courses["Sunday"][0]  # Data Structures
print(student1.enroll_in_class(course_to_enroll))

# Show student's activity log
print("\nActivity Log:")
print(student1.show_activity_log())

# Mark attendance for the student
course_to_enroll.mark_attendance(student1.id, present=True)
course_to_enroll.mark_attendance(student1.id, present=False)

# Display attendance
print("\nAttendance for Data Structures:")
print(course_to_enroll.show_attendance())

# Drop a course
print("\nDropping a course:")
print(student1.drop_class("CS101"))

# Updated activity log
print("\nUpdated Activity Log:")
print(student1.show_activity_log())

# Set a holiday
print("\nSetting holiday:")
print(schedule.set_holiday("Sunday"))

# Display updated schedule for Sunday
print("\nUpdated Schedule for Sunday:")
print(schedule.display_schedule("Sunday"))

# Test accessing a course by time
time_slot = "10:30 AM - 12:30 PM"
lecture = schedule[time_slot]
if lecture:
    print(f"\nLecture at {time_slot}: {lecture.show_course()}")
else:
    print(f"\nNo lecture at {time_slot}.")
