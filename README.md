# Typing Coach written in python, using tkinter
## General Info
- This is a typing coach app to help improve user's typing speed.
- Attached is a .txt file of 225 random words, initally an API was used to fetch a random list of words but it slowed the program down considerably.
- The app uses OOP to generate a start screen, a game screen, and an end screen.
- A timer begins from one minute. The target words are displayed and the users current word is formatted accordingly.
- The user types the word into the input text box (which is preselected). Upon hitting space the user input is submitted.
- The submitted word is compared to the current word. If correct the score is updated. The previous word is formatted green for correct,
  red for incorrect. The next word is formatted to be current word.
- Once the timer reaches zero the game screen ends and the end screen is generated, displaying how the user did.
- Restart button if user wants to play again

## Technologies
- tkinter 8.6.13 
- python 3.12.3
