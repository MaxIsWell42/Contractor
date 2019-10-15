# tests.py

from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId

sample_product_id = ObjectId('5da4caf7a65948f80902765c')
sample_product = {
    "_id": {
        "$oid": "5da4caf7a65948f80902765c"
    },
    "title": "Skateboard",
    "price": "115",
    "description": "A simple skateboard, complete build.",
    "created_at": {
        "$date": "2019-10-14T12:22:31.974Z"
    },
    "reviews": "Description is accurate, image is just deck tho 4/5 could be better",
    "image": "https://scene7.zumiez.com/is/image/zumiez/pdp_hero/RIPNDIP-Lord-Nermal-Silver-8.0%22--Skateboard-Deck-_256865.jpg"
    }



sample_form_data = {
    'title': sample_product['title'],
    'description': sample_product['description'],
    'image': sample_product['image']
    
}

class productsTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the products homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'product', result.data)

    def test_new(self):
        """Test the new product creation page."""
        result = self.client.get('/products/new')
        self.assertEqual(result.status, '200 OK')

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_product(self, mock_find):
        """Test showing a single product."""
        mock_find.return_value = sample_product

        result = self.client.get(f'/products/{sample_product_id}')
        self.assertEqual(result.status, '200 OK')

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_product(self, mock_find):
        """Test editing a single product."""
        mock_find.return_value = sample_product

        result = self.client.get(f'/products/{sample_product_id}/edit')
        self.assertEqual(result.status, '200 OK')

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_product(self, mock_insert):
        """Test submitting a new product."""
        result = self.client.post('/product', data=sample_form_data)

        # After submitting, should redirect to that product's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_product)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_product(self, mock_update):
        result = self.client.post(f'/products/{sample_product_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_product_id}, {'$set': sample_product})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_product(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/products/{sample_product_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_product_id})

if __name__ == '__main__':
    unittest_main()