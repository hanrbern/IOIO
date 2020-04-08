import kivy
from kivy.app import App
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.uix.popup import Popup
from random import randint
from kivy.uix.image import Image
import numpy as np
import os.path
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
import datetime
#import pandas as pd
#import xlrd
import scipy.stats as stats
#import matplotlib.pyplot as plt
import logging
import sys
import socketserver
import socket
kivy.require('1.11.1')


# colours in rgba
blue = 0, 0, 1, 1
green = 0, 1, 0, 1
silver = 1, 1, 1, 0.5
gold = 1, 1, 0, 0.5


# Window for submitting subject ID to start a new game
class Intro1(Screen):
    def next(self):
        sm.current = 'Intro2'

class Intro2(Screen):
    def next(self):
        sm.current = 'Intro3'

class Intro3(Screen):
    def next(self):
        sm.current = 'new'

class NewWindow(Screen):

    def submit(self):
        ioio.add_subject()
        sm.current = "game"
        press_to_start()


    def use_bestinputs(self):
        GameWindow.inputs_text = 1
        GameWindow.inputs = "bestInputs.txt"

    def show_results(self):
        sm.current = "results"

# Window to play the game on
class GameWindow(Screen):
    score = NumericProperty(0)
    rounds = NumericProperty(0)
    prob = NumericProperty(0)
    val = NumericProperty(0)
    correct = NumericProperty(0)
    suggestion = StringProperty('')
    suggestions = ["Blue.png", "Green.png"]
    colour = NumericProperty(0)
    quits = NumericProperty(0)
    pie_chart = ObjectProperty('black.png')
    value = NumericProperty(0)
    result = NumericProperty(0)

    # change to False if you want to use default probStructure, random correct answers and random pie charts
    inputs_text = NumericProperty(0)
    inputs = StringProperty("bestInputs.txt")

    # for AudioButton
    filename = StringProperty(None)
    sound = ObjectProperty(None, allownone=True)
    volume = NumericProperty(1.0)

    # Method for suggestion to change based on adviser's probability of giving the right advice
    def change_suggestion(self):

        # game update will change these to sound files
        suggestions = ["Blue.png", "Green.png"]

        # pie charts with black backgrounds
        images = ["b25.png", "b30.png", "b35.png", "b40.png", "b45.png", "b50.png", "b55.png", "b60.png", "b65.png",
                  "b70.png", "b75.png"]

        # values corresponding with the pie charts
        values_blue = [".25", ".30", '.35', '.40', '.45', '.50', '.55', '.60', '.65', '.70', '.75']
        values_green = [".75", ".70", ".65", ".60", ".55", ".50", ".45", ".40", ".35", ".30", ".25"]

        if self.rounds in range(0, 100):

            if self.inputs_text == 1:

                sug_column = np.loadtxt(self.inputs)[:, 0]
                value_column = np.loadtxt(self.inputs)[:, 1]
                prob_column = np.loadtxt(self.inputs)[:, 2]
                probStructure = []
                sugStructure = []
                valueStructure = []

                for i in range(0, 100):
                    s = sug_column[i]
                    v = self.round_value(value_column[i])
                    p = self.round_prob(prob_column[i])
                    sugStructure.append(int(s))
                    valueStructure.append(v)
                    probStructure.append(p)

                sug = sugStructure[self.rounds]
                value = valueStructure[self.rounds]
                probability = probStructure[self.rounds]

                if value == 0.25:
                    self.pie_chart = images[0]
                    # if green is correct, pie chart values written as green percentages
                    if sug == 1:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 5)
                            if self.val <= 2:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 1
                        return [self.result, self.suggestion]

                    # if blue is correct, pie charts written as blue percentages
                    if sug == 0:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 10)
                            if self.val <= 4:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 0
                        return [self.result, self.suggestion]
                if value == 0.3:
                    self.pie_chart = images[1]
                    # if green is correct, pie chart values written as green percentages
                    if sug == 1:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 5)
                            if self.val <= 2:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 1
                        return [self.result, self.suggestion]

                    # if blue is correct, pie charts written as blue percentages
                    if sug == 0:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 10)
                            if self.val <= 4:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 0
                        return [self.result, self.suggestion]
                if value == 0.35:
                    self.pie_chart = images[2]
                    # if green is correct, pie chart values written as green percentages
                    if sug == 1:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 5)
                            if self.val <= 2:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 1
                        return [self.result, self.suggestion]

                    # if blue is correct, pie charts written as blue percentages
                    if sug == 0:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 10)
                            if self.val <= 4:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 0
                        return [self.result, self.suggestion]
                if value == 0.4:
                    self.pie_chart = images[3]
                    # if green is correct, pie chart values written as green percentages
                    if sug == 1:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 5)
                            if self.val <= 2:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 1
                        return [self.result, self.suggestion]

                    # if blue is correct, pie charts written as blue percentages
                    if sug == 0:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 10)
                            if self.val <= 4:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 0
                        return [self.result, self.suggestion]
                if value == 0.45:
                    self.pie_chart = images[4]
                    # if green is correct, pie chart values written as green percentages
                    if sug == 1:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 5)
                            if self.val <= 2:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 1
                        return [self.result, self.suggestion]

                    # if blue is correct, pie charts written as blue percentages
                    if sug == 0:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 10)
                            if self.val <= 4:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 0
                        return [self.result, self.suggestion]
                if value == 0.5:
                    self.pie_chart = images[5]
                    # if green is correct, pie chart values written as green percentages
                    if sug == 1:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 5)
                            if self.val <= 2:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 1
                        return [self.result, self.suggestion]

                    # if blue is correct, pie charts written as blue percentages
                    if sug == 0:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 10)
                            if self.val <= 4:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 0
                        return [self.result, self.suggestion]
                if value == 0.55:
                    self.pie_chart = images[6]
                    # if green is correct, pie chart values written as green percentages
                    if sug == 1:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 5)
                            if self.val <= 2:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 1
                        return [self.result, self.suggestion]

                    # if blue is correct, pie charts written as blue percentages
                    if sug == 0:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 10)
                            if self.val <= 4:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 0
                        return [self.result, self.suggestion]
                if value == 0.6:
                    self.pie_chart = images[7]
                    # if green is correct, pie chart values written as green percentages
                    if sug == 1:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 5)
                            if self.val <= 2:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 1
                        return [self.result, self.suggestion]

                    # if blue is correct, pie charts written as blue percentages
                    if sug == 0:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 10)
                            if self.val <= 4:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 0
                        return [self.result, self.suggestion]
                if value == 0.65:
                    self.pie_chart = images[8]
                    # if green is correct, pie chart values written as green percentages
                    if sug == 1:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 5)
                            if self.val <= 2:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 1
                        return [self.result, self.suggestion]

                    # if blue is correct, pie charts written as blue percentages
                    if sug == 0:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 10)
                            if self.val <= 4:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 0
                        return [self.result, self.suggestion]
                if value == 0.7:
                    self.pie_chart = images[9]
                    # if green is correct, pie chart values written as green percentages
                    if sug == 1:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 5)
                            if self.val <= 2:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 1
                        return [self.result, self.suggestion]

                    # if blue is correct, pie charts written as blue percentages
                    if sug == 0:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 10)
                            if self.val <= 4:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 0
                        return [self.result, self.suggestion]
                if value == 0.75:
                    self.pie_chart = images[10]
                    # if green is correct, pie chart values written as green percentages
                    if sug == 1:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 5)
                            if self.val <= 2:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 1
                        return [self.result, self.suggestion]

                    # if blue is correct, pie charts written as blue percentages
                    if sug == 0:

                        self.correct = sug

                        if probability == 0.1:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.2:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.3:
                            self.val = randint(1, 10)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.4:
                            self.val = randint(1, 10)
                            if self.val <= 4:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.5:
                            self.val = randint(1, 2)
                            if self.val == 1:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.6:
                            self.val = randint(1, 5)
                            if self.val <= 3:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.7:
                            self.val = randint(1, 10)
                            if self.val <= 7:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]
                            else:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]

                        if probability == 0.8:
                            self.val = randint(1, 5)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        if probability == 0.9:
                            self.val = randint(1, 10)
                            if self.val == 1:
                                # suggest incorrect answer
                                if self.correct == 0:
                                    self.suggestion = suggestions[1]
                                    self.ids.suggestion.source = suggestions[1]
                                else:
                                    self.suggestion = suggestions[0]
                                    self.ids.suggestion.source = suggestions[0]
                            else:
                                # suggest correct answer
                                self.suggestion = suggestions[sug]
                                self.ids.suggestion.source = suggestions[sug]

                        # update subject.txt file
                        # correct colour
                        db.correct_colour(sug)
                        # pie chart value (percent blue)
                        db.probability(value)
                        # probability of correct advice
                        db.prob_advice(round(probability, 1))

                        # self.result is used to validate if answer is correct
                        self.result = 0
                        return [self.result, self.suggestion]

        # when game reaches 100 rounds, score and rounds reset, sent back to new game screen
        if self.rounds == 100:
            self.reset()
            self.new()


    def round_prob(self, x):
        a = x * 1000
        b = round(a, -2)
        c = b / 10
        if c % 10 == 0:
            return c / 100
        if c % 10 == 1:
            c = c - 1
            return c / 100
        if c % 10 == 2:
            c = c - 2
            return c / 100
        if c % 10 == 3:
            c = c - 3
            return c / 100
        if c % 10 == 4:
            c = c - 4
            return c / 100
        if c % 10 == 5:
            c = c + 5
            return c / 100
        if c % 10 == 6:
            c = c + 4
            return c / 100
        if c % 10 == 7:
            c = c + 3
            return c / 100
        if c % 10 == 8:
            c = c + 2
            return c / 100
        if c % 10 == 9:
            c = c + 1
            return c / 100

    def round_value(self, x):
        a = x * 1000
        b = round(a, -1)
        c = b / 10
        if c % 5 == 0:
            return c / 100
        if c % 5 == 1:
            c = c - 1
            return c / 100
        if c % 5 == 2:
            c = c - 2
            return c / 100
        if c % 5 == 3:
            c = c + 2
            return c / 100
        if c % 5 == 4:
            c = c + 1
            return c / 100

    # popup to tell user their answer is correct
    def correct_answer(self):
        show = Correct()
        popupWindow = Popup(title="Correct!",
                            content=show,
                            size_hint=(None, None),
                            size=(300, 300),
                            pos_hint={"center_x": 0.5, "center_y": 0.5}
                            )
        popupWindow.open()

    def incorrect_answer(self):
        show = Incorrect()
        popupWindow = Popup(title="Incorrect!",
                            content=show,
                            size_hint=(None, None),
                            size=(300, 300),
                            pos_hint={"center_x": 0.5, "center_y": 0.5}
                            )
        popupWindow.open()

    # called when blue button is pressed
    def bluepressed(self):
        # Blue = 0
        if self.rounds == 0:
            self.score = 0
            self.ids.scorelbl.text = str(self.score)
            self.change_suggestion()
            AudioButton.play_sound(self, self.suggestion)
        if self.rounds == 100:
            self.validate(0)
            self.reset()
            self.new()
            return
        else:
            self.validate(0)
            AudioButton.play_sound(self, self.suggestion)
        self.rounds += 1

    # called when green button is pressed
    def greenpressed(self):
        # Green = 1
        if self.rounds == 0:
            self.score = 0
            self.ids.scorelbl.text = str(self.score)
            self.change_suggestion()
            AudioButton.play_sound(self, self.suggestion)
        if self.rounds == 100:
            self.validate(1)
            self.reset()
            self.new()
            return
        else:
            self.validate(1)
            AudioButton.play_sound(self, self.suggestion)
        self.rounds += 1

    # checks if user selected the correct colour and updates subjects.txt file with the button selected
    def validate(self, colour):
        if colour == 1:
            if self.result == colour:
                self.score += 1
                self.ids.scorelbl.text = str(self.score)
                self.correct_answer()
            else:
                if self.score != 0:
                    self.score -= 1
                self.ids.scorelbl.text = str(self.score)
                self.incorrect_answer()
            db.button_selected(1)
        if colour == 0:
            if self.result == colour:
                self.score += 1
                self.ids.scorelbl.text = str(self.score)
                self.correct_answer()
            else:
                if self.score != 0:
                    self.score -= 1
                self.ids.scorelbl.text = str(self.score)
                self.incorrect_answer()
            db.button_selected(0)
        # prompts the suggestion to change
        self.helppopup()
        self.change_suggestion()


    # popup to ask about the intentions of the adviser
    def helppopup(self):
        if self.rounds == 25:
            help_adviser()
        if self.rounds == 50:
            help_adviser()
        if self.rounds == 75:
            help_adviser()
        else:
            return None

    def new(self):
        man = IOManager(db.filename,'192.168.0.15')
        res.pvec = man.getResults()
        sm.current = "results"


    # pops up as a warning if the first time the quit button is pressed
    # second press resets the game and takes the user back to the new game screen
    def quit_btn(self):
        if self.quits == 1:
            self.reset()
            self.new()
            self.quits = 0
        else:
            show_warning()
            self.quits = 1

    # resets the score and rounds
    def reset(self):
        self.score = 0
        self.rounds = 0
        self.ids.suggestion.text = " "

    # gives the user a refresher of the instructions without having to restart the game
    def revInstructions(self):
        pop = Popup(title='Instructions',
                    content=Label(text="Using the advice given, \n select BLUE or GREEN \n to guess the result of \n the binary lottery. Click \n anywhere to close popups. ", halign='center'),
                    size_hint=(None, None),
                    size=(250, 250),
                    pos_hint={"center_x": 0.5, "center_y": 0.5}
                    )
        pop.open()

