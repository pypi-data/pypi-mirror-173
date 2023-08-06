from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

def chat(delay: float):
    slot_1 = ""
    slot_2 = ""
    slot_3 = ""
    slot_4 = ""
    slot_5 = ""
    while True:
        autochat = input("What do you wan't to do? edit/play/view/exit ")
        if autochat == "edit":
            while True:
                slot = input("What slot do you wan't to change? 1..5/exit ")
                if slot == '1':
                    slot_1 = input("What message do you wan't to put in slot one? ")
                if slot == '2':
                    slot_2 = input("What message do you wan't to put in slot two? ")
                if slot == '3':
                    slot_3 = input("What message do you wan't to put in slot three? ")
                if slot == '4':
                    slot_4 = input("What message do you wan't to put in slot four? ")
                if slot == '5':
                    slot_5 = input("What message do you wan't to put in slot five? ")
                if slot == 'exit':
                    print("")
                    break
        if autochat == "play":
            while True:
                slot = input("What slot do you wan't to play? 1..5/exit ")
                if slot == "1":
                    a = [*slot_1]
                    time.sleep(delay)
                    for x in range(len(a)):
                        keyboard.press(a[x])
                        keyboard.release(a[x])
                if slot == "2":
                    a = [*slot_2]
                    time.sleep(delay)
                    for x in range(len(a)):
                        keyboard.press(a[x])
                        keyboard.release(a[x])
                if slot == "3":
                    a = [*slot_3]
                    time.sleep(delay)
                    for x in range(len(a)):
                        keyboard.press(a[x])
                        keyboard.release(a[x])
                if slot == "4":
                    a = [*slot_4]
                    time.sleep(delay)
                    for x in range(len(a)):
                        keyboard.press(a[x])
                        keyboard.release(a[x])
                if slot == "5":
                    a = [*slot_5]
                    time.sleep(delay)
                    for x in range(len(a)):
                        keyboard.press(a[x])
                        keyboard.release(a[x])
                if slot == 'exit':
                    print("")
                    break
        if autochat == 'view':
            if slot_1 == "":
                print("There is nothing in slot one")
            else:
                print("in slot one is: ", slot_1)
            if slot_2 == "":
                print("There is nothing in slot two")
            else:
                print("in slot two is: ", slot_2)
            if slot_3 == "":
                print("There is nothing in slot three")
            else:
                print("in slot three is: ", slot_3)
            if slot_4 == "":
                print("There is nothing in slot four")
            else:
                print("in slot four is: ", slot_4)
            if slot_5 == "":
                print("There is nothing in slot five")
            else:
                print("in slot five is: ", slot_5)
        if autochat == 'exit':
            print("")
            break

def spam(num: float, speed: float, delay: float):
    if input("Use at your own risk. proceed? y/n ") == "y":
        time.sleep(delay)
        for i in range(0,num):
            keyboard.press(Key.ctrl)
            keyboard.press('v')
            keyboard.release(Key.ctrl)
            keyboard.release('v')
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(speed)