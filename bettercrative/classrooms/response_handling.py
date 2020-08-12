from bettercrative import db
from bettercrative.models import Response, Answer
"""
-------------------------------------------------------------------
Handling Responses of the User
-------------------------------------------------------------------
"""
def regular_responses(current_student,current_answer,response):

    """
    if the response is in the database:
        delete that response
    else:
        add that response to the database
    """
    print('inside regular responses')
    print(current_student)
    print(current_student.id)
    response_in_the_db = Response.query.filter_by(student_id = current_student.id,answer_reference =response.answer_reference , question_num =response.question_num).first()
    
        
    if response_in_the_db is None:
        db.session.add(response)
    else:
        db.session.delete(response_in_the_db)
        

def tf_responses(current_student,current_answer, response, current_question):
    # for answer in current_question.answers:
    """
    if the answer is in the database:
        is it identical to the current answer? (case 3)
            don't do anything
        is it different from the current answer? (case 2)
            delete this answer
            add the response
    else:
        add the response
    """
    
    for answer in current_question.answers:
    
        response_in_the_db = Response.query.filter_by(student_id = response.student_id,answer_reference =answer.id, question_num =response.question_num).first()
        print(response_in_the_db)
        if response_in_the_db is not None and response_in_the_db != response:
            print(f'deleting{response_in_the_db}')
            db.session.delete(response_in_the_db)
        else:
            print(f'adding {response}')
            db.session.add(response)
        

            

def sa_response(current_student, curernt_answer, response, current_question):
        response_in_the_db = Response.query.filter_by(student_id = current_student.id,answer_reference =response.answer_reference , question_num =response.question_num).first()

        """
        if the response is already in the db:
            edit the content of that response
        else:
            add the response
        """
        if response_in_the_db:
            response_in_the_db.value = response.value
            db.session.add(response_in_the_db)
        else:
            db.session.add(response)

