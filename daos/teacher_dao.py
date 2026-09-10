# -*- coding: utf-8 -*-

"""
Classe Dao[Student]
"""
import pymysql

from dataclasses import dataclass
from typing import Optional
from daos.dao import Dao
from models.teacher import Teacher


@dataclass
class TeacherDao(Dao[Teacher]):

    def create(self, teacher: Teacher) -> int:
        """ Créer en BD l'entité Teacher correspondant au professeur

        :param teacher: à créer sous forme d'entité Teacher en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = """
                    INSERT INTO person (first_name, last_name, age)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (teacher.first_name, teacher.last_name, teacher.age))
                id_person = cursor.lastrowid
                sql = """
                    INSERT INTO teacher (hiring_date, id_person) 
                    VALUES (%s, %s)
                """
                cursor.execute(sql, (teacher.hiring_date, id_person))
                teacher_id = cursor.lastrowid
                teacher.id = teacher_id

            Dao.connection.commit()

            return teacher_id

        except pymysql.MySQLError as e:
            Dao.connection.rollback()
            print(f"Erreur SQL : {e}")
            return 0

    def read(self, id_teacher: int) -> Optional[Teacher]:
        """ Renvoie le professeur correspondant à l'entité dont l'id est id_teacher
           (ou None s'il n'a pu être trouvé)"""
        teacher: Optional[Teacher]
        with Dao.connection.cursor() as cursor:
            sql = """
                SELECT * 
                FROM teacher 
                JOIN person ON teacher.id_person = person.id_person
                WHERE id_teacher = %s
            """
            cursor.execute(sql, id_teacher)
            record = cursor.fetchone()
            if record is not None:
                teacher = Teacher(record['first_name'], record['last_name'], record['age'], record['hiring_date'])
                teacher.id = record['id_teacher']
            else:
                teacher = None

        return teacher

    def update(self, teacher: Teacher) -> bool:
        """Met à jour en BD l'entité Teacher correspondant au teacher en paramètre

        :param teacher: le professeur mis à jour
        :return: True si la mise à jour a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            sql = """
                UPDATE person
                JOIN teacher ON teacher.id_person = person.id_person
                SET person.first_name = %s, person.last_name = %s, person.age = %s, teacher.hiring_date = %s
                WHERE teacher.id_teacher = %s
            """
            cursor.execute(sql, (
                teacher.first_name,
                teacher.last_name,
                teacher.age,
                teacher.hiring_date,
                teacher.id
            ))
            result = cursor.rowcount > 0
        Dao.connection.commit()

        return result

    def delete(self, teacher: Teacher) -> bool:
        """Supprime en BD l'entité Teacher correspondant à teacher

        :param teacher: le professeur dont l'entité Teacher correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                # Récupération de la personne associée au professeur
                sql = """
                    SELECT id_person FROM teacher WHERE id_teacher = %s
                """
                cursor.execute(sql, teacher.id)
                record = cursor.fetchone()

                if record is None:
                    return False

                id_person = record['id_person']

                # Suppression du professeur
                sql = """
                DELETE FROM teacher WHERE id_teacher = %s
                """
                cursor.execute(sql, teacher.id)

                # Suppression de la personne
                sql = """
                DELETE FROM person WHERE id_person = %s"""
                cursor.execute(sql, id_person)

            Dao.connection.commit()
            return True

        except pymysql.MySQLError:
            Dao.connection.rollback()
            return False
