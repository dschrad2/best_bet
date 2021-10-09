// Import questions from questions.js
import { questions } from "/static/questions.js";

// Set buttons to move through game
const startButton = document.getElementById('start-btn');
const nextButton = document.getElementById('next-btn');
const endButton = document.getElementById('end-btn');

// Set the intro language
const intro = document.getElementById('intro');

// Set variable for the input fields
const betForm = document.getElementsByClassName('bet');

// Set variable for questions and answers
const questionContainerElement = document.getElementById('question-container');
const questionElement = document.getElementById('question');
const answerButtonsElement = document.getElementById('answer-buttons');

// Create variable for randomizing questions
let shuffledQuestions;

// Create variable for incrementing number of questions
let currentQuestionIndex;

// Set chip total to start game
let bankroll = 100;

// Set input range between 10 and chip total
let bet_input = document.getElementById("bet-input");
function limit() {
    bet_input.value=Math.min(bankroll, bet_input.value);
    bet_input.value=Math.max(10, bet_input.value);
}
bet_input.onchange=limit;

// Action based on buttons clicked
startButton.addEventListener('click', startGame);
nextButton.addEventListener('click', () => {
    currentQuestionIndex++;
    setNextQuestion();
});
//endButton.addEventListener('click', endGame);


// Start the game
function startGame() {
    console.log("Game has started");

    // Hide start button
    startButton.classList.add('hide');
    intro.classList.add('hide');

    // List chip total
    $('#chips_in_bank').text("You have " + bankroll + " chips to bet.");

    // Remove the input field
    for (var i = 0; i < betForm.length; i ++) {
    betForm[i].classList.remove('hide');
    }

    // Choose a random question and set it as the first
    shuffledQuestions = questions.sort(() => Math.random() - 0.5);
    currentQuestionIndex = 0;
    questionContainerElement.classList.remove('hide');
    setNextQuestion();
}


function setNextQuestion() {
    resetState();

    // Display new random question
    showQuestion(shuffledQuestions[currentQuestionIndex]);

    // Show the input field
    for (var i = 0; i < betForm.length; i ++) {
    betForm[i].classList.remove('hide');

    // Set the default input value always to 10
    betForm[i].value = 10;
    }
}


function showQuestion(question) {
    $("#win_or_lose").hide();

    // Show the question
    questionElement.innerText = question.question;

    // Transform answers for question array into button choices
    question.answers.forEach(answer => {
      const button = document.createElement('button');
      button.innerText = answer.text;
      // Turn answers into button classes
      button.classList.add('btn');

      // Establish correct answer from answers (correct: true)
      if (answer.correct) {
          button.dataset.correct = answer.correct;
      }
      button.addEventListener('click', selectAnswer);

      // Display answer choices
      answerButtonsElement.appendChild(button);
    });
}

function resetState() {
    // Hide next button
    nextButton.classList.add('hide');

    // Remove answer choices
    while (answerButtonsElement.firstChild) {
        answerButtonsElement.removeChild
        (answerButtonsElement.firstChild);
    }
}

function selectAnswer(e) {

    // Determine whether clicked answer is correct
    const selectedButton = e.target;
    const correct = selectedButton.dataset.correct;
    setStatusClass(document.body, correct);

    // Hide the input field
    for (var i = 0; i < betForm.length; i ++) {
    betForm[i].classList.add('hide');
    }


    event.preventDefault();
    let bet = parseInt($("#bet-input").val(), 10);
    console.log(bet);

    // Determine payouts if answer is correct
    if (correct) {

        $('#win_or_lose').text("Correct! You double your bet!");
        bankroll = (bankroll + bet*2);

    } else {
        $('#win_or_lose').text("Your guess was incorrect. You lost the bet.");
        bankroll = (bankroll - bet);
        if (bankroll < 10) {
            bankroll = 10;
        }
    }

    // Set correct or incorrect status for each button on click
    Array.from(answerButtonsElement.children).forEach(button => {
        setStatusClass(button, button.dataset.correct);

        // Show whether user got question right
        $('#win_or_lose').show();

        // Determine whether game is over after (8 questions)
        if (currentQuestionIndex + 1 == 8) {
          endGame(bankroll);

        } else {
            // Otherwise show next button and chip total
            nextButton.classList.remove('hide');
            $('#chips_in_bank').text("You have " + bankroll + " chips left to bet.");
        }
        });
}


function endGame(bankroll) {
    endButton.classList.remove('hide');
    $('#chips_in_bank').text("You earned " + bankroll + " chips. Thanks for playing, and keep going to improve your score!");
    $("#bankroll").val(bankroll);
}


function setStatusClass(element, correct) {
    // Clear any ornamentation to answer choices
    clearStatusClass(element);

    // Add green or red style to answer buttons
    if (correct) {
        element.classList.add('correct');
    } else {
        element.classList.add('incorrect');
    }
}


function clearStatusClass(element) {
    element.classList.remove('correct');
    element.classList.remove('incorrect');
}