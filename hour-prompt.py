import pyautogui

work_item = pyautogui.prompt(
    text='What have you been working on?',
    title='Work Tracking',
)

# import tkinter as tk
# from tkinter import simpledialog

# ROOT = tk.Tk()

# ROOT.withdraw()
# # the input dialog
# USER_INP = simpledialog.askstring(
#     title="Test",
#     prompt="What's your Name?"
# )

# # check it out
# print("Hello", USER_INP)