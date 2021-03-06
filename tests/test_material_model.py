from odoo.tests.common import SavepointCase
from odoo.exceptions import ValidationError
from odoo.tests import tagged

@tagged('post_install', '-at_install', 'ns_material')
class NusantechMaterialTestCase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(NusantechMaterialTestCase,cls).setUpClass()

        related_supplier_vals = {
            'name': 'Test Supplier',
            'is_company': True,
            'email': 'test@test.com',
        }
        cls.related_supplier_id = cls.env['res.partner'].create(related_supplier_vals).id
        #cls.currency_id = cls.env['res.currency'].search([('name','=','IDR')]).id
        cls.currency_id = 1
        material_vals = {
            'material_code' : "C999",
            'material_name': "Cotton Grade 999",
            'material_type': "C",
            'material_buy_price': "100000",
            'currency_id': cls.currency_id,
            'related_supplier_id': cls.related_supplier_id,
        }
        cls.material = cls.env['ns_material.material'].create(material_vals)
        

    def test_material_created_on_create(self):
        # TEST CASE
        """ 
        Check if a material record  created after creating a material
        """
        # ARRANGE
        material = self.env['ns_material.material'].search([
            ('material_code', '=', 'C999')
        ], limit=1)

        # ASSERT
        self.assertEqual(
            material.material_name, 'Cotton Grade 999', 'No material record after material creation')

    def test_material_updated_on_update(self):
        # TEST CASE
        """ 
        Check if a material record updated after updating a material
        """
        # ARRANGE
        material = self.env['ns_material.material'].search([
            ('material_code', '=', 'C999')
        ], limit=1)

        #ACT
        material.update(
            {'material_name': 'Cotton Grade 999 Updated'}
            )

        material = self.env['ns_material.material'].search([
            ('material_code', '=', 'C999')
        ], limit=1)

        # ASSERT
        self.assertEqual(
            material.material_name, 'Cotton Grade 999 Updated', 'Material record not updated after material update')
    
    def test_material_create_invalid_buy_price_raise(self):
        # TEST CASE
        """
        Check if the error occurs when trying to create material with buy price less than 100.
        """
        # NO ARRANGE
        # ACT & ASSERT
        with self.assertRaises(
            ValidationError,
            msg="Field Material Buy Price can't be less than 100",
        ):
            material = self.env["ns_material.material"].create(
                {
                    'material_code' : "C900",
                    'material_name': "Cotton Grade 900",
                    'material_type': "C",
                    'material_buy_price': "50",
                    'currency_id': self.currency_id,
                    'related_supplier_id': self.related_supplier_id,
                }
            )
    
    def test_material_update_invalid_buy_price_raise(self):
        # TEST CASE
        """
        Check if the error occurs when trying to update material with buy price less than 100.
        """
        # NO ARRANGE
        # ACT & ASSERT
        with self.assertRaises(
            ValidationError,
            msg="Field Material Buy Price can't be less than 100",
        ):
            self.material.update({'material_buy_price': "50"})
