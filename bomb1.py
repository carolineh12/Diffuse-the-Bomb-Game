######################
# CSC 102 Bomb Project
######################

# imports
from tkinter import *
import tkinter
from threading import Thread
from time import sleep
# also, import the configs file
from bomb_configs1 import *

#########
# classes
#########
# the LCD display "GUI"
class Lcd(Frame):
    def __init__(self, window):
        super().__init__(window, bg="black")
        # make the GUI fullscreen
        window.attributes("-fullscreen", True)
        self._timer = None  # a copy of the timer on the 7-segment display
        self._button = None # the pushbutton's state
        # setup the GUI
        self.setupBoot()

    # sets up the LCD "GUI" for the initial "bootup"
    def setupBoot(self):
        # set column weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.pack(fill=BOTH, expand=True)
        self._lscroll = Label(self, bg="black", fg="white", font=("Courier New", 14), text="", justify=LEFT)
        self._lscroll.grid(row=0, column=0, columnspan=3, sticky=W)

    # sets up the LCD "GUI"
    def setup(self):
        # the timer
        self._ltimer = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Time left: ")
        self._ltimer.grid(row=1, column=0, columnspan=3, sticky=W)
        # the keypad passphrase
        self._lkeypad = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Keypad phase: ")
        self._lkeypad.grid(row=2, column=0, columnspan=3, sticky=W)
        # the jumper wires status
        self._lwires = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Wires phase: ")
        self._lwires.grid(row=3, column=0, columnspan=3, sticky=W)
        # the pushbutton status
        self._lbutton = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Button phase: ")
        self._lbutton.grid(row=4, column=0, columnspan=3, sticky=W)
        # the toggle switches status
        self._ltoggles = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Toggles phase: ")
        self._ltoggles.grid(row=5, column=0, columnspan=2, sticky=W)
        # the strikes
        self._lstrikes = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Strikes: 0")
        self._lstrikes.grid(row=5, column=2, sticky=W)
        if (SHOW_BUTTONS):
            # the pause button (pauses the timer)
            self._lpause = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Pause", justify=CENTER, command=self.pause)
            self._lpause.grid(row=6, column=0, sticky=W, padx=25, pady=40)
            # the quit button
            self._lquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", justify=CENTER, command=self.quit)
            self._lquit.grid(row=6, column=2, sticky=W, padx=25, pady=40)

    # binds the 7-segment display component to the GUI
    def setTimer(self, timer):
        self._timer = timer

    # binds the pushbutton component to the GUI
    def setButton(self, button):
        self._button = button

    # pauses the timer
    def pause(self):
        if (RPi):
            self._timer.pause()

    # quits the GUI, resetting some components
    def quit(self):
        if (RPi):
            # turn off the 7-segment display
            self._timer._display.blink_rate = 0
            self._timer._display.fill(0)
            # turn off the pushbutton's LED
            for pin in self._button._rgb:
                pin.value = True
        # close the GUI
        exit(0)

# template (superclass) for various bomb components/phases
class PhaseThread(Thread):
    def __init__(self, name):
        super().__init__(name=name, daemon=True)
        self._running = False
        self._value = None # phases can have values (e.g., a pushbutton can be True or False, a keypad passphrase can be some string, etc)

    # resets the phase's value
    def reset(self):
        self._value = None

# the timer phase
class Timer(PhaseThread):
    def __init__(self, value, display, name="Timer"):
        super().__init__(name)
        self._value = value
        self._display = display # the LCD display object
        self._paused = False

    # updates the timer
    def update(self):
        self._min = f"{self._value // 60}".zfill(2)
        self._sec = f"{self._value % 60}".zfill(2)

    # runs the thread
    def run(self):
        self._running = True
        while (True):
            if (not self._paused):
                # update the timer and display its value on the 7-segment display
                self.update()
                self._display.print(str(self))
                # wait 1s and continue
                sleep(1)
                if (self._value == 0):
                    break
                self._value -= 1
            else:
                sleep(0.1)
        self._running = False

    # pauses and unpauses the timer
    def pause(self):
        self._paused = not self._paused
        # blink the 7-segment display when paused
        self._display.blink_rate = (2 if self._paused else 0)

    def __str__(self):
        return f"{self._min}:{self._sec}"

# the keypad phase
class Keypad(PhaseThread):
    def __init__(self, keypad, target, name="Keypad"):
        super().__init__(name)
        self._value = ""
        self._keypad = keypad # the keypad pins
        self._target = target
        self._defused = False
        self._failed = False

    # runs the thread
    def run(self):
        self._running = True
        while (True):
            # process keys when keypad key(s) are pressed
            if (self._keypad.pressed_keys):
                # debounce
                while (self._keypad.pressed_keys):
                    try:
                        key = self._keypad.pressed_keys[0]
                    except:
                        key = ""
                    sleep(0.1)
                # log the key
                self._value += str(key)
                
                # check the combination
                if (self._value == self._target):
                    self._defused = True
                elif (self._value != self._target[0:len(self._value)]):
                    self._failed = True
            sleep(0.1)
        self._running = False

    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        return self._value

# the jumper wires phase
class Wires(PhaseThread):
    def __init__(self, pins, name="Wires"):
        super().__init__(name)
        self._value = None
        self._pins = pins # the jumper wire pins

    # runs the thread
    def run(self):
        self._running = True
        while (True):
            # get the jumper wire states (0->False, 1->True)
            self._value = int("".join([str(int(pin.value)) for pin in self._pins]), 2)
            sleep(0.1)
        self._running = False

    def __str__(self):
        return f"{bin(self._value)[2:].zfill(5)}/{self._value}"

