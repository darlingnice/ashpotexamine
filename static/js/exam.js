document.addEventListener('DOMContentLoaded', () => {
  loadFirstQuestion(); // Load the first question when the page is loaded
});

var number = 0;  // Represents the current question number (zero-indexed)

document.getElementById('btn-next').addEventListener('click', () => {
  loadNextQuestion();
});

document.getElementById('btn-previous').addEventListener('click', () => {
  loadPreviousQuestion();
});
const givenAnswers = {}
const correct_options = {}




async function loadFirstQuestion(){
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
      if(response.status = 401){
        document.location.href = '/login/'
      }
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
    correct_options[number+1] = data.correct_option
    number ++; // increment the number used to fetch the questions according to the list in the backend

  } catch (error) {
    console.error('Error:', error);
  }
}


async function loadNextQuestion() {
  const total_questions = parseInt(document.getElementById('total-questions').innerText);
  const course_id = parseInt(document.getElementById('record-id').innerText);
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  let  = selectedAnswer  = 'none';
  selectedAnswer = document.querySelector('input[name="options"]:checked')
  const question_number = parseInt(document.getElementById('question-number').innerText);

  if(number  >= total_questions  ){
      givenAnswers[question_number] = selectedAnswer.value
      const btn_container = document.getElementById('btn-container');
      const submit_container = document.getElementById('submit-container')
      btn_container.style.display = 'none';
      submit_container.style.display = 'flex'
      submit_container.style.justifyContent = 'flex-end'

  }else{
    if (!selectedAnswer){
      showPopup("Info Message","You have not seected any answer.\nPlease select an option.")
    }else{
        givenAnswers[question_number] = selectedAnswer.value
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
        correct_options[number+1] = data.correct_option
    
        // Update the question number display (1-based for UI)
        const question_number = document.getElementById('question-number');
        question_number .innerText = number + 1;
        const previous_button = document.getElementById('btn-previous');
        parseInt(question_number.innerText)  > 1? 
        previous_button.style.visibility = 'visible': previous_button.style.visibility = 'hidden';
        let option_radios = document.getElementsByName('options')
        console.log(number)
        number ++;
  
        for(let x of option_radios){
          x.checked = false;
        }
  
      } catch (error) {
        console.error('Error:', error);
      }
    }
      }

  }
   
  }




async function loadPreviousQuestion() {
  const total_questions = parseInt(document.getElementById('total-questions').innerText);
  const course_id = parseInt(document.getElementById('record-id').innerText);
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  number --;
  
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



document.getElementById('btn-submit').addEventListener('click',submit)  
function submit(){
  const record_id  = document.getElementById('record-id').innerText;
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  fetch('/exam/submit/',{
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(
      {  
        exam_id: record_id,
        answers: givenAnswers,
        correct_options: correct_options
       })
  })
  .then((response)=>{
    if(!response.ok){
      throw new Error('Network response was not ok ' + response.statusText)
    }
    return response.json()
    .then((data)=>{
       showPopup("Congratulation ","You are done writing the Test.\nYour answers have been submitted.",forced_to_appear=false)
    })
    .catch((e)=>{
      console.log(e)
    })
  })
}


// function to retrieve the result
document.getElementById('btn-result').addEventListener('click',getResult)  
function getResult(){
  const record_id  = document.getElementById('record-id').innerText;
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  fetch('/exam/result/',{
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(
      {  
        user: record_id
       })
  })
  .then((response)=>{
    if(!response.ok){
      throw new Error('Network response was not ok ' + response.statusText)
    }
    return response.json()
    .then((data)=>{
      //  showPopup("Congratulation ","You are done writing the Test.\nYour answers have been submitted.")
    })
    .catch((e)=>{
      console.log(e)
    })
  })
}



  // Set the exam duration in minutes
  const examDurationMinutes = parseInt(document.getElementById('duration').innerText);
  let timeRemaining = examDurationMinutes * 60; // Convert to seconds

    const timerElement = document.getElementById('examTimer');

    // Update the countdown every 1 second
    const countdown = setInterval(() => {
        // Calculate minutes and seconds
        const minutes = Math.floor(timeRemaining / 60);
        const seconds = timeRemaining % 60;

        // Display the result in the timer element
        timerElement.textContent = `Time Remaining: ${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;

        // If the time is up, stop the timer and trigger exam submission
        if (timeRemaining <= 0) {
            clearInterval(countdown);
            showPopup();
            document.getElementById('btn-submit').click() //submit the exam         
        }

        timeRemaining--; // Decrease time by 1 second
    }, 1000);




      // Function to show the custom popup
      function showPopup(header_message=null,message=null,forced_to_appear=true) {

        const dialog_text_header = document.getElementById('dialog-text-header');
        const dialog_text = document.getElementById('dialog-text');
        if(!forced_to_appear){
          dialog_text_header.innerText = header_message;
          dialog_text.innerText = message;
        }else{
          dialog_text_header.innerText = "Time's up";
          dialog_text.innerText = 'Your time for the exam has ended and your answers have been submitted';
        }
      
        popup.style.display = 'block';
        overlay.style.display = 'block'; // Show the overlay
    }

    // Function to close the popup
    function closePopup() {
        popup.style.display = 'none';
        overlay.style.display = 'none'; // Hide the overlay
    }