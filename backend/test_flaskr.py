import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    DONE
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_return_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)

    def test_404_no_categories(self):
        res = self.client().get('/categories/4')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')    


    def test_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions']) 
        self.assertTrue(len(data['questions']))
        self.assertEqual(len(data['categories']), 6)

    def test_404_bad_paginated_request(self):
        res = self.client().get('/questions?page=24')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_question(self):
        res = self.client().delete('/questions/14')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 14).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)

    def test_422_bad_question_request(self):
        res = self.client().delete('/questions/890')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')     

    def add_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_if_missing_requested_arguments(self):
        res = self.client().post('/questions', json=self.new_question_incomplete)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')    


    def test_405_if_question_creation_is_not_allowed(self):    
        res = self.client().post('/questions/45', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')   

    def test_422_if_data_does_not_exist(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')            

    def test_search_questions_with_results(self):
        res = self.client().post('/searchQuestions', json={'searchTerm':'art'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions']) 
        self.assertEqual(data['total_questions'], 2)

    def test_query_no_results(self):
        res = self.client().post('/searchQuestions', json={'searchTerm':'astrerytiibmddsn'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['questions'], [])    
        self.assertEqual(data['total_questions'], 0)    

    def test_404_if_missing_query(self):
        res = self.client().post('/searchQuestions', json={'searchTerm':''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')    


    def test_405_if_method_is_not_allowed(self):    
        res = self.client().post('/categories',  json={'searchTerm':'art'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')   

    def test_422_if_bad_query(self):
        res = self.client().post('/searchQuestions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')     

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_no_avail_questions_or_categories(self):
        res = self.client().get('/categories/9/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')
   

    def test_get_random_quiz_question(self):
        res = self.client().post('/quizzes', json={'quiz_category':{'type':'Science', 'id':1}, 'previous_questions':[20,21]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['answer'], 'Blood')

    def test_get_empty_quiz_question(self):
        res = self.client().post('/quizzes', json={'quiz_category':{'type':'Science', 'id':1}, 'previous_questions':[20,21,22]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], None)           

    def test_404_if_bad_trivia_request(self):
        res = self.client().post('/quizzes', json={'quiz_category':{}, 'previous_questions':[20,21]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')    


    def test_405_if_this_method_is_not_allowed(self):    
        res = self.client().post('/categories', json={'quiz_category':{'type':'Science', 'id':1}, 'previous_questions':[20,21]})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')   

    def test_422_if_previous_data_does_not_exist(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()