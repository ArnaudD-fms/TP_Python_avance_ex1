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

    student = Student("Jean", "Dupont", 20)

    student_dao: StudentDao = StudentDao()

    result = student_dao.create(student)

    print(result)

    # print(school.get_course_by_id(1))
    # print(school.get_course_by_id(2))
    # print(school.get_course_by_id(9))


if __name__ == '__main__':
    main()
