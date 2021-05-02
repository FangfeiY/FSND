import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.models.models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:postgres@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()

        self.new_question = {
            'question': 'What is Python?',
            'answer': 'A programming language.',
            'category': 1,
            'difficulty': 1,
        }  

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories_success(self):
        respond = self.client().get('/categories')
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
    
    def test_get_ques_page_valid(self):
        respond = self.client().get('/questions?page=1')
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_422_get_ques_page_invalid(self):
        respond = self.client().get('/questions?page=1000')
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_del_ques_success(self):
        respond = self.client().delete('/questions/2')
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_404_del_ques_not_exist(self):
        respond = self.client().delete('/questions/1000')
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_create_quest_success(self):
        respond = self.client().post('/questions', json=self.new_question)
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_ques_creation_not_allowed(self):
        respond = self.client().post('/questions/1', json=self.new_question)

        self.assertEqual(respond.status_code, 405)

    def test_search_ques_with_result(self):
        respond = self.client().post('/questions/search', json={'searchTerm':'Python'})
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 1)

    def test_search_ques_no_result(self):
        respond = self.client().post('/questions/search', json={'searchTerm':'XXXYYYZZZ'})
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)

    def test_get_ques_by_cate_success(self):
        respond = self.client().get('/categories/1/questions')
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
    
    def test_404_get_ques_by_cate_not_found(self):
        respond = self.client().get('/categories/1000/questions')
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_quiz_has_next_ques(self):
        next_ques_param = {
            'previous_questions':[],
            'quiz_category':{'type': 'Art', 'id': '2'}
        }
        respond = self.client().post('/quizzes', json=next_ques_param)
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'].get('category'), 2)

    def test_quiz_end(self):
        next_ques_param = {
            'previous_questions':['16','17','18','19'],
            'quiz_category':{'type': 'Art', 'id': '2'}
        }
        respond = self.client().post('/quizzes', json=next_ques_param)
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'] is None)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()