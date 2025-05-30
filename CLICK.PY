#pip install pyautogui
#instll above library
#this below code is for clicking a point what uwant in screen with input x and y cordinate and clicking interval and total duration 


import pyautogui
import time

def mouse_clicker(x, y, duration, interval):
    """
    Clicks the mouse at a specific (x, y) coordinate for a given duration
    with a specified interval between clicks.

    Args:
        x (int): The x-coordinate of the click.
        y (int): The y-coordinate of the click.
        duration (int): The total time in seconds to perform clicks.
        interval (float): The time in seconds between each click.
    """
    start_time = time.time()
    while time.time() - start_time < duration:
        pyautogui.click(x, y)
        time.sleep(interval)

if __name__ == "__main__":
    print("Please provide the coordinates, duration, and interval for the mouse clicks.")
    try:
        click_x = int(input("Enter the x-coordinate: "))
        click_y = int(input("Enter the y-coordinate: "))
        click_duration = int(input("Enter the total duration in seconds: "))
        click_interval = float(input("Enter the interval between clicks in seconds: "))

        print(f"\nMouse will start clicking at ({click_x}, {click_y}) every {click_interval} seconds for {click_duration} seconds.")
        input("Press Enter to start the mouse clicking...")
        mouse_clicker(click_x, click_y, click_duration, click_interval)
        print("\nMouse clicking finished.")

    except ValueError:
        print("Invalid input. Please enter numeric values for coordinates, duration, and interval.")
    except KeyboardInterrupt:
        print("\nMouse clicking interrupted by the user.")
