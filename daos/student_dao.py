# -*- coding: utf-8 -*-

"""
Classe Dao[Student]
"""
from typing import Optional

from models.student import Student
from daos.dao import Dao
from dataclasses import dataclass


@dataclass
class StudentDao(Dao[Student]):
    def create(self, student: Student) -> int:
        """ Créer en BD l'entité Student correspondant aux élèves

        :param student: à créer sous forme d'entité Student en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        with Dao.connection.cursor() as cursor:
            sql = """
                INSERT INTO person (first_name, last_name, age)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (student.first_name, student.last_name, student.age))
            id_person = cursor.lastrowid
            sql = "INSERT INTO student (student_nbr, id_person) VALUES (%s, %s)"
            cursor.execute(sql, (student.student_nbr, id_person))

        Dao.connection.commit()

        return student.student_nbr

    def read(self, id_student: int) -> Optional[Student]:
        """ Renvoie l'élève correspondant à l'entité dont l'id est id_student
           (ou None s'il n'a pu être trouvé)"""
        student: Optional[Student]

        with Dao.connection.cursor() as cursor:
            sql = """
                SELECT *
                FROM student
                JOIN person ON student.student_nbr = person.id_person
                WHERE student_nbr = %s
            """
            cursor.execute(sql, (id_student,))
            record = cursor.fetchone()
        if record is not None:
            student = Student(record['first_name'], record['last_name'], record['age'])
            student.student_nbr = record['student_nbr']
        else:
            student = None

        return student

    def update(self, student: Student) -> bool:
        """Met à jour en BD l'entité Student correspondant au student en paramètre

        :param student: l'élève à mettre à jour
        :return: True si la mise à jour a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            sql = """
                UPDATE person
                JOIN student ON student.id_person = person.id_person
                SET person.first_name = %s, person.last_name = %s, person.age = %s
                WHERE student.student_nbr = %s
            """
            cursor.execute(sql, (student.first_name, student.last_name, student.age, student.student_nbr))
            Dao.connection.commit()

        # retourne true si une ligne a été update
        return cursor.rowcount > 0

    def delete(self, student: Student) -> bool:
        with Dao.connection.cursor() as cursor:
            # Récupération de la personne associée à l'étudiant
            sql = """
                SELECT id_person FROM student WHERE student_nbr = %s
            """
            cursor.execute(sql, (student.student_nbr,))
            record = cursor.fetchone()

            if record is None:
                return False

            id_person = record['id_person']

            # Suppression de l'étudiant
            sql = """
            DELETE FROM student WHERE student_nbr = %s
            """
            cursor.execute(sql, (student.student_nbr,))

            # 
            sql = """
            DELETE FROM person WHERE id_person = %s"""
            cursor.execute(sql, (id_person,))

            Dao.connection.commit()

        return True

