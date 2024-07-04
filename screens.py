from tkinter import *
from random import shuffle

# Ranking for typing speed
wpm_ranking = {
    0: "Absolute Beginner",
    10: "Absolute Beginner",
    20: "Beginner",
    30: "Novice",
    40: "Congratulations! You are average!",
    50: "Above Average! (Superiority Complex)",
    60: "Professional",
    70: "Fast n Furious",
    80: "S-M-R-T",
    90: "Genious",
    100: "You are in the top 1% of typists!"
}


class StartScreen:
    """Display start screen to begin the game"""
    def __init__(self, root):
        # Root window to be passed into Game class as the root window
        self.root = root

        # Create a frame to display the start screen widgets
        self.start_screen = Frame(root)
        self.start_screen.config(padx=100,
                                 pady=20,
                                 highlightbackground="wheat4",
                                 highlightthickness=2)
        self.start_screen.pack()

        # Create title label
        self.title_label = Label(self.start_screen,
                                 text="TYPING COACH",
                                 font=("Futura", 50, "italic"),
                                 pady=80)
        self.title_label.grid(column=0, row=1)

        # Create highscore label
        with open("highscore.txt") as file:
            highscore = file.read()
            self.highscore_label = Label(self.start_screen,
                                         text=f"Highscore: {highscore}",
                                         font=("Silom", 16),
                                         anchor="nw")
            self.highscore_label.grid(column=0, row=0)

        # Create button to begin the game
        self.start_button = Button(self.start_screen,
                                   width=10,
                                   text="Start",
                                   font=("Silom", 12))
        self.start_button.bind("<Button-1>", self.begin)
        self.start_button.grid(column=0, row=2)

    def begin(self, event=None):
        """Function to remove start screen and begin the game"""
        self.__del__()

        Game(self.root)

    def __del__(self):
        """Function to remove StartScreen object and associated widgets"""
        self.start_screen.destroy()


class Game:
    """Game to test how fast a user can type"""
    def __init__(self, root):
        # Attributes to keep track of time / what word / score user is on
        self.time = None
        self.current_word_index = 0
        self.score = 0

        # Get a list of random words
        with open("words.txt") as file:
            self.word_list = [line.strip() for line in file.readlines()]
        shuffle(self.word_list)

        # Root window to be passed into Game class as the root window
        self.root = root

        # Frame to hold the game widgets
        self.text_space = Frame(root)
        self.text_space.config(padx=5,
                               pady=5,
                               bg="wheat2",
                               highlightbackground="wheat2",
                               highlightthickness=2)
        self.text_space.pack()

        # Label for current word
        self.current_word_label = Label(self.text_space,
                                        width=20,
                                        text=f"Current word: {self.word_list[self.current_word_index]}",
                                        font=("Silom", 16),
                                        anchor="w",
                                        padx=10,
                                        pady=10,
                                        bg="wheat2")
        self.current_word_label.grid(row=0, column=0)

        # Timer label
        self.time_label = Label(self.text_space,
                                width=6,
                                text="00:00",
                                font=("Silom", 16),
                                padx=10,
                                pady=10,
                                bg="wheat2")
        self.time_label.grid(row=0, column=1)

        # Score label
        self.score_label = Label(self.text_space, width=14,
                                 text=f"Score: {self.score}",
                                 font=("Silom", 16),
                                 anchor="e",
                                 padx=10,
                                 pady=10,
                                 bg="wheat2")
        self.score_label.grid(row=0, column=2)

        # Word box displaying the random words
        self.word_box = Text(self.text_space,
                             width=20,
                             height=3,
                             font=("Silom", 40),
                             wrap="word",
                             padx=10,
                             pady=15,
                             highlightbackground="wheat4",
                             highlightthickness=1)
        self.word_box.grid(row=1, column=0, columnspan=3)
        self.word_box.insert(END, self.word_list)
        self.word_box.config(state=DISABLED)

        # Text box for user to type words into, pressing space/enter submits the word and calls the submit function
        self.user_entry = Text(self.text_space,
                               width=20,
                               height=1,
                               font=("Silom", 40),
                               padx=10,
                               pady=10,
                               highlightbackground="wheat4",
                               highlightthickness=1)
        self.user_entry.bind("<space>", self.submit)
        self.user_entry.bind("<Return>", self.submit)
        self.user_entry.grid(row=2, column=0, columnspan=3)
        self.user_entry.focus()

        # Find current word position in text box
        self.current_word = self.word_list[self.current_word_index]
        self.pos = self.word_box.search(self.current_word, "1.0", stopindex=END)
        self.end_pos = self.add_decimal_places(self.pos, len(self.current_word)/10)

        # Format the first word as the 'current word'
        self.word_box.tag_config("start", foreground="wheat4")
        self.word_box.tag_add("start", self.pos, self.end_pos)

        # Start the timer
        self.count_down(60)

    def count_down(self, count):
        """Function for timer"""
        self.time = count

        # If timer reaches zero end the game and display end screen
        if self.time == 0:
            EndScreen(self.root, self.score, self.current_word_index)
            self.__del__()
            return

        # Formatting timer
        if self.time == 0 or self.time < 10:
            count_text = f"0{self.time}"
        else:
            count_text = self.time

        # Set timer value to label
        self.time_label.config(text=f"00:{count_text}")

        # Count down by one second
        if self.time > 0:
            self.text_space.after(1000, self.count_down, self.time - 1)

    def submit(self, event=None):
        """Function to determine if the user typed current word correctly"""

        # Get the text user submitted
        entry = self.user_entry.get("1.0", END).strip()

        # Formatting for text colour
        self.word_box.tag_remove("current", "1.0", "end")

        # Compare submission to current word
        if entry == self.current_word:
            # Increment score / change word colour accordingly
            self.score += 1
            self.word_box.tag_config("correct", foreground="sea green")
            self.word_box.tag_add("correct", f"{self.pos}", f"{self.end_pos}")

        else:
            # Change word colour for wrong answer
            self.word_box.tag_config("incorrect", foreground="IndianRed2")
            self.word_box.tag_add("incorrect", f"{self.pos}", f"{self.end_pos}")

        # Clear user box and update score
        self.user_entry.delete("1.0", END)
        self.score_label.config(text=f"{self.score}")

        # Move to next word
        self.current_word_index += 1
        self.current_word = self.word_list[self.current_word_index]

        # Reformat for new current word
        self.pos = self.word_box.search((self.current_word + " "), self.end_pos, stopindex=END)
        self.end_pos = self.add_decimal_places(self.pos, len(self.current_word) / 10)
        self.word_box.tag_config("current", foreground="wheat4")
        self.word_box.tag_add("current", f"{self.pos}", f"{self.end_pos}")
        self.current_word_label.config(text=f"Current word: {self.current_word}")

        # Scroll down the textbox
        self.word_box.see(index=self.pos)

    def add_decimal_places(self, num1, num2):
        """Function for character positioning (Tkinter positioning adds decimals as if they were integers)"""

        # Convert numbers to strings to separate integer and decimal parts
        str_num1 = str(num1)
        str_num2 = str(num2)

        # Separate the integer and decimal parts
        int_part1, dec_part1 = str_num1.split(".")
        int_part2, dec_part2 = str_num2.split(".")

        # Add the integer parts
        int_sum = int(int_part1)

        # If the word is greater than 10 character, count those characters as decimals
        if int(int_part2) > 0:
            word_over = int(int_part2)*10
        else:
            word_over = 0

        # Add the decimal parts
        dec_sum = int(dec_part1) + int(dec_part2) + word_over

        # Combine the integer and decimal parts
        result = f"{int_sum}.{dec_sum}"

        return result

    def __del__(self):
        """Function to remove Game object and associated widgets"""
        self.text_space.destroy()


class EndScreen:
    """Display end screen after typing game is finished"""
    def __init__(self, root, score, total_words):
        # Root window to be passed into Game class as the root window
        self.root = root

        # Check if user score beats highscore
        self.new_highscore = False
        self.check_highscore(score)

        # Create frame for end screen widgets
        self.end_screen = Frame(root)
        self.end_screen.config(padx=70,
                               pady=20,
                               highlightbackground="wheat4",
                               highlightthickness=2)
        self.end_screen.pack()

        # Calculate user accuracy and rating, and input into score label detailing how the user performed
        accuracy = int((score/total_words) * 100)
        ranking = wpm_ranking[(score//10) * 10]

        self.score_label = Label(self.end_screen,
                                 text=f"Your Score: {score} wpm!\nAccuracy: {accuracy}%\nYour Ranking: {ranking}",
                                 font=("Futura", 30, "italic"),
                                 justify=LEFT,
                                 pady=80)
        self.score_label.grid(column=0, row=1)

        # Displays highscore
        with open("highscore.txt") as file:
            highscore = file.read()
            if self.new_highscore:
                message = f"Good Job! You've set a new highscore of: {score}!"
            else:
                message = f"Highscore: {highscore}"
            self.highscore_label = Label(self.end_screen,
                                         text=message,
                                         font=("Silom", 16),
                                         anchor="nw")
            self.highscore_label.grid(column=0, row=0)

        # Button to restart the game
        self.restart_button = Button(self.end_screen,
                                     width=10,
                                     text="Restart",
                                     font=("Silom", 12))
        self.restart_button.bind("<Button-1>", self.restart)
        self.restart_button.grid(column=0, row=2)

    def restart(self, event=None):
        """Function to remove end screen and restart the game"""
        self.__del__()
        Game(self.root)

    def check_highscore(self, score):
        """Function to see if highscore has been beaten"""
        with open("highscore.txt") as file:
            highscore = int(file.read())

        # If user score beats highscore, rewrite highscore as user score
        if score > highscore:
            self.new_highscore = True
            with open("highscore.txt", "w") as file:
                file.write(str(score))

    def __del__(self):
        """Function to remove EndScreen object and associated widgets"""
        self.end_screen.destroy()
