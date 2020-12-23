

def get_alphabet_index(index):
    alpha = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    s = ""
    quotient = index
    while quotient > 26:
        remainder = int(quotient % 26)
        # Takes care of edge case when rightmost letter is Z
        if remainder == 0:
            quotient -= 26
        s += alpha[remainder - 1]
        quotient = int(quotient / 26)
    s += alpha[quotient - 1]
    return s[::-1]


def append_form(form):
    form.answer_form.append_entry()


def find_selected_answer(question_category, answer_response, answer_id, student_id):
    
    if question_category != 'Short Answer' and question_category != 'IDE':
        for response in answer_response:
            if response.student_id == student_id and response.answer_reference == answer_id:
                return True
        
        return False
    else:
        for response in answer_response:
            if response.student_id == student_id and response.answer_reference == answer_id:
                return response.value
        return ""


def check_is_complete(quiz):
    if quiz.questions:
        for question in quiz.questions:
            if not question.content:
                return False
            if question.type == 'Multiple Choice':
                if not question.answers:
                    return False
                has_correct_answer = False
                for answer in question.answers:
                    if not answer.content:
                        return False
                    if answer.correct:
                        has_correct_answer = True
                if not has_correct_answer:
                    return False
    return True

