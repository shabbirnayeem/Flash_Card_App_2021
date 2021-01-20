from tkinter import *
import pandas
import random
from tkinter import messagebox

BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------- Creating New Flash Cards ------------------------------- #
current_word = {}
to_learn = {}

try:
    # program will try to read from the words_to_learn.csv
    # this will not exit when the program first run
    # reading from the CSV file using pandas
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    # if the words_to_learn.csv not found, load data from the french_words.csv
    # this is included in with the program
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
except pandas.errors.EmptyDataError:
    # this error occur after all the words are learned and words_to_learn file is empty
    messagebox.showinfo(title="Complete", message="No more words to learn, Congrats!\n The words to learn file is empty.")

else:
    # creating dict from CSV file
    to_learn = data.to_dict(orient="records")


def new_word():
    # generating a card from the data file
    global current_word, flip_timer
    # when the we click right or wrong to to go the next card the, the flip_timer should be deactivate
    # THIS is to prevent a bug, without the after.cancel no matter which card your on after 3s the card will flip
    # with this added the will only change once you land on card and wait 3s
    window.after_cancel(flip_timer)

    try:
        current_word = random.choice(to_learn)
    except IndexError:
        # this error occur after all the words are learned and words_to_learn file is empty
        messagebox.showinfo(title="Complete", message="No more words to learn, Congrats!")

    else:
        # getting host of the French word from the dict
        fr_word = current_word["French"]

        # Change the flash card back to front card and text to black
        canvas.itemconfig(canvas_image, image=card_front)
        canvas.itemconfig(title_text, text=f"French", fill="black")
        canvas.itemconfig(word_text, text=f"{fr_word}", fill="black")

        # restart the flip_timer
        flip_timer = window.after(3000, flip)

# -----------------------------  Flip the Cards  -------------------------------- #

# Creating fun to flip the index card after 3s
# Going to use TKinter after methods


def flip():
    # changing the canvas image
    # basically the swapping the image
    canvas.itemconfig(canvas_image, image=card_back)

    # Change the title to English and display the eng meaning of the Fr word
    canvas.itemconfig(title_text, text=f"English", fill="white")
    eng_word = current_word["English"]
    canvas.itemconfig(word_text, text=f"{eng_word}", fill="white")


# is_known function is going to remove the current_word if the user presses the check,
# which means the user knows the words
# this function is bind with the check button
def is_known():
    try:
        # remove current_word from the to_learn list
        to_learn.remove(current_word)
    except ValueError:
        # this error occur after all the words are learned and words_to_learn file is empty
        messagebox.showinfo(title="Complete", message="No more words to learn, Congrats!")
    else:
        data_learn = pandas.DataFrame(to_learn)
        data_learn.to_csv("data/words_to_learn.csv", index=False)

        # call the next word
        new_word()

# --------------------------------- UI SETUP ------------------------------------------ #


window = Tk()
window.title("Flashy")
# Adding padding and bg color
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# time to flip card
# The index card will flip after every 3s
# 1000mx == 1s
flip_timer = window.after(3000, flip)

# creating the canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR,  highlightthickness=0)

# reading the images from the files
card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")

# Adding the image to to the canvas
canvas_image = canvas.create_image(410, 263, image=card_front)

# Writing Text on top of the flash card
title_text = canvas.create_text(400, 150, text="", fill="black", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 40, "bold"))

# Layout manager
canvas.grid(column=0, row=0, columnspan=2)

# Creating the right and wrong buttons
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)
wrong_button = Button(image=wrong_image, highlightthickness=0, command=new_word)
wrong_button.grid(column=0, row=1)


# calling the random_word generating function
new_word()


window.mainloop()