# the pushbutton phase
class Button(PhaseThread):
    def __init__(self, state, rgb, color, target, timer, name="Button"):
        super().__init__(name)
        self._value = False
        self._state = state # the pushbutton's state pin
        self._rgb = rgb     # the pushbutton's LED pins
        self._color = color
        self._target = target
        self._timer = timer
        self._pressed = False
        self._defused = False
        self._failed = False

    # runs the thread
    def run(self):
        self._running = True
        # set the LED to a random color
        self._rgb[0].value = False if self._color == "R" else True
        self._rgb[1].value = False if self._color == "G" else True
        self._rgb[2].value = False if self._color == "B" else True
        while (True):
            # get the pushbutton's state
            self._value = self._state.value
            # it's pressed
            if (self._value):
                # note it
                self._pressed = True
            # it's released
            else:
                # was it already pressed?
                if (self._pressed):
                    # check the release parameters
                    # for R, nothing else is needed
                    # for G or B, a specific value must be in the timer when released
                    if (not self._target or self._target in self._timer._sec):
                        self._defused = True
                    else:
                        self._failed = True
                    self._pressed = False
                                                
            sleep(0.1)
        self._running = False

    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        return str("Pressed" if self._value else "Released")

# the toggle switches phase
class Toggles(PhaseThread):
    def __init__(self, pins, name="Toggles"):
        super().__init__(name)
        self._value = None
        self._pins = pins # the toggle switch pins

    # runs the thread
    def run(self):
        self._running = True
        while (True):
            # get the toggle switch states (0->False, 1->True)
            self._value = int("".join([str(int(pin.value)) for pin in self._pins]), 2)
            sleep(0.1)
        self._running = False

    def __str__(self):
        return f"{bin(self._value)[2:].zfill(5)}/{self._value}"

###########
# functions
###########
# generates the bootup sequence on the LCD
def bootup(n=0):
    # if we're not animating (or we're at the end of the bootup text)
    if (not ANIMATE or n == len(boot_text)):
        if (not ANIMATE):
            gui._lscroll["text"] = boot_text.replace("\x00", "")
        # configure the remaining GUI widgets
        gui.setup()
        # setup the phase threads, execute them, and check their statuses
        if (RPi):
            setup_phases()
            check_phases()
    # we're animating
    else:
        # \x00 is a longer pause in the scrolling, so don't render it
        if (boot_text[n] != "\x00"):
            gui._lscroll["text"] += boot_text[n]

        # scroll the next character after a delay
        gui.after(25 if boot_text[n] != "\x00" else 1000, bootup, n + 1)

# sets up the phase threads
def setup_phases():
    global timer, keypad, wires, button, toggles
    
    # setup the timer thread
    timer = Timer(COUNTDOWN, display)
    # bind the 7-segment display to the LCD GUI
    gui.setTimer(timer)
    # setup the keypad thread
    keypad = Keypad(matrix_keypad, keypad_target)
    # setup the jumper wires thread
    wires = Wires(wire_pins)
    # setup the pushbutton thread
    button = Button(button_input, button_RGB, button_color, button_target, timer)
    # bind the pushbutton to the LCD GUI
    gui.setButton(button)
    # setup the toggle switches thread
    toggles = Toggles(toggle_pins)

    # start the phase threads
    timer.start()
    keypad.start()
    wires.start()
    button.start()
    toggles.start()

# checks the phase threads
def check_phases():
    global strikes
    
    # check the countdown
    if (timer._running):
        # update the GUI
        gui._ltimer["text"] = f"Time left: {timer}"
    else:
        # if the countdown has expired, quit
        quit()
    # check the keypad
    if (keypad._running):
        # update the GUI
        gui._lkeypad["text"] = f"Combination: {keypad}" + (f" (target={keypad_target})" if DEBUG else "")
        # check the phase
        if (keypad._defused):
            keypad._running = False
        elif (keypad._failed):
            strikes += 1
            keypad._failed = False
            keypad._value = ""
    # check the wires
    if (wires._running):
        # update the GUI
        gui._lwires["text"] = f"Wires: {wires}" + (f" (target={bin(wires_target)[2:].zfill(5)}/{wires_target})" if DEBUG else "")
    # check the button
    if (button._running):
        # update the GUI
        gui._lbutton["text"] = f"Button: {button}"
        # check the phase
        if (button._defused):
            button._running = False
        elif (button._failed):
            strikes += 1
            button._failed = False
    # check the toggles
    if (toggles._running):
        # update the GUI
        gui._ltoggles["text"] = f"Toggles: {toggles}" + (f" (target={bin(toggles_target)[2:].zfill(4)}/{toggles_target})" if DEBUG else "")
    # note the strikes
    gui._lstrikes["text"] = f"Strikes: {strikes}"

    # too many strikes -> explode!
    if (strikes == STRIKES):
        print("EXPLODE!")
        pass
    
    # check again after a delay
    gui.after(100, check_phases)

# quits the bomb
def quit():
    # turn off the 7-segment display
    display.blink_rate = 0
    display.fill(0)
    # turn off the pushbutton's LED
    for pin in button._rgb:
        pin.value = True
    # destroy the GUI and exit the program
    window.destroy()
    exit(0)

######
# MAIN
######

# initialize the LCD GUI
window = Tk()
gui = Lcd(window)

# initialize the strikes
strikes = 0

# "boot" the bomb
gui.after(1000, bootup)

# display the LCD GUI
window.mainloop()
