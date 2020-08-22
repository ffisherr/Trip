import unittest
import os
import json
from app import create_app, db

class TripTestCase(unittest.TestCase):

	def setUp(self):
		self.app = create_app(config_name="testing")
		self.client = self.app.test_client 
		self.trip = {'name': 'tName', 'description': 'test trip',
			'date_starts': '10-10-2020 10:00', 'date_ends': '20-10-2020 10:00',
			'owner': '1'}
		with self.app.app_context():
			db.create_all()

	def test_trip_creation(self):
		res = self.client().post('/trip/', data=self.trip)
		self.assertEqual(res.status_code, 201)
		self.assertIn('tName', str(res.data))

	def test_api_can_get_all(self):
		res = self.client().post('/trip/', data=self.trip)
		self.assertEqual(res.status_code, 201)
		res = self.client().get('/trip/')
		self.assertEqual(res.status_code, 200)
		self.assertIn('tName', str(res.data))

	def test_api_can_get_trip_by_id(self):
		rv = self.client().post('/trip/', data=self.trip)
		self.assertEqual(rv.status_code, 201)
		result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
		result = self.client().get(
			'/trip/{}'.format(result_in_json['id']))
		self.assertEqual(result.status_code, 200)
		self.assertIn('tName', str(result.data))

	def test_trip_can_be_edited(self):
		rv = self.client().post(
			'/trip/', 
			data={'name': 'ttt ', 'description': 'some',
			'date_starts': '10-10-2020 10:00', 'date_ends': '20-10-2020 10:00',
			'owner': '1'})
		self.assertEqual(rv.status_code, 201)
		rv = self.client().put(
			'/trip/1', 
			data={'name': 'some other name','date_starts': '10-10-2020 10:00', 'date_ends': '20-10-2020 10:00', 'description': 'sss'})
		self.assertEqual(rv.status_code, 200)
		results = self.client().get('/trip/1')
		self.assertIn('other', str(results.json))

	def test_trip_deletion(self):
		rv = self.client().post(
			'/trip/',
			data=self.trip)
		self.assertEqual(rv.status_code, 201)
		r_check = self.client().get('/trip/1')
		self.assertEqual(r_check.status_code, 200)
		self.assertIn('tName', str(r_check.data))
		res = self.client().delete('/trip/1')
		result = self.client().get('/trip/1')
		self.assertEqual(result.status_code, 404)
		
	def tearDown(self):
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

if __name__ == '__main__':
	unittest.main()
