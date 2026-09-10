# -*- coding: utf-8 -*-

"""
Classe Dao[Address]
"""

import pymysql

from dataclasses import dataclass
from typing import Optional
from daos.dao import Dao
from models.address import Address


@dataclass
class AddressDao(Dao[Address]):

    def create(self, address: Address) -> int:
        """Crée en BD l'entité Address correspondant à l'adresse

        :param address: à créer sous forme d'entité Address en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = """
                INSERT INTO address(street, city, postal_code) 
                VALUES(%s, %s, %s)
                """
                cursor.execute(sql, (address.street, address.city, address.postal_code))
                address_id: int = cursor.lastrowid
                address.id = address_id

            Dao.connection.commit()
            return address_id

        except pymysql.MySQLError as e:
            Dao.connection.rollback()
            print(f"Erreur SQL : {e}")
            return 0

    def read(self, id_address: int) -> Optional[Address]:
        """Renvoie l'adresse correspondante à l'entité dont l'id est id_address
           (ou None s'il n'a pu être trouvé)"""
        address: Optional[Address]

        with Dao.connection.cursor() as cursor:
            sql = """
                SELECT * FROM address  WHERE id_address = %s
            """
            cursor.execute(sql, id_address)
            record = cursor.fetchone()
            if record is not None:
                address = Address(record['street'], record['city'], record['postal_code'])
                address.id = record['id_address']
            else:
                address = None

        return address

    def update(self, address: Address) -> bool:
        """Met à jour en BD l'entité Address correspondant à address

        :param address: adresse mise à jour
        :return: True si la mise à jour a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            sql = """
                UPDATE address 
                SET street=%s, city=%s, postal_code=%s
                WHERE id_address = %s
            """
            cursor.execute(sql, (address.street, address.city, address.postal_code, address.id))
            result = cursor.rowcount > 0

        Dao.connection.commit()
        return result

    def delete(self, address: Address) -> bool:
        """Supprime en BD l'entité Address correspondant à address

        :param address: adresse dont l'entité Address correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            sql = """
                DELETE FROM address WHERE id_address = %s
            """
            cursor.execute(sql, (address.id,))
            result = cursor.rowcount > 0

        Dao.connection.commit()

        return result