class Correct(FloatLayout):
    pass

class Incorrect(FloatLayout):
    pass

class ResultsWindow(Screen):
    pvec = ObjectProperty()

    def start(self):
        sm.current = 'results'

    def restart(self):
        db.new_file(filename="data/" + DataBase.get_date() + "_" + str(randint(0, 10000)) + ".txt")
        sm.current = 'Intro1'

    def kappa(self):
        graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
        x_ticks_major=0.5, y_ticks_major=0.2,
        y_grid_label=True, x_grid_label=True, padding=5,
        x_grid=True, y_grid=True, xmin=-2, xmax=4, ymin=0, ymax=0.5)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        x = np.arange(-2,4,0.1)
        m = 1
        y1 = stats.norm.pdf(x, m, 1)
        pts = []
        for i in range(len(y1)):
            pts.append((x[i],y1[i]))
        plot.points = pts
        y2 = np.arange(0,1,0.1)
        pts1 = []
        for i in range(len(y2)):
            pts1.append((self.pvec[9],y2[i]))
        plot2 = MeshLinePlot(color=[0,1,0,1])
        plot2.points = pts1
        graph.add_plot(plot)
        graph.add_plot(plot2)
        pop = Popup(title='Kappa',
                    content=graph,
                    size_hint=(None,None),
                    size=(300,300))
        pop.open()



    def omega2(self):
        graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
                      x_ticks_major=0.5, y_ticks_major=0.2,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=-7, xmax=3, ymin=0, ymax=0.5)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        x = np.arange(-5, 1, 0.1)
        m = -3
        y1 = stats.norm.pdf(x, m, 1)
        pts = []
        for i in range(len(y1)):
            pts.append((x[i], y1[i]))
        plot.points = pts
        y2 = np.arange(0, 1, 0.1)
        pts1 = []
        for i in range(len(y2)):
            pts1.append((self.pvec[10], y2[i]))
        plot2 = MeshLinePlot(color=[0, 1, 0, 1])
        plot2.points = pts1
        graph.add_plot(plot)
        graph.add_plot(plot2)
        pop = Popup(title='Omega',
                    content=graph,
                    size_hint=(None, None),
                    size=(300, 300))
        pop.open()

    def m2(self):
        graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
                      x_ticks_major=0.5, y_ticks_major=0.2,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=-4, xmax=4, ymin=0, ymax=0.5)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        x = np.arange(-3, 3, 0.1)
        m = 0
        y1 = stats.norm.pdf(x, m, 1)
        pts = []
        for i in range(len(y1)):
            pts.append((x[i], y1[i]))
        plot.points = pts
        y2 = np.arange(0, 1, 0.1)
        pts1 = []
        for i in range(len(y2)):
            pts1.append((self.pvec[7], y2[i]))
        plot2 = MeshLinePlot(color=[0, 1, 0, 1])
        plot2.points = pts1
        graph.add_plot(plot)
        graph.add_plot(plot2)
        pop = Popup(title='M2',
                    content=graph,
                    size_hint=(None, None),
                    size=(300, 300))
        pop.open()

    def m3(self):
        graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
                      x_ticks_major=0.5, y_ticks_major=0.2,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=-4, xmax=4, ymin=0, ymax=0.5)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        x = np.arange(-3, 3, 0.1)
        m = 0
        y1 = stats.norm.pdf(x, m, 1)
        pts = []
        for i in range(len(y1)):
            pts.append((x[i], y1[i]))
        plot.points = pts
        y2 = np.arange(0, 1, 0.1)
        pts1 = []
        for i in range(len(y2)):
            pts1.append((self.pvec[8], y2[i]))
        plot2 = MeshLinePlot(color=[0, 1, 0, 1])
        plot2.points = pts1
        graph.add_plot(plot)
        graph.add_plot(plot2)
        pop = Popup(title='M3',
                    content=graph,
                    size_hint=(None, None),
                    size=(300, 300))
        pop.open()

    def theta(self):
        graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
                      x_ticks_major=0.5, y_ticks_major=0.2,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=-9, xmax=-3, ymin=0, ymax=0.5)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        x = np.arange(-8, -4, 0.1)
        m = -6
        y1 = stats.norm.pdf(x, m, 1)
        pts = []
        for i in range(len(y1)):
            pts.append((x[i], y1[i]))
        plot.points = pts
        y2 = np.arange(0, 1, 0.1)
        pts1 = []
        for i in range(len(y2)):
            pts1.append((self.pvec[11], y2[i]))
        plot2 = MeshLinePlot(color=[0, 1, 0, 1])
        plot2.points = pts1
        graph.add_plot(plot)
        graph.add_plot(plot2)
        pop = Popup(title='Theta',
                    content=graph,
                    size_hint=(None, None),
                    size=(300, 300))
        pop.open()


class DataBase(object):
    def __init__(self, filename):
        self.filename = filename
        self.file = None
        self.load()

    def new_file(self, filename):
        self.filename = filename
        self.file = None
        self.load()

    def load(self):
        # if file already exists, 'r', if it doesn't then 'w+'
        if os.path.isfile(self.filename):
            self.file = open(self.filename, 'r')
        else:
            self.file = open(self.filename, "w+")
        self.file.close()

    def add_subject(self):
        file_object = open(self.filename, 'a')
        file_object.write(DataBase.get_date() + "_" + DataBase.get_time() + "\n")

    def start(self):
        file_object = open(self.filename, 'a')
        file_object.write(str(bool) + "\n")
        file_object.close()

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]

    @staticmethod
    def get_time():
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    # First column is correct colour: 0 - blue, 1 - green
    def correct_colour(self, bool):
        file_object = open(self.filename, 'a')
        file_object.write(str(bool) + "\t")
        file_object.close()

    # Second column is probability of correct colour in the pie chart: value between 0.25 and 0.75
    def probability(self, value):
        file_object = open(self.filename, 'a')
        file_object.write(str(value) + " \t")
        file_object.close()

    # Third column is probability of adviser giving right advice: blocks of 10 between 0.1 and 0.9
    def prob_advice(self, value):
        file_object = open(self.filename, 'a')
        file_object.write(str(value) + " \t")
        file_object.close()

    # Fourth column is colour selected by subject: 0 - blue, 1 - green
    def button_selected(self, bool):
        file_object = open(self.filename, 'a')
        file_object.write(str(bool) + " \n")
        file_object.close()

    def helpfulness(self, value):
        file_object = open(self.filename, 'a')
        file_object.write("Adviser is: " + value + "\n")
        file_object.close()

