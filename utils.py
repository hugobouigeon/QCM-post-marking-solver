import numpy as np
import matplotlib.pyplot as plt

class Constant:
    n_questions = 120
    n_answers = 4
    n_students = 100
    max_correction_epochs= 10

#simulation

def get_answer_sheet():
    return np.random.randint(0, Constant.n_answers, Constant.n_questions)

def get_student_answer_sheet():
    return np.random.randint(0, Constant.n_answers, Constant.n_questions)

def get_answer_matrix():
    answer_matrix = np.zeros((Constant.n_students, Constant.n_questions),dtype=np.int8)
    for i in range(Constant.n_students):
        answer_matrix[i] = get_student_answer_sheet()
    return answer_matrix

def get_student_answer_sheet_assuming_smart(smartness: float, answers):     # assuming students know some of the answers 
    student_answers = np.zeros(Constant.n_questions,dtype=np.int8)
    for i in range(Constant.n_questions):
        if np.random.rand() < smartness:
            student_answers[i] = answers[i]
        else:
            student_answers[i] = np.random.randint(0, Constant.n_answers)
    return student_answers

def get_answer_matrix_assuming_smart(answers, average_smartness:float = 0.6, smartness_std:float = 0.2):
    answer_matrix = np.zeros((Constant.n_students, Constant.n_questions),dtype=np.int8)
    for i in range(Constant.n_students):
        smartness = np.random.normal(average_smartness, smartness_std)
        smartness = max(0.02, min(0.98, smartness))
        answer_matrix[i] = get_student_answer_sheet_assuming_smart(smartness, answers)
    return answer_matrix

def get_student_score(student_answers, answer_sheet):
    return np.sum(student_answers == answer_sheet)

def get_score_list(answer_matrix, answer_sheet):
    score_list = np.zeros(Constant.n_students)
    for i in range(Constant.n_students):
        score_list[i] = get_student_score(answer_matrix[i], answer_sheet)/Constant.n_questions
    return score_list

#inference

def get_probability_matrix(score_list, answer_matrix):
    """
    gives a probability for each answer to each question to be the correct one.
    """
    probability_matrix = np.zeros((Constant.n_questions, Constant.n_answers))
    for i in range(Constant.n_questions):
        for j in range(Constant.n_answers):
            for k in range(Constant.n_students):
                probability_matrix[i, j] += score_list[k] * (answer_matrix[k, i] == j) + (1-score_list[k]) * (answer_matrix[k, i] != j) / (Constant.n_answers - 1)
    return probability_matrix

def get_argmaxes(probability_matrix):
    """
    argmaxes are most likely answers. this returns a prediction.
    """
    argmaxes = np.zeros(Constant.n_questions)
    for i in range(Constant.n_questions):
        argmaxes[i] = np.argmax(probability_matrix[i])
    argmaxes = np.array(argmaxes, dtype=int)
    return argmaxes

# evaluation

def evaluate(prediction,groud_truth):
    return np.sum(prediction == groud_truth)/Constant.n_questions

# visualization

def show_answers(sheet):
    sheet_matrix = np.zeros((Constant.n_questions, Constant.n_answers))
    for i in range(Constant.n_questions):
        sheet_matrix[i, sheet[i]] = 1
    plt.imshow(sheet_matrix, cmap='gray')

def compare_sheets(predictions, groud_truth):
    plt.figure(figsize=(4,10))
    plt.subplot(1,3,1)
    plt.title("predictions")
    show_answers(predictions)
    plt.subplot(1,3,2)
    plt.title("groud_truth")
    show_answers(groud_truth)
    plt.subplot(1,3,3)
    plt.title('Correct')
    comparison = predictions == groud_truth
    comparison = comparison.reshape((-1,1))
    plt.imshow(comparison, cmap='RdYlGn')
    plt.show()

# Correction

def get_validity_distance_list(predictions, score_list, answer_matrix):
    """
    finds for each student the difference between there score and the score they would have according to prediction.
    """
    validity_list = np.zeros(Constant.n_students,dtype=int)
    for i in range(Constant.n_students):
        student_answers = answer_matrix[i]
        validity_list[i] = round(abs(get_student_score(student_answers, predictions)/Constant.n_questions - score_list[i]) * Constant.n_questions,0)
    return validity_list

def try_changes(predictions, score_list, answer_matrix):
    """
    evolutionary algorithm to get a better prediction.
    """
    start_distance = np.sum(get_validity_distance_list(predictions, score_list, answer_matrix))
    print("start_distance: ", start_distance)
    for epoch in range(Constant.max_correction_epochs):
        for i in range(Constant.n_questions):
            backup = predictions[i]
            distance_changed = False
            for j in range(Constant.n_answers):
                predictions[i] = j
                distance = np.sum(get_validity_distance_list(predictions, score_list, answer_matrix))
                if distance < start_distance:
                    start_distance = distance
                    distance_changed = True
                    print("distance: ", distance)
                    break
                else:
                    predictions[i] = (j+1)%Constant.n_answers
            if not distance_changed:
                predictions[i] = backup
            elif start_distance == 0:
                return predictions
    return predictions

def get_uncertainty_priority_list(probability_matrix):
    stdlist = [[0,i] for i in range(Constant.n_questions)]
    for i in range(Constant.n_questions):
        stdlist[i][0] = np.std(probability_matrix[i])
    stdlist.sort()
    priority_list = [x[1] for x in stdlist]
    return priority_list

def try_changes_with_priority_to_least_known_answers(predictions, score_list, answer_matrix, priority_list):
    """
    Slightly improved evolutionary algorithm to get a better prediction.
    Tries to make changes on questions where the initial guess was least confident (low std between scores for answers).
    """
    start_distance = np.sum(get_validity_distance_list(predictions, score_list, answer_matrix))
    for epoch in range(Constant.max_correction_epochs):
        for i in priority_list:
            backup = predictions[i]
            distance_changed = False
            for j in range(Constant.n_answers):
                predictions[i] = j
                distance = np.sum(get_validity_distance_list(predictions, score_list, answer_matrix))
                if distance < start_distance:
                    start_distance = distance
                    distance_changed = True
                    break
                else:
                    predictions[i] = (j+1)%Constant.n_answers
            if not distance_changed:
                predictions[i] = backup
            elif start_distance == 0:
                return predictions
    return predictions