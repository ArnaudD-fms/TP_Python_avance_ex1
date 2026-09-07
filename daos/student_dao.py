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
        """Crée en BD l'entité Student correspondant aux élèves

        :param student: à créer sous forme d'entité Student en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        with Dao.connection.cursor() as cursor:
            sql = "INSERT INTO person (first_name, last_name, age) VALUES (%s, %s, %s)"
            cursor.execute(sql, (student.first_name, student.last_name, student.age))
            id_person = cursor.lastrowid
            sql = "INSERT INTO student (student_nbr, id_person) VALUES (%s, %s)"
            cursor.execute(sql, (student.student_nbr, id_person))

        Dao.connection.commit()

        return student.student_nbr

    def read(self, id_entity: int) -> Optional[Student]:
        ...

    def update(self, student: Student) -> bool:
        ...
        return True

    def delete(self, student: Student) -> bool:
        """delete"""
        ...
        return True