class AudioButton(Button):
    filename = StringProperty(None)
    sound = ObjectProperty(None, allownone=True)
    volume = NumericProperty(1.0)

    def play_sound(self, sug_given):
        if sug_given == "Blue.png":
            self.filename = "Blue.wav"
            self.sound = SoundLoader.load(self.filename)
            # stop the sound if it's currently playing
            self.sound.volume = self.volume
            self.sound.play()
        if sug_given == "Green.png":
            self.filename = "Green.wav"
            self.sound = SoundLoader.load(self.filename)
            # stop the sound if it's currently playing
            self.sound.volume = self.volume
            self.sound.play()

# updates IOIO.txt with the user's response of how helpful the adviser has been
class Help(FloatLayout):

    def press_helpful(self):
        ioio.helpfulness("Helpful")

    def press_misleading(self):
        ioio.helpfulness("Misleading")

    def press_indifferent(self):
        ioio.helpfulness("Indifferent")


# pop up to ask user how helpful the adviser has been
def help_adviser():
    show = Help()
    pop_help = Popup(title="Helpfulness",
                     content=show,
                     auto_dismiss=False,
                     size_hint=(None, None),
                     size=(300, 300),
                     pos_hint={"center_x": 0.5, "center_y": 0.5}
                     )

    # popup will not close unless a button is pressed
    pop_help.content.helpful.bind(on_press=pop_help.dismiss)
    pop_help.content.misleading.bind(on_press=pop_help.dismiss)
    pop_help.content.indifferent.bind(on_press=pop_help.dismiss)

    pop_help.open()


class Warning(FloatLayout):
    pass


# popup to show warning that pressing quit button will reset the user's progress
def show_warning():
    show = Warning()
    popupWindow = Popup(title="Warning",
                        content=show,
                        size_hint=(None, None),
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                        size=(300, 200),
                        )
    popupWindow.open()

class IOManager(object):

    def __init__(self, filename, ip):
        self.filename = filename
        self.str = ''
        self.rsp = ''
        self.results = []
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger = logging.getLogger('client')
        self.asString()
        self.connectTo(ip)
        self.sendMsg()
        self.rcvMsg()
        self.closeConn()
        self.asArray()


    def connectTo(self, ip):
        port = 65000

        self.logger.info('Server on %s:%s', ip, port)

        # Connect to the server
        self.logger.debug('creating socket')

        self.logger.debug('connecting to server')
        self.s.connect((ip, port))

    def asString(self):
        with open(self.filename, 'r') as file:
            self.str = file.read().replace('\n', '')

    def sendMsg(self):
        self.logger.debug('sending data:')
        self.s.send(bytes(self.str,'utf-8'))

    def rcvMsg(self):
        self.logger.debug('waiting for response')
        self.rsp = self.s.recv(1024)
        self.logger.debug('response from server')

    def asArray(self):
        r = self.rsp.decode('utf-8')
        r = r.replace('nan,','')
        r = r.replace('[','')
        r = r.replace(']','')
        r = r.replace(' ','')
        r = r.split(',')
        r = [float(e) for e in r]
        self.results = r

    def closeConn(self):
        self.logger.debug('closing socket')
        self.s.close()
        self.logger.debug('done')

    def getResults(self):
        return self.results


class WindowManager(ScreenManager):
    pass

def press_to_start():
    pop = Popup(title='Start',
                content=Label(text='Press the BLUE or GREEN \n button to start the game'),
                size_hint=(None, None),
                size=(200, 200),
                pos_hint={"center_x": 0.5, "center_y": 0.5}
                )
    pop.open()

# links the kv file which contains all of the styling and formatting for the game
kv = Builder.load_file("my.kv")
sm = WindowManager()
db = DataBase(filename=r'data/' + DataBase.get_date() + '_' + str(randint(0,10000)) +".txt")
ioio = DataBase(r'data/IOIO.txt')
#db = DataBase("../IOIO_Results/data/" + DataBase.get_date() + "_" + DataBase.get_time() + ".txt")
#ioio = DataBase("../IOIO_Results/data/IOIO.txt")
res = ResultsWindow(name="results")
screens = [Intro1(name='Intro1'), Intro2(name='Intro2'), Intro3(name='Intro3'), NewWindow(name="new"), GameWindow(name="game"),res]

for screen in screens:
    sm.add_widget(screen)

sm.current = "Intro1"


# builds the screen manager
class IOIOApp(App):
    def build(self):
        return sm


# launches the app
if __name__ == '__main__':
    IOIOApp().run()
