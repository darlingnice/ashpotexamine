document.addEventListener('DOMContentLoaded', () => {
  loadFirstQuestion(); // Load the first question when the page is loaded

  // clear the local storage

  localStorage.clear()
});

var number = 0;  // Represents the current question number (zero-indexed)

document.getElementById('btn-next').addEventListener('click', (e) => {
  loadNextQuestion();
});

document.getElementById('btn-previous').addEventListener('click', (e) => {
  loadPreviousQuestion();
});

async function loadNextQuestion() {
  const total_questions = parseInt(document.getElementById('total-questions').innerText);
  const course_id = parseInt(document.getElementById('record-id').innerText);
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  let  = selectedAnswer  = 'none';
  selectedAnswer = document.querySelector('input[name="options"]:checked')
  if (!selectedAnswer){
    console.log("select an option")
  }else{
    localStorage.setItem(`question${number+1}`,selectedAnswer.value)
  // Update question number based on button clicked

    if (number < total_questions - 1) {  // Prevent going beyond total questions
      number++;
    }
  }
  // Fetch the question data only if number is in a valid range
  if (number >= 0 && number < total_questions) {    
    try {
      const response = await fetch(`/exam/take/${course_id}`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question_number: number })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
      }

      const data = await response.json();

      // Update the DOM with the new question and options
      document.getElementById('question-displayer').innerText = data.question;
      document.getElementById('lbl-A').innerText = data.optionA;
      document.getElementById('lbl-B').innerText = data.optionB;
      document.getElementById('lbl-C').innerText = data.optionC;
      document.getElementById('lbl-D').innerText = data.optionD;

      // Update the question number display (1-based for UI)
      const question_number = document.getElementById('question-number');
      question_number .innerText = number + 1;
      const previous_button = document.getElementById('btn-previous');
      parseInt(question_number.innerText)  > 1? 
      previous_button.style.visibility = 'visible': previous_button.style.visibility = 'hidden';
      let option_radios = document.getElementsByName('options')

      for(let x of option_radios){
        x.checked = false;
      }

    } catch (error) {
      console.error('Error:', error);
    }
  }
  }

  




async function loadFirstQuestion(){
  const total_questions = parseInt(document.getElementById('total-questions').innerText);
  const course_id = parseInt(document.getElementById('record-id').innerText);
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  try {
    const response = await fetch(`/exam/take/${course_id}`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question_number: number })
    });

    if (!response.ok) {
      throw new Error('Network response was not ok ' + response.statusText);
    }

    const data = await response.json();

    // Update the DOM with the new question and options
    document.getElementById('question-displayer').innerText = data.question;
    document.getElementById('lbl-A').innerText = data.optionA;
    document.getElementById('lbl-B').innerText = data.optionB;
    document.getElementById('lbl-C').innerText = data.optionC;
    document.getElementById('lbl-D').innerText = data.optionD;

    // Update the question number display (1-based for UI)
    const question_number = document.getElementById('question-number');
    question_number .innerText = number + 1;
    // const previous_button = document.getElementById('btn-previous');
    // parseInt(question_number.innerText)  > 1? 
    // previous_button.style.visibility = 'visible': previous_button.style.visibility = 'hidden';

  } catch (error) {
    console.error('Error:', error);
  }
}

async function loadPreviousQuestion() {
  const total_questions = parseInt(document.getElementById('total-questions').innerText);
  const course_id = parseInt(document.getElementById('record-id').innerText);
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  number --;
  // let  = selectedAnswer  = 'none';
  // selectedAnswer = document.querySelector('input[name="options"]:checked')
  // if (!selectedAnswer){
  //   console.log("select an option")
  // }else{
  //   localStorage.setItem(`question${number+1}`,selectedAnswer.value)
  // // Update question number based on button clicked

  // }
  // Fetch the question data only if number is in a valid range
  if (number >= 0 && number < total_questions) {    
    try {
      const response = await fetch(`/exam/take/${course_id}`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question_number: number })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
      }

      const data = await response.json();

      // Update the DOM with the new question and options
      document.getElementById('question-displayer').innerText = data.question;
      document.getElementById('lbl-A').innerText = data.optionA;
      document.getElementById('lbl-B').innerText = data.optionB;
      document.getElementById('lbl-C').innerText = data.optionC;
      document.getElementById('lbl-D').innerText = data.optionD;

      // Update the question number display (1-based for UI)
      const question_number = document.getElementById('question-number');
      question_number .innerText = number + 1;
      const previous_button = document.getElementById('btn-previous');
      parseInt(question_number.innerText)  > 1? 
      previous_button.style.visibility = 'visible': previous_button.style.visibility = 'hidden';
      let option_radios = document.getElementsByName('options')

      for(let x of option_radios){
        x.checked = false;
      }

    } catch (error) {
      console.error('Error:', error);
    }
  }
  }

  
