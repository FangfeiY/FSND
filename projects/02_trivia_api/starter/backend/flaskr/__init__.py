import os
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

  #int current_cate = None
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    try:
      return jsonify({
        'success': True,
        'categories': Category.get_all()
      })
    except:
      abort(500)

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    # questions = [question.format() for question in selection]
    # paginate_questions = questions[start:end]
    # return paginate_questions

    return selection[start:end]

  @app.route('/questions')
  def get_questions_paged():
    try:
      questions = Question.query.order_by(Question.id).all()
      paged_questions = paginate_questions(request, questions)

      if len(paged_questions) == 0:
        abort(404)

      return jsonify({
            'success':True,
            'questions': paged_questions,
            'total_questions': len(questions),
            'categories': Category.get_all(),
            'current_category': None })
    except:
      abort(500)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:ques_id>', methods=['DELETE'])
  def del_question(ques_id):
    try:
      question = Question.query.get(ques_id)

      if question is None:
        abort(404)

      question.delete()

      return jsonify({
        'success': True
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    try:
      body = request.get_json()
      new_question = Question(
        question = body.get('question', None),
        answer = body.get('answer', None),
        difficulty = body.get('difficulty', None),
        category = int(body.get('category', None))
      )

      new_question.insert()

      return jsonify({
        'success': True
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def get_search_res():
    try:
      body = request.get_json()
      search_term = body.get('searchTerm')

      if search_term is not None and len(search_term) > 0:
        temp_res = Question.query.filter(Question.question.ilike(f'%{search_term}%'))
      else:
        temp_res = Question.query
      
      search_res = temp_res.order_by(Question.id).all()
      format_ques = [question.format() for question in search_res]

      return jsonify({
        'success': True,
        'questions': format_ques,
        'total_questions': len(format_ques),
        'current_category': current_cate
      })

    except:
      abort(500)
    
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:cate_id>/questions')
  def get_by_cate(cate_id):
    try:
      category = Category.query.get(cate_id)

      if category is None:
        abort(404)
      
      return jsonify({
            'success': True,
            'questions': category.questions,
            'total_questions': len(category.questions),
            'current_category': category.id})
    except:
      abort(500)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quzzies', methods=['POST'])
  def get_next_question():
    try:
      body = request.get_json()
      # previous_ques is a list of question IDs
      previous_ques = body.get('previous_questions', None)
      previous_ques = [int(ques_id) for ques_id in previous_ques]

      quiz_category = int(body.get('quiz_category', None))

      category = Category.query.get(quiz_category)

      for question in shuffle(category.questions.copy()):
        if question.id not in previous_ques:
          next_question = question
      
      return jsonify({
        'success': True,
        'question': next_question.format()
      })

    except:
      abort(422)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422

  @app.errorhandler(500)
  def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500
  
  return app

    