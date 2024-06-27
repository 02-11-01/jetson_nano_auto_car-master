from pynput import keyboard
import YB_Pcb_Car as car
import time
def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        #print(format(key.char))
        if format(key.char)=='w':
            print('running in straight direction')
            car.Car_Run(150, 150)
            time.sleep(0.1)
            car.Car_Stop()

    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()