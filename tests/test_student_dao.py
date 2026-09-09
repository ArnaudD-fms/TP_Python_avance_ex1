import unittest

from daos.dao import Dao
from daos.student_dao import StudentDao
from models.student import Student


class TestStudentDao(unittest.TestCase):

    def setUp(self):
        self.student_dao = StudentDao()

        with Dao.connection.cursor() as cursor:
            sql = """
                SELECT COALESCE(MAX(student_nbr), 0) AS max_student_nbr
                FROM student
            """

            cursor.execute(sql)
            record = cursor.fetchone()

        Student.students_nb = record["max_student_nbr"]

    def test_read_existing_student(self):
        student = self.student_dao.read(1)

        self.assertIsNotNone(student)
        self.assertIsInstance(student, Student)
        self.assertEqual(student.student_nbr, 1)
        self.assertEqual(student.first_name, "Paul")
        self.assertEqual(student.last_name, "Dubois")
        self.assertEqual(student.age, 12)

    def test_read_not_existing_student(self):
        student = self.student_dao.read(999999)

        self.assertIsNone(student)

    def test_create_student(self):
        student = Student("first_name_test", "last_name_test", 99)

        result = self.student_dao.create(student)

        self.assertNotEqual(result, 0)
        self.assertIsNotNone(student.student_nbr)
        self.assertEqual(result, student.student_nbr)

    def test_update_student(self):
        # Création d'un nouvel élève
        student = Student("first_name_test", "last_name_test", 99)
        student_id = self.student_dao.create(student)

        # On vérifie que la création a fonctionné
        self.assertNotEqual(student_id, 0)

        # On modifie l'objet student
        student.first_name = "new_first_name"
        student.last_name = "new_last_name"

        # On vérifie que l'update a fonctionné
        result = self.student_dao.update(student)
        self.assertTrue(result)

        # On vérifie que la ligne en base a bien été modifié
        updated_student = self.student_dao.read(student_id)
        self.assertEqual(updated_student.first_name, "new_first_name")
        self.assertEqual(updated_student.last_name, "new_last_name")

    def test_delete_student(self):
        # Création d'un nouvel élève
        student = Student("first_name_test", "last_name_test", 99)
        student_id = self.student_dao.create(student)

        # On vérifie que la création a fonctionné
        self.assertNotEqual(student_id, 0)

        # Suppression de l'èlève
        result = self.student_dao.delete(student)
        self.assertTrue(result)
        deleted_student = self.student_dao.read(student_id)
        self.assertIsNone(deleted_student)

    def tearDown(self):
        with Dao.connection.cursor() as cursor:
            cursor.execute("SELECT COALESCE(MAX(id_person), 0) + 1 AS next_id FROM person")
            next_id = cursor.fetchone()["next_id"]

            cursor.execute(
                f"ALTER TABLE person AUTO_INCREMENT = {next_id}"
            )

        Dao.connection.commit()

    if __name__ == '__main__':
        unittest.main()
