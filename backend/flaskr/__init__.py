import os
import sys
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''

    CORS(app, resources=r'*')

    '''
    @DONE: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def header_Set(request):
        headers = request.headers
        headers['Access-Control-Allow-Origin'] = "*"
        return request

    '''
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    '''

    @app.route('/categories')
    def get_all_categories():
            all_categories = Category.query.all()
            sorted_categories = {}

            for category in all_categories:
                sorted_categories[category.id] = category.type

            if (len(sorted_categories) == 0):
                abort(404)

            return jsonify({
                'success': True,
                'categories': sorted_categories
            })

    '''
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    @app.route('/questions')
    def get_questions():
            current_page = int(request.args.get('page'))

            start = (current_page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE

            all_questions = list(map(Question.format, Question.query.all()))
            total_questions = len(all_questions)
            current_question_set = all_questions[start:end]

            all_categories = Category.query.all()
            sorted_categories = {}

            for category in all_categories:
                sorted_categories[category.id] = category.type

            # return data to view
            return jsonify({
                'success': True,
                'questions': current_question_set,
                'total_questions': len(all_questions),
                'categories': sorted_categories
              })

    '''
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route("/questions/<question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        
        if question:
          Question.delete(question)
          return jsonify({
              "success": True
          })

    '''
    @DONE: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route("/questions", methods=["POST"])
    def create_question():
        if request.data:
            new_question = json.loads(request.data)
            if ((new_question["question"] and new_question["answer"] and new_question["difficulty"] and new_question["category"])):
                question = Question(
                      question=new_question['question'],
                      answer=new_question['answer'],
                      difficulty=new_question['difficulty'],
                      category=new_question['category']
                )
                Question.insert(question)
                return jsonify({
                    "success": True
                })
            abort(404)
        abort(422)

    '''
    @DONE: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route("/searchQuestions", methods=["POST"])
    def find_questions():
          if request.data:
                page = 1
                query = json.loads(request.data)
                if query["searchTerm"]:
                      db_query = Question.query.filter(
                        Question.question.like(
                          "%" + query["searchTerm"] + "%"
                        )
                      )

                      start = (page - 1) * QUESTIONS_PER_PAGE
                      end = start + QUESTIONS_PER_PAGE
                      results = list(map(Question.format, db_query.all()))
                      current_result_set = results[start:end]

                      if len(results) > 0:
                            return jsonify({
                              "success": True,
                              "questions": current_result_set,
                              "total_questions": len(results),
                              "category": None
                            })
                abort(404)
          abort(422)        


    '''
    @DONE: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route("/categories/<int:category_id>/questions")
    def return_questions_from_category(category_id):
          category = Category.query.get(category_id)
          if request.args.get('page'):
                page = int(request.args.get('page'))
          else:
                page = 1
          all_category_questions = Question.query.filter_by(
            category=category_id
          )
          questions = list(map(Question.format, all_category_questions.all()))
          start = (page - 1) * QUESTIONS_PER_PAGE
          end = start + QUESTIONS_PER_PAGE
          current_question_set = questions[start:end]

          if len(current_question_set) > 0:
                return jsonify({
                  "success": True,
                  "questions": current_question_set,
                  "total_questions": len(questions),
                  "category": Category.format(category)
                })
          abort(404)

    '''
    @DONE: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.route("/quizzes", methods=["POST"])
    def start_quiz():
          if request.data:
                quiz_data = json.loads(request.data)

                if (('quiz_category' in quiz_data
                 and 'id' in quiz_data['quiz_category'])
                    and 'previous_questions' in quiz_data):

                      if quiz_data['quiz_category']['id'] == 0:
                            quiz_data['quiz_category']['id'] = random.randint(1, 6)
                            
                      query = Question.query.filter_by(
                        category=quiz_data["quiz_category"]["id"]
                      ).filter(
                        Question.id.notin_(quiz_data['previous_questions'])
                      ).all()

                      if len(query) > 0:
                            return jsonify({
                              "success": True,
                              "question": Question.format(
                                query[random.randrange(0, len(query))]
                              )
                            })
                      else:
                            return jsonify({
                              "success": True,
                              "question": None
                            })
                abort(404)
          abort(422)
                          

    '''
    @DONE: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(404)
    def not_found(error):
        error_data = {
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }
        return jsonify(error_data), 404

    @app.errorhandler(422)
    def unprocessable(error):
        error_data = {
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }
        return jsonify(error_data), 422
    return app
