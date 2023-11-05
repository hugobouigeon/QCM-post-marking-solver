# QCM solver

This code provides tools to find the answers of a quiz given student scores and answer-sheets.
It uses a statistical approach combined with an evolutionary algorithm.

## Assumptions

I assume the following :
- quizzes have N questions (by default N = 120)
- Each question has n different possible solutions (by default, n=4)
- Each question has a unique answer
- there are m students partaking in the quiz (by default, m = 100)
- Students have a given probability to know an answer, and answer at random if they don't. (by default, a student knows 25% of the answers). "inteligence" is spread among students following a gaussian distribution.

## How to use

All usefull functions can be found in the utils folder.

Simulation functions create a fictional dataset to work with, as I had no first hand data. Some functions take into account wether stundents know some of the answers or not (get_answer_matrix_assuming_smart).

Inference functions make predictions on what the actual answers are. They only require student scores and answers to run and in no case reuse the ground truth data. Inference is done by giving scores to each possible answer of each question depending on each students score (if a student has good scores, his answers are given a higher value, if he has low scores, his answers are given a lower value). I made two visuals as gifs of this process.

Evaluation and visualization functions can be used to evaluate predictions.

Correction functions are an essential part of the algorithm. Predictions made by he algorithms mentioned above can have some errors. The correction function try_changes tweeks the initial guess make it match with student scores / answer sheets. It implements a basic evolutionary algorithm that tries to find the right answer. This usualy works as long as the initial guess is almost correct (only a few questions have wrong answers associated to them). Given anough students which are answering at random, this step may not be necessary.

The draft.ipynb contains all of these functions and some variants which may improve some of the results. Code can be executed there.

## Insights

The more students there are, the better this algorithm works. The smarter students are the better this algorithm works.

Given 70 students knowin on average 25% of answers, the combined algorithm finds the correct answer 20 out of 20 times.

The algorithm runs within a few seconds (gets slower with the mmount of student answers).

## Visual

![Alt text](<solver gif 1.gif>)
![Alt text](<solver gif 2.gif>)

## Contributors

Hugo Bouigeon 