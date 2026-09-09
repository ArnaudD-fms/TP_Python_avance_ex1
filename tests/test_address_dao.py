import unittest

from daos.address_dao import AddressDao
from daos.dao import Dao
from models.address import Address


class TestAdressDao(unittest.TestCase):

    def setUp(self):
        self.address_dao = AddressDao()

    def test_read_existing_address(self):
        address = self.address_dao.read(1)

        self.assertIsNotNone(address)
        self.assertIsInstance(address, Address)
        self.assertEqual(address.id, 1)
        self.assertEqual(address.street, "12 rue des Pinsons")
        self.assertEqual(address.city, "Castanet")
        self.assertEqual(address.postal_code, 31320)

    def test_read_non_existing_address(self):
        address = self.address_dao.read(999999)
        self.assertIsNone(address)

    def test_create_address(self):
        address = Address("street_test", "city_test", 11111)

        result = self.address_dao.create(address)

        self.assertNotEqual(result, 0)
        self.assertIsNotNone(address.id)
        self.assertEqual(result, address.id)

    def test_update_address(self):
        # Création d'une nouvelle adresse
        address = Address("street_test", "city_test", 11111)
        address_id = self.address_dao.create(address)

        # On vérifie que la création a fonctionné
        self.assertNotEqual(address_id, 0)

        # On modifie l'objet address
        address.street = "new_street_test"
        address.city = "new_city_test"
        address.postal_code = 22222

        # On vérifie que l'update a fonctionné
        result = self.address_dao.update(address)
        self.assertTrue(result)

        # On vérifie que la ligne en base a bien été modifié
        updated_address = self.address_dao.read(address_id)
        self.assertEqual(updated_address.street, "new_street_test")
        self.assertEqual(updated_address.city, "new_city_test")
        self.assertEqual(updated_address.postal_code, 22222)

    def test_delete_address(self):
        # Création d'une nouvelle adresse
        address = Address("street_test", "city_test", 11111)
        address_id = self.address_dao.create(address)

        # On vérifie que la création a fonctionné
        self.assertNotEqual(address_id, 0)

        # Suppression du cours
        result = self.address_dao.delete(address)
        self.assertTrue(result)
        deleted_course = self.address_dao.read(address_id)
        self.assertIsNone(deleted_course)

    def tearDown(self):
        with Dao.connection.cursor() as cursor:
            cursor.execute("SELECT COALESCE(MAX(id_address), 0) + 1 AS next_id FROM address")
            next_id = cursor.fetchone()["next_id"]

            cursor.execute(
                f"ALTER TABLE address AUTO_INCREMENT = {next_id}"
            )

        Dao.connection.commit()

    if __name__ == '__main__':
        unittest.main()


