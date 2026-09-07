#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""

from business.school import School
from daos.student_dao import StudentDao
from models.student import Student


def main() -> None:
    """Programme principal."""
    print("""\
--------------------------
Bienvenue dans notre école
--------------------------""")

    school: School = School()

    # initialisation d'un ensemble de cours, enseignants et élèves composant l'école
    school.init_static()

    # affichage de la liste des cours, leur enseignant et leurs élèves
    # school.display_courses_list()

    student_dao: StudentDao = StudentDao()

    # student = Student("Jean", "Dupont", 20)
    # student_dao.create(student)

    # student = Student("Marc", "Dupont", 25)
    # student_dao.update(student)

    student = student_dao.read(4)
    print(student)
    student_dao.delete(student)

    # print(school.get_course_by_id(1))
    # print(school.get_course_by_id(2))
    # print(school.get_course_by_id(9))


if __name__ == '__main__':
    main()
