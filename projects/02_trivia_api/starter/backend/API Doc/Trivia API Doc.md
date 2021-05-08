# Documentation of Trivia API

## Introduction
The functions in this Trivia API server allows web app users to create trivia questions by categories, browes questions and answers, and play quizzes created by randomly drawing questions from a category.

## Getting Started
- Base URL: At this momnent this app can only run locally and doesn't have its dedicated base URL. The API server is hosted at http://127.0.0.1:5000/.
- Authentication: This API server doesn't require authentication or API keys.

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    'success': False,
    'error': 404,
    'message': 'not found'
}
```

The API will return the following types of errors should the requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Request Not Processable
- 500: Internal Server Error

## End Point Library

### GET /categories
- Purpose: Returns a list of question categories and success value.
- Sample: ```curl http://127.0.0.1:5000/categories```

```
Respond{
    'success': True,
    'categories':[
        {'1': 'Science'},
        {'2': 'Art'}
    ]
}
```

### GET /questions
- Purpose: 
    - Returns a list of question objects, a list of categories, total number of questions, and success value.
    - Returned questions are paginated in groups of 10, based on the page parameter attached to the request. The default page parameter is 1.
- Sample: ```curl http://127.0.0.1:5000/questions?page=1```

```
Respond{
    'success':True,
    'questions': [
        {
            'id': 1,
            'question': 'What is Python?',
            'answer': 'A programming language.',
            'category': 1,
            'difficulty': 1
        }
    ],
    'total_questions': 20,
    'categories': [
        {'1': 'Science'},
        {'2': 'Art'}
    ]
}
```

### DELETE /questions/{question_id}
- Purpose: Deletes the question of the given ID if it exists. Returns the success value.
- Sample: ```curl -X DELETE http://127.0.0.1:5000/questions/1```
```
Respond{
    'success': True
}
```

### POST /questions
- Purpose: Creates a new question using the submitted question description, answer, category, and difficulty. Returns the success value.
- Sample: ```curl http://127.0.0.1:5000/questions -X POST -H 'Content-Type: application/json' -d '{"question": "When was iPhone born?", "answer": "2007", "category": "1", "difficulty": "1"}' ```
```
Respond{
    'success': True
}
```

### POST /questions/search
- Purpose: Search the questions containing the submitted search term. Returns all qualifying questions, number of questions in the search results, current category, and the success value.
- Sample: ```curl http://127.0.0.1:5000/questions/search -X POST -H 'Content-Type: application/json' -d '{"searchTerm": "Python"}' ```
```
Respond{
    'success': True,
    'questions': [{
      'id': 1,
      'question': 'What is Python?',
      'answer': 'A programming language.',
      'category': 1,
      'difficulty': 1
    }],
    'total_questions': 1,
    'current_category': 1
}
```

### GET /categories/{category_id}/questions
- Purpose: Returns a list of questions of the specified category, number of questions in this category, the selected category, and the success value.
- Sample: ```curl http://127.0.0.1:5000/categories/1/questions```
```
Respond{
    'success': True,
    'questions': [{
        'id': 1,
        'question': 'What is Python?',
        'answer': 'A programming language.',
        'category': 1,
        'difficulty': 1
    }],
    'total_questions': 1,
    'current_category': 1
}
```

### POST /quizzes
- Purpose: 
    - Gets questions of the specified category to play the quiz.
    - Takes 2 parameters from the request body: the category and a list of IDs of the questions that are already shown
    - Returns a random question within the given category, and that is not one of the previous questions.
    - Returns null to indicate the end of the quiz in the following circumstances: 1)Users have played five questions of the chosen category; 2) There are fewer than five questions in the category.
- Sample: ```curl http://127.0.0.1:5000/quizzes -X POST -H 'Content-Type: application/json' -d '{"previous_questions": [1, 2, 3], "quiz_category": {"type": "Science", "id": 1}}' ```
```
Respond{
    'success': True,
    'question': {
        'id': 1,
        'question': 'What is Python?',
        'answer': 'A programming language.',
        'category': 1,
        'difficulty': 1
    }
}
```


