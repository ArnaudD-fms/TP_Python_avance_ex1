# -*- coding: utf-8 -*-

"""
Classe School
"""

from dataclasses import dataclass, field

from daos.address_dao import AddressDao
from daos.course_dao import CourseDao
from daos.student_dao import StudentDao
from daos.teacher_dao import TeacherDao
from models.course import Course
from models.teacher import Teacher
from models.student import Student


@dataclass
class School:
    """Couche métier de l'application de gestion d'une école,
    reprenant les cas d'utilisation et les spécifications fonctionnelles :
    - courses : liste des cours existants
    - teachers : liste des enseignants
    - students : liste des élèves"""

    courses: list[Course] = field(default_factory=list, init=False)
    teachers: list[Teacher] = field(default_factory=list, init=False)
    students: list[Student] = field(default_factory=list, init=False)

    course_dao: CourseDao = field(default_factory=CourseDao, init=False)
    teacher_dao: TeacherDao = field(default_factory=TeacherDao, init=False)
    student_dao: StudentDao = field(default_factory=StudentDao, init=False)
    address_dao: AddressDao = field(default_factory=AddressDao, init=False)

    def add_course(self, course: Course) -> None:
        """Ajout du cours course à la liste des cours."""
        self.course_dao.create(course)
        self.courses.append(course)

    def add_teacher(self, teacher: Teacher) -> None:
        """Ajout de l'enseignant teacher à la liste des enseignants."""
        self.teacher_dao.create(teacher)
        self.teachers.append(teacher)

    def add_student(self, student: Student) -> None:
        """Ajout de l'élève spécifié à la liste des élèves."""
        self.student_dao.create(student)
        self.students.append(student)

    def display_courses_list(self) -> None:
        """Affichage de la liste des cours avec pour chacun d'eux :
        - leur enseignant
        - la liste des élèves le suivant"""

        for course in self.courses:
            print(f"cours de {course}")
            for student in course.students_taking_it:
                print(f"- {student}")
            print()

    def init_static(self) -> None:
        self.courses = self.course_dao.read_all()
        self.students = self.student_dao.read_all()
        self.teachers = self.teacher_dao.read_all()

        # association des élèves aux cours qu'ils suivent
        for course in self.courses:
            student_numbers = self.course_dao.read_student_numbers(course)

            for student in self.students:
                if student.student_nbr in student_numbers:
                    course.add_student(student)

        # association des enseignants aux cours qu'ils enseignent
        for course in self.courses:
            teacher_id = self.course_dao.read_teacher_id(course)

            for teacher in self.teachers:
                if teacher.id == teacher_id:
                    course.set_teacher(teacher)
