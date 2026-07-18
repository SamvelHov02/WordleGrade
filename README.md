# WordleGrade

WordleGrade is a project that uses expected information gain to grade a game of Wordle. This project was inspired by the 3Blue1Brown video series however this project is far simpler e.g. WordleGrade assumes that the distribution of the wordle words as the answer is uniform.

## Grading

As mentioned before `WordleGrade` uses average of the expected information gain from the guesses to grade a game this means that it is feasible that a game of length 6 gives a better grade than one where the player guesses the word on the second attempt. This might seem wrong to some, but it's seems reasonable if you accept what `WordleGrade` actually does is not game specific but rather more general. In the future there might be a version that supports other metrics e.g. actual information gain of the guess.

Another thing to know is that the first guess of a game isn't considered in the grading. The goal of this detail is to make the game less "robotic", at the start of the game the player has 0 information and therefore no real oppurtunity to make a "good" guess therefore it's ignored.

## How to run

TODO
