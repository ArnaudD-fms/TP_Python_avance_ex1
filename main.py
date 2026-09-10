#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""
from datetime import date

from business.school import School
from daos.course_dao import CourseDao
from daos.student_dao import StudentDao
from models.course import Course
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
    school.display_courses_list()


if __name__ == '__main__':
    main()
