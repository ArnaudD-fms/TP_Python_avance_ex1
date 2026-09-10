import unittest
from datetime import date

from daos.dao import Dao
from daos.teacher_dao import TeacherDao
from models.teacher import Teacher


class testTeacherDao(unittest.TestCase):

    def setUp(self):
        self.teacher_dao = TeacherDao()

    def test_read_existing_teacher(self):
        teacher = self.teacher_dao.read(1)

        self.assertIsNotNone(teacher)
        self.assertIsInstance(teacher, Teacher)
        self.assertEqual(teacher.id, 1)
        self.assertEqual(teacher.first_name, "Victor")
        self.assertEqual(teacher.last_name, "Hugo")
        self.assertEqual(teacher.age, 23)
        self.assertEqual(teacher.hiring_date, date(2023, 9, 4))

    def test_read_not_existing_teacher(self):
        teacher = self.teacher_dao.read(999999)

        self.assertIsNone(teacher)

    def test_create_teacher(self):
        teacher = Teacher("first_name_test", "last_name_test", 99, date.today())

        result = self.teacher_dao.create(teacher)

        self.assertNotEqual(result, 0)
        self.assertIsNotNone(teacher.id)
        self.assertEqual(result, teacher.id)

    def test_update_teacher(self):
        # Création d'un nouveau professeur
        teacher = Teacher("first_name_test", "last_name_test", 99, date.today())
        teacher_id = self.teacher_dao.create(teacher)

        # On vérifie que la création a fonctionné
        self.assertNotEqual(teacher_id, 0)

        # On modifie l'objet student
        teacher.first_name = "new_first_name"
        teacher.last_name = "new_last_name"

        # On vérifie que l'update a fonctionné
        result = self.teacher_dao.update(teacher)
        self.assertTrue(result)

        # On vérifie que la ligne en base a bien été modifié
        updated_teacher = self.teacher_dao.read(teacher_id)
        self.assertEqual(updated_teacher.first_name, "new_first_name")
        self.assertEqual(updated_teacher.last_name, "new_last_name")

    def test_delete_teacher(self):
        # Création d'un nouveau professeur
        teacher = Teacher("first_name_test", "last_name_test", 99, date.today())
        teacher_id = self.teacher_dao.create(teacher)

        # On vérifie que la création a fonctionné
        self.assertNotEqual(teacher_id, 0)

        # Suppression du professeur
        result = self.teacher_dao.delete(teacher)
        self.assertTrue(result)
        deleted_teacher = self.teacher_dao.read(teacher_id)
        self.assertIsNone(deleted_teacher)

    def tearDown(self):
        with Dao.connection.cursor() as cursor:
            cursor.execute("SELECT COALESCE(MAX(id_person), 0) + 1 AS next_id FROM person")
            next_id = cursor.fetchone()["next_id"]

            cursor.execute(
                f"ALTER TABLE person AUTO_INCREMENT = {next_id}"
            )

            cursor.execute("SELECT COALESCE(MAX(id_teacher), 0) + 1 AS next_id FROM teacher")
            next_id = cursor.fetchone()["next_id"]

            cursor.execute(
                f"ALTER TABLE teacher AUTO_INCREMENT = {next_id}"
            )

        Dao.connection.commit()
