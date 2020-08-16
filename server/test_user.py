import unittest
import os
import json
from app import create_app, db

class UserTestCase(unittest.TestCase):

	def setUp(self):
		self.app = create_app(config_name="testing")
		self.client = self.app.test_client 
		self.user = {'name': 'tName', 'email': 'test@gmail.com'}
		with self.app.app_context():
			db.create_all()

	def test_user_creation(self):
		res = self.client().post('/user/', data=self.user)
		self.assertEqual(res.status_code, 201)
		self.assertIn('tName', str(res.data))

	def test_api_can_get_all(self):
		res = self.client().post('/user/', data=self.user)
		self.assertEqual(res.status_code, 201)
		res = self.client().get('/user/')
		self.assertEqual(res.status_code, 200)
		self.assertIn('tName', str(res.data))

	def test_api_can_get_user_by_id(self):
		rv = self.client().post('/user/', data=self.user)
		self.assertEqual(rv.status_code, 201)
		result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
		result = self.client().get(
			'/user/{}'.format(result_in_json['id']))
		self.assertEqual(result.status_code, 200)
		self.assertIn('tName', str(result.data))

	def test_user_can_be_edited(self):
		rv = self.client().post(
			'/user/', 
			data={'name': 'Ivan', 'email': 'ivan@gmail.com'})
		self.assertEqual(rv.status_code, 201)
		rv = self.client().put(
			'/user/1', 
			data={'name': 'Ivan Dorn'})
		self.assertEqual(rv.status_code, 200)
		results = self.client().get('/user/1')
		self.assertIn('Dorn', str(results.json))

	def test_user_deletion(self):
		rv = self.client().post(
			'/user/',
			data={'name': 'Ivan', 'email': 'ivan@gmail.com'})
		self.assertEqual(rv.status_code, 201)
		r_check = self.client().get('/user/1')
		self.assertEqual(r_check.status_code, 200)
		self.assertIn('Ivan', str(r_check.data))
		res = self.client().delete('/user/1')
		result = self.client().get('/user/1')
		self.assertEqual(result.status_code, 404)

	def tearDown(self):
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

if __name__ == '__main__':
	unittest.main()
