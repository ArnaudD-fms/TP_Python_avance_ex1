import unittest
from datetime import date

import pymysql

from daos.course_dao import CourseDao
from models.course import Course
from models.teacher import Teacher


class TestCourseDao(unittest.TestCase):

    def setUp(self):
        self.course_dao = CourseDao()

    def test_read_existing_course(self):
        course = self.course_dao.read(1)

        self.assertIsNotNone(course)
        self.assertIsInstance(course, Course)
        self.assertEqual(course.id, 1)
        self.assertEqual(course.name, "Français")
        self.assertEqual(course.start_date, date(2024, 1, 29))
        self.assertEqual(course.end_date, date(2024, 2, 16))

    def test_read_not_existing_course(self):
        course = self.course_dao.read(999999)

        self.assertIsNone(course)

    def test_create_course(self):
        course = Course("Cuisine", date(2026, 9, 8), date(2026, 9, 9))
        teacher = Teacher("Test", "Test", 99, date(2026, 1, 1))
        teacher.id = 1
        course.teacher = teacher

        result = self.course_dao.create(course)

        self.assertNotEqual(result, 0)
        self.assertIsNotNone(course.id)
        self.assertEqual(result, course.id)

    def test_create_course_no_associaite_teacher(self):
        course = Course("Cuisine", date(2026, 9, 8), date(2026, 9, 9))

        result = self.course_dao.create(course)
        self.assertEqual(result, 0)

    def test_create_course_with_unknown_teacher(self):
        course = Course("Cuisine", date(2026, 9, 8), date(2026, 9, 9))
        teacher = Teacher("Test", "Test", 99, date(2026, 1, 1))
        teacher.id = 99
        course.teacher = teacher

        result = self.course_dao.create(course)
        self.assertEqual(result, 0)


    if __name__ == '__main__':
        unittest.main()
