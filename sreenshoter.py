from pynput.mouse import Listener
import pyautogui

def on_move(x, y):
    pass

def on_scroll(x, y, dx, dy):
    pass

click_counter = 0
click_arr = []

def on_click(x, y, button, pressed):
    global click_counter
    global click_arr
    if pressed:
        print ('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
        click_arr.append(x)
        click_arr.append(y)
        click_counter += 1
        if click_counter > 1:
            listener.stop()


with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()

print(click_arr)

im = pyautogui.screenshot(region=(click_arr[0], click_arr[1], abs(click_arr[2] - click_arr[0]), abs(click_arr[3] - click_arr[1])))
im.save('sc.png')
im = im.convert('1')
im.save('ss.png')