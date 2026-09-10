import unittest

from datetime import date
from daos.course_dao import CourseDao
from daos.dao import Dao
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

    def test_read_all_course(self):
        courses = self.course_dao.read_all()

        self.assertIsInstance(courses, list)
        self.assertGreater(len(courses), 0)

        for course in courses:
            self.assertIsInstance(course, Course)
            self.assertIsNotNone(course.id)

    def test_create_course(self):
        course = Course("Creation_test", date(2026, 9, 8), date(2026, 9, 9))

        # On créer un teacher car on a besoin que le cours possède un teacher et un teacher.id
        # Les attributs du teacher en lui-même n'ont pas d'importance seul l'id compte
        teacher = Teacher("Test", "Test", 99, date(2026, 1, 1))
        teacher.id = 1
        course.teacher = teacher

        result = self.course_dao.create(course)

        self.assertNotEqual(result, 0)
        self.assertIsNotNone(course.id)
        self.assertEqual(result, course.id)

    def test_create_course_no_associaite_teacher(self):
        course = Course("Creation_test", date(2026, 9, 8), date(2026, 9, 9))

        result = self.course_dao.create(course)
        self.assertEqual(result, 0)

    def test_create_course_with_unknown_teacher(self):
        course = Course("Creation_test", date(2026, 9, 8), date(2026, 9, 9))
        teacher = Teacher("Test", "Test", 99, date(2026, 1, 1))
        teacher.id = 99
        course.teacher = teacher

        result = self.course_dao.create(course)
        self.assertEqual(result, 0)

    def test_update_course(self):
        # Création d'un nouveau cours
        teacher = Teacher("Test", "Test", 99, date(2026, 1, 1))
        teacher.id = 1
        course = Course(
            "Test",
            date(2026, 9, 8),
            date(2026, 9, 9)
        )
        course.teacher = teacher
        course_id = self.course_dao.create(course)

        # On vérifie que la création a fonctionné
        self.assertNotEqual(course_id, 0)

        # On modifie l'objet cours
        course.name = "Update_test"
        course.start_date = date(2026, 10, 3)
        course.end_date = date(2026, 10, 5)

        # On vérifie que l'update a fonctionné
        result = self.course_dao.update(course)
        self.assertTrue(result)

        # On vérifie que la ligne en base a bien été modifié
        updated_course = self.course_dao.read(course_id)
        self.assertEqual(updated_course.name, "Update_test")
        self.assertEqual(updated_course.start_date, date(2026, 10, 3))
        self.assertEqual(updated_course.end_date, date(2026, 10, 5))

    def test_delete_course(self):
        teacher = Teacher("Test", "Test", 99, date(2026, 1, 1))
        teacher.id = 1

        # Création d'un nouveau cours
        course = Course(
            "Delete_test",
            date(2026, 9, 8),
            date(2026, 9, 9)
        )
        course.teacher = teacher
        course_id = self.course_dao.create(course)
        self.assertNotEqual(course_id, 0)

        # Suppression du cours
        result = self.course_dao.delete(course)
        self.assertTrue(result)
        deleted_course = self.course_dao.read(course_id)
        self.assertIsNone(deleted_course)

    def tearDown(self):
        with Dao.connection.cursor() as cursor:
            cursor.execute("SELECT COALESCE(MAX(id_course), 0) + 1 AS next_id FROM course")
            next_id = cursor.fetchone()["next_id"]

            cursor.execute(
                f"ALTER TABLE course AUTO_INCREMENT = {next_id}"
            )

        Dao.connection.commit()

    if __name__ == '__main__':
        unittest.main()
