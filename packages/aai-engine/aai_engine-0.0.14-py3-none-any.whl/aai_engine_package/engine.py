"""""" #Left empty because its prettier in mkdocs
from csv import get_dialect
from tabnanny import check
import pyautogui
import sys
import time
import random
import os
import json
import platform
import subprocess
import pandas as pd
import numpy as np
from random import choice
from string import digits
from datetime import datetime
import tempfile
import yaml
import traceback
import cv2

from .engine_util import locate_on_screen, screenshot, locate
from .engine_util import LARGE_FONT, NORM_FONT, SMALL_FONT, REGION_PICK_VIEW, OFFSET_PICK_VIEW, SIMILARITY_PICK_VIEW, NAME_PICK_VIEW
from cron_descriptor import get_description

import collections
Box = collections.namedtuple('Box', 'left top width height')

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

import tkinter
from tkinter import ttk
from PIL import Image, ImageTk, ImageGrab
from PIL.PngImagePlugin import PngImageFile, PngInfo

try:
    from aai_engine_package.screenshot_taker import ScreenShotTaker
except:
    from src.aai_engine_package.screenshot_taker import ScreenShotTaker

import logging
import zmq

logging.basicConfig(
        format='%(asctime)s: %(levelname)s %(message)s',
        level=logging.INFO,
        datefmt='%H:%M:%S'
    )

REQUEST_TIMEOUT = 2500
REQUEST_RETRIES = 3

ZMQ_PORT = 5555
ZMQ_MSG_TYPE_PROGRESS = "progress"
ZMQ_MSG_TYPE_DATA = "data"

pyautogui.FAILSAFE = True

CWD = os.getcwd()

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
REL_PATH = "my_screenshot.png"
abs_file_path = os.path.join(script_dir, REL_PATH)
SCREENSHOT = abs_file_path

dirname = os.path.dirname(__file__)
if os.name == "posix":
    icon_path = os.path.join(dirname, r'style/icon.ico')
    theme_path = os.path.join(dirname, r'style/sun-valley.tcl')
else:
    icon_path = os.path.join(dirname, r'style\icon.ico')
    theme_path = os.path.join(dirname, r'style\sun-valley.tcl')

# Global variables to check if internal display is used as main display on OSX. Needed because of bug which causes the
# screen resolution to be doubled when said condition is met.
USING_OSX = os.name == 'posix' and platform.system() == "Darwin"
USING_INTERNAL_DISPLAY_AS_MAIN_ON_OSX = False

FILLING_SPACE = 103


def internal_display_used_as_main_on_osx() -> bool:
        '''
        Checks if internal display is used as main display on macOS
        '''
        if not USING_OSX:
            return False

        # read display information on mac
        display_profiler_output = json.loads(subprocess.getoutput('system_profiler SPDisplaysDataType -json'))

        # search for info object for internal display
        display_infos = display_profiler_output['SPDisplaysDataType'][0]['spdisplays_ndrvs']
        internal_display_as_main = False
        i = 0
        while i < len(display_infos) and not internal_display_as_main:
            display_info = display_infos[i]
            internal_display_as_main = 'spdisplays_connection_type' in display_info \
                and display_info['spdisplays_connection_type'] == 'spdisplays_internal' \
                and 'spdisplays_main' in display_info \
                and display_info['spdisplays_main'] == 'spdisplays_yes'
            i += 1

        return internal_display_as_main


def get_zmq_client_socket():
    """Establishes ZMQ connection with engine manager process and returns Socket"""
    logging.info("Connecting to ZMQ client socket…")
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{ZMQ_PORT}")
    return socket


class TaskWrapper():
    """
    Task wrapper class to control execution
    """

    def __init__(self, task_id, name, cwd, script, scheduled_time, execution_type=-1, trigger=lambda _: True):
        self.task_id = task_id
        self.name = name
        self.cwd = cwd
        self.steps = []
        self.script = script
        self.scheduled_time = scheduled_time
        self.execution_type = execution_type
        self.trigger = trigger
        self.log_dir = os.path.join(cwd, 'logs', self.name)
        self.log_time = None

        self.init_log_dir()

    def execute(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: Executing task script")

        filepath=self.script # TODO: checks on file

        # info = subprocess.STARTUPINFO()
        # info.dwFlags = subprocess.STARTUPINFO()
        # info.wShowWindow = SW_MINIMIZE

        self.log_time = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')
        log_file_stdout = os.path.join(self.log_dir, self.log_time + "stdout.txt")
        log_file_stderr = os.path.join(self.log_dir, self.log_time + "stdinfo.txt")

        with open(log_file_stdout, "w+", encoding="utf-8") as stdout_log_file, open(log_file_stderr, "w+", encoding="utf-8") as stderr_log_file:
            # check if python command exists on current machine and has version 3.x, otherwise run python3
            status, output = subprocess.getstatusoutput('python --version')
            if status == 0 and output.startswith("Python 3"):
                return subprocess.Popen(
                    ['python', filepath], cwd=self.cwd, stdout=stdout_log_file,
                    stderr=stderr_log_file, shell=False) #, startupinfo=info)

            return subprocess.Popen(['python3', filepath], cwd=self.cwd, stdout=stdout_log_file, stderr=stderr_log_file, shell=False) #, startupinfo=info)

    def __str__(self) -> str:
        """str format for TaskWrapper"""
        if self.execution_type == 'SC':
            return f"ID:{self.task_id} = {self.name}||scheduled at: {get_description(self.scheduled_time)}"
        if self.execution_type == 'MA':
            return f"ID:{self.task_id} = {self.name}||scheduled at: manually"
        return f"ID:{self.task_id} = {self.name}||scheduled at: continuously"

    def init_log_dir(self):
        """Init log directory
        """
        if not os.path.isdir(self.log_dir):
            original_umask = os.umask(0)
            try:
                os.makedirs(self.log_dir, 0o777)
            finally:
                os.umask(original_umask)


class Task():
    """
    Task class to control and keep track of all information and steps within a task.
    """
    def __init__(self, name, cwd, script=None, standalone=False):
        """

        Args:
            name (str): Name of the task.
            cwd (str): The current working directory.
            script (str, optional): Optional path to a script you can provide for the give task. If a script is given this will override the steps that are listed in the task. Defaults to None.
            standalone (bool, optional): Put this value to True if you run your robot independently without the task manager. Defaults to False.
        """
        self.name = name
        self.cwd = cwd
        self.steps = []
        self.script = script
        self.execution_log_file = None
        self.log_time = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')
        self.execution_log_file = os.path.join(cwd, 'logs', self.name , self.log_time + "execution_log.txt")
        self.standalone = standalone
        self._data = {}  # task-specific data
        self.zmq_client_socket = get_zmq_client_socket()
        self.last_box_location = None
        self.error = False

        self._init_log_dir()
        self._print_title()


    def add_step(self, step):
        """Add a step to the current list of steps.

        Args:
            step (Step): The step you want to add.
        """
        self.steps.append(step)
        step.set_task(self)

    def execute(self):
        """Execute all steps within this task"""

        # Only check if internal display is used as main on OSX once per task execution for efficiency reasons
        global USING_INTERNAL_DISPLAY_AS_MAIN_ON_OSX
        USING_INTERNAL_DISPLAY_AS_MAIN_ON_OSX = internal_display_used_as_main_on_osx()

        if self.script is None:
            self.error = False
            self._update_progress(f"0/{len(self.steps)}")
            for idx, step in enumerate(self.steps):
                self._print_step(step,idx)
                step.execute()
                if not self.standalone:
                    self._update_progress(f"{idx + 1}/{len(self.steps)}")
            if not self.error:
                print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: TASK SUCCESSFULLY FINISHED!\n")
                self._log("TASK SUCCESSFULLY FINISHED!\n")
            if not self.standalone:
                # task finished, send task data as JSON string to engine manager process
                # TODO maybe don't send task data immediately but allow control for when this happens outside of this function?
                self._send_task_data()
        else:
            # For legacy scripts or external scripts outside the engine
            print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: Executing script")
            filepath=self.script # TODO: checks on file
            proc = subprocess.Popen(filepath, shell=True, stdout=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: return code={proc.returncode}") # is 0 if success

    def _task_failed(self):
        """Function that logs the most important things after a failure
        """
        self.error = True
        screenshot_path = os.path.join(self.cwd, 'logs', self.name, self.log_time + ".png")
        try:
            img = PngImageFile(os.path.join(self.cwd,".temp_screenshot.png"))
            img.save(screenshot_path)
        except Exception as ex:
            screenshot_path = "No screenshot could be found"
        self._log(f"The last screenshot can be found at: {screenshot_path}", time=False)
        self._log(f"The last box was: {self.last_box_location}", time=False)
        self._log(f"TASK FAILED!")

    def _set_last_box_location(self, new_box_location):
        """Setter for the last box location used for logging purposes

        Args:
            new_box_location (Box): new box location
        """
        self.last_box_location = new_box_location

    def _print_step(self,step, idx):
        """Print the current step information

        Args:
            step (Step): The step we want to log
            idx (int): Step number
        """
        self._log("-"*(len(self.name) + FILLING_SPACE), time=False)
        self._log("\tExecuting step ({idx}/{total}) - {name}".format(idx=(idx+1), total=len(self.steps), name=step.name), time=False)
        self._log("-"*(len(self.name) + FILLING_SPACE), time=False)

    def _print_title(self):
        """Log the title of the task in the execution logs
        """
        title_length = len(self.name) + FILLING_SPACE
        s_char = "="
        str1 = s_char*int((FILLING_SPACE - len("Task Name: "))/2)
        str2 = s_char*title_length
        self._log(str2, time=False)
        self._log(str1 + "Task Name: " + self.name + str1, time=False)
        self._log(str2, time=False)

    def _init_log_dir(self):
        """Initializes the logging dir
        """
        if not os.path.isdir(os.path.join(self.cwd, 'logs', self.name)):
            original_umask = os.umask(0)
            try:
                os.makedirs(os.path.join(self.cwd, 'logs', self.name), 0o777)
            finally:
                os.umask(original_umask)

    def _log(self, line, time=True):
        """Log the execution process
        """
        with open(self.execution_log_file, "a+", encoding="utf-8") as file:
            if time:
                now = datetime.strftime(datetime.now(), '%H:%M:%S') + ": "
            else:
                now = ""
            file.write(now + line + "\n")

    def _update_progress(self, progress):
        """Update progress on task

        Args:
            progress (str): Description of the current progress
        """
        request = json.dumps({"type": ZMQ_MSG_TYPE_PROGRESS, "msg": progress}, ensure_ascii=False).encode('utf8')
        logging.info("Sending (%s)", request)
        self.zmq_client_socket.send(request)
        logging.info("Waiting for reply")
        while True:
            logging.info("Polling server")
            if (self.zmq_client_socket.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
                reply = self.zmq_client_socket.recv()
                logging.info("Server replied OK (%s)", reply)

                break

    def _send_task_data(self):
        '''Send task data to ZMQ server'''
        logging.info("Sending task data")
        msg = {"type": ZMQ_MSG_TYPE_DATA, "msg": self._data}
        self.zmq_client_socket.send_json(msg, ensure_ascii=False)
        reply = self.zmq_client_socket.recv()
        logging.info(f"Server replied: {reply}")

    def set_data_item(self, key, val):
        """Set key-value pair in task data"""
        self._data[key] = val

    def get_data_item(self, key):
        """Get item with given key from task data"""
        return self._data[key]

    def get_data(self):
        """Get task data"""
        return self._data

    # ENGINE FUNCTIONS
    def click(self, img_location):
        """Calls engine.click
        """
        click(img_location, task=self)
        self._log(f"-> click on {img_location} located at {self.last_box_location}")

    def click_right(self, img_location):
        """Calls engine.click_right
        """
        click_right(img_location, task=self)
        self._log(f"-> right click on {img_location} located at {self.last_box_location}")

    def double_click(self, img_location):
        """Calls engine.double_click
        """
        double_click(img_location, task=self)
        self._log(f"-> double click on {img_location} located at {self.last_box_location}")

    def click_n(self, img_location, nr_clicks, button='left'):
        """Calls engine.click_n
        """
        click_n(img_location, nr_clicks, button=button, task=self)
        self._log(f"-> click {button}, {nr_clicks} times on {img_location} located at {self.last_box_location}")

    def exists(self, img_location):
        """Calls engine.exists
        """
        self._log("-> check if image exists")
        return exists(img_location, task=self)

    def get_box_location(self, img_location,haystack=None,iterations=5,steps_per_iteration=4,cache_confidence=True,debug=False):
        """Calls engine.get_box_location
        """
        return get_box_location(img_location,haystack=haystack,iterations=iterations,steps_per_iteration=steps_per_iteration,cache_confidence=cache_confidence,debug=debug, task=self)

    def check_boxes_list(self, boxes,limit=5, treshold=10):
        """Calls engine.check_box_list
        """
        self._log("-> Verify how close boxes are")
        return check_boxes_list(boxes, limit=limit, treshold=treshold, task=self)

    def wait(self,img_location, seconds):
        """Calls engine.wait
        """
        self._log(f"-> Wait for {seconds}s, then try to find the image")
        wait(img_location, seconds, task=self)

    def sleep(self, seconds):
        """Calls engine.sleep
        """
        self._log(f"-> sleep for {seconds}s")
        sleep(seconds, task=self)

    def type_text(self, text):
        """Calls engine.type_text
        """
        self._log(f"-> Write '{text}'")
        type_text(text, task=self)

    def key_combo(self, *keys):
        """Calls engine.key_combo
        """
        self._log(f"-> click_right")
        key_combo(*keys, task=self)

    def remove_char(self, nr_characters=1):
        """Calls engine.remove_char
        """
        remove_char(nr_characters=nr_characters, task=self)

    def copy_to_clipboard(self):
        """Calls engine.copy_to_clipboard
        """
        self._log(f"-> Copy to clipboard")
        copy_to_clipboard(task=self)

    def get_clipboard(self):
        """Calls engine.get_clipboard
        """
        self._log(f"-> Get clipboard contents")
        return get_clipboard(task=self)

    def read_excel(self, path):
        """Calls engine.read_excel
        """
        self._log(f"-> Read excel file")
        result = read_excel(path, task=self)
        self._log(f"\tDATA from {path}: ", time=False)
        for point in result:
            self._log("\t\t" + str(point), time=False)
        return result


class Step():
    """
    Keep track of a certain step within a task
    """

    def __init__(self, name, func, *args):
        self.name = name
        self.func = func
        self.args = args
        self.task = None  # Task object which the step is part of

    def execute(self):
        """Execute the step
        """
        try:
            self.func(self.task, *self.args)
        except Exception as ex:
            self.task._log("ERROR: ")
            self.task._log(traceback.format_exc(), time=False)
            self.task._task_failed()

    def set_task(self, task):
        """Set the step's corresponding Task"""
        self.task = task


def click(img_location,task=None):
    """Locate the given image on the screen and click it. Calls click_n.


    Args:
        img_location (str): Location of the image that needs to be clicked
        task (Task, optional): Task object to log the information of this function. Defaults to None.
    """
    click_n(img_location, 1, task=task)


def click_right(img_location, task=None):
    """Locate the given image on the screen and right click it. Calls click_n.


    Args:
        img_location (str): Location of the image that needs to be clicked
        task (Task, optional): Task object to log the information of this function. Defaults to None.
    """
    click_n(img_location, 1, button="right", task=task)


def double_click(img_location, task=None):
    """Locate the given image on the screen and double click it. Calls click_n.


    Args:
        img_location (str): Location of the image that needs to be clicked
        task (Task, optional): Task object to log the information of this function. Defaults to None.
    """
    click_n(img_location, 2, task=task)

def click_n(img_location, nr_clicks, button='left', task=None):
    """This function will try to find the image on the screen. If the image is found, a click event happens on the provided location offset.
       This offset is saved in the image metadata as: 'offset_x' and 'offset_y'.
    Args:
        img_location (str): The location of the image that you want to find on the screen.
        nr_clicks (int): Amount of times the image needs to be clicked.
        button (str, optional): Type of click [left,right,middle]. Defaults to 'left'.
        task (Task, optional): Task object to log the information of this function. Defaults to None.

    Raises:
        RuntimeError: Raised when the image is not find on the current screen.
    """
    full_file_path = '/'.join([CWD, img_location])
    img = PngImageFile(full_file_path)
    print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: Trying to click on {img_location}")
    print(f"\t image metadata: {img.text}")

    haystack = screenshot(CWD + "/.temp_screenshot.png")

    if task:
        box_location = get_box_location(img_location,haystack=haystack,cache_confidence=True, task=task)
    else:
        box_location = get_box_location(img_location,haystack=haystack,cache_confidence=True)

    if box_location is None:
        raise RuntimeError("Image not found on current screen.")

    print(f"\tImage found on screen at: {box_location}")

    x_coord = int(float(img.text["offset_x"]))
    y_coord = int(float(img.text["offset_y"]))

    if USING_INTERNAL_DISPLAY_AS_MAIN_ON_OSX:
        # resolution is half the size on macos when using internal display as main screen
        x_coord /= 2
        y_coord /= 2
        x_coord += (box_location.left + box_location.width / 2) / 2
        y_coord += (box_location.top + box_location.height / 2) / 2
    else:
        x_coord += box_location.left + box_location.width / 2
        y_coord += box_location.top + box_location.height / 2

    for _ in range(0,nr_clicks):
        pyautogui.click(x=x_coord,
                        y=y_coord,
                        button=button)
    print(f"\tClicked: {img_location}")


def exists(img_location, task=None):
    """Checks if a given image exists on the screen.

    Args:
        img_location (str): Path to the image.
        task (Task, optional): Task object to log the information of this function. Defaults to None.
    Returns:
        exist(bool): True if the image exists, False otherwise.
    """
    return get_box_location(img_location, task=task) is not None


def get_box_location(img_location,haystack=None,iterations=5,steps_per_iteration=4,cache_confidence=True,debug=False, task=None):
    """Checks if the images exists on the current screen or haystack image, and returns the box location

    Args:
        img_location (str): Path to the needle image (Image to be found on the screen)
        haystack (str, optional): Image where the needle image needs to be found. Defaults to None.
        iterations (int, optional): Maximum iterations of the algorithm. Defaults to 5.
        steps_per_iteration (int, optional): Amount of steps per iteration. This determines the step size of the confidence values. Defaults to 4.
        cache_confidence (bool, optional): Tells to this algorithm to look for a cache confidence value before running the iterations. Defaults to True.
        debug (bool, optional): Debug toggle for logging some useful information about the process. Defaults to False.
        task (Task, optional): Task object to log the information of this function. Defaults to None.

    Returns:
        box_location(Box): The location of the box that was found by the algorithm
    """
    full_file_path = '/'.join([CWD, img_location])
    img = PngImageFile(full_file_path)
    upper_confidence = float(img.text["upper_confidence"])
    lower_confidence = float(img.text["lower_confidence"])

    box_location = None
    print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: Trying to find the image on the screen")
    # CHECK IF CONFIDENCE VALUE IS CACHED
    if cache_confidence:
        try:
            confidence = float(img.text['cached_confidence'])
            print(f"\tCached confidence available: {confidence}")
            if haystack:
                box_location = locate(img, haystack_image=haystack, confidence=float(confidence))
            else:
                box_location = locate_on_screen(full_file_path, confidence=float(confidence))
            if box_location and not isinstance(box_location,list):
                print(f"\tbox found in cache!")
                if task:
                    task._set_last_box_location(box_location)
                return box_location
        except Exception as ex:
            print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: An error occured while searching for the image")

    # ITERATE OVER SEVERAL RANGES UNTIL BOX IS FOUND OR MAX ITERATIONS IS EXCEEDED
    if debug:
        print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: Executing the dynamic confidence finder algorithm")
    for iteration in range(iterations):
        step_size = (upper_confidence - lower_confidence)/(steps_per_iteration*1.0)
        upper_confidence_fixated = upper_confidence
        if debug:
            print(f"ITERATION: {iteration}")
            print(f"\tcurrent step size: {step_size:.2f}")
            print(f"\tcurrent upper bound: {upper_confidence:.2f}")
            print(f"\tcurrent lower bound: {lower_confidence:.2f}\n")


        for i in range(steps_per_iteration):
            # Try to find a single box for the current needle
            current_confidence = upper_confidence_fixated - i*step_size
            if debug:
                print(f"\tSTEP {i}")
                print(f"\t\tConfidence value: {current_confidence}")
            try:
                if haystack:
                    box_location = locate(img, haystack_image=haystack, confidence=float(current_confidence))
                else:
                    box_location = locate_on_screen(full_file_path, confidence=float(current_confidence))
            except Exception as ex:
                pass

            # Check the box_location
            if not box_location:
                # The confidence was too high and the new upperbound of the confidence should be lowered!
                upper_confidence = current_confidence
                if debug:
                    print(f"\t\tnew upper: {upper_confidence}")
            elif isinstance(box_location,list):
                if debug:
                    print(f"\t\tToo many boxes: {len(box_location)}")
                # If box_location is array, more than 1 match is found -> lower confidence bound should be raised + break the inner for loop!
                lower_confidence = current_confidence
                break
            else:
                # Box location exists and is singular -> return the box + cache the found confidence value if cache=True!
                if cache_confidence:
                    info = PngInfo()
                    for key,value in img.text.items():
                        info.add_text(key,value)
                    info.add_text('cached_confidence',str(current_confidence))
                    img.save('/'.join([CWD, img_location]),pnginfo=info)
                if task:
                    task._set_last_box_location(box_location)
                return box_location

    # If max iterations is exceeded and multiple boxes remain: Check if they are close to each other and if so, return the first box
    if box_location:
        if task:
            task._set_last_box_location(box_location)
        return check_boxes_list(box_location, task=task)

    if task:
        task._set_last_box_location(None)
    return None

def check_boxes_list(boxes,limit=5, treshold=10, task=None):
    """Checks if the box locations are close to each other. Returns the first box if they are close.
       Otherwise it will return None.

    Args:
        boxes (list): list of box locations
        limit (int, optional): Limit of boxes to take into consideration. Defaults to 5.
        treshold (int, optional): Treshold for the similarity metric. Defaults to 10.
        task (Task, optional): Task object to log the information of this function. Defaults to None.

    Returns:
        Box(Box): The final box location or None if they are too far apart
    """
    # Check if amount of boxes goes over the allowed number
    print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: Check if boxes are close to each other")
    if len(boxes) > limit:
        return None

    mae = 0
    for box in boxes:
        # All boxes need to have the same dimensions
        if box.width != boxes[0].width or box.height != boxes[0].height:
            print(f"\tBoxes didn't have the same dimensions")
            return None
        if box != boxes[0]:
            mae += abs(box.left - boxes[0].left)
            mae += abs(box.top - boxes[0].top)

    print(f"\tThe MAE for this case is: {mae}")
    if mae <= treshold:
        print(f"\tThe boxes where close enough! Returning the first one.")
        return boxes[0]

    return None


def wait(img_location, seconds, task=None):
    """ Wait a given amount of seconds for a given image, checking its existence.

    Args:
        img_location (str): Path to the image.
        seconds (int): Amount of seconds to wait.
        task (Task, optional): Task object to log the information of this function. Defaults to None.

    Raises:
        RuntimeError: Raised when the image was not found.
    """
    print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: Waiting for: {img_location}")
    starttime = time.time()
    for _ in range(0, seconds):
        if exists(img_location, task=task):
            return
        time.sleep(1.0 - ((time.time() - starttime) % 1.0))
    raise RuntimeError("\tTimeout: Image not found.")


def sleep(seconds, task=None):
    """Sleep for a certain amount of time

    Args:
        seconds (int): Amount of seconds to sleep
        task (Task, optional): Task object to log the information of this function. Defaults to None.
    """
    print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: Sleeping for {seconds}s")
    time.sleep(seconds)


def type_text(text, task=None):
    """Type the given text.

    Args:
        text (str): The text to write.
        task (Task, optional): Task object to log the information of this function. Defaults to None.
    """
    print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: Write {text}")
    pyautogui.write(text)

def key_combo(*keys, task=None):
    """Type a given key comination (ctrl, shift, esc, f1, ...).

    Args:
        task (Task, optional): Task object to log the information of this function. Defaults to None.
    """
    print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: Pressing keys: {str(keys)}")
    pyautogui.hotkey(*keys)

def remove_char(nr_characters=1, task=None):
    """Remove n characters (backspace).

    Args:
        nr_characters (int, optional): Amount of characters to remove. Defaults to 1.
        task (Task, optional): Task object to log the information of this function. Defaults to None.
    """
    print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: Removing {nr_characters} characters")
    for _ in range(0, nr_characters):
        pyautogui.hotkey("backspace")


def copy_to_clipboard(task=None):
    """Copy data to clipboard

    Args:
        task (Task, optional): Task object to log the information of this function. Defaults to None.
    """
    print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: Copy to clipboard")
    tcl = tkinter.Tk()
    tcl.withdraw()
    tcl.clipboard_clear()

    data = sys.stdin.read()

    tcl.clipboard_append(data)

    if sys.platform != 'win32':
        if len(sys.argv) > 1:
            print('\tData was copied into clipboard. Paste and press ENTER to exit...')
        else:
            # stdin already read; use GUI to exit
            print('\tData was copied into clipboard. Paste, then close popup to exit...')
            tcl.deiconify()
            tcl.mainloop()
    else:
        tcl.destroy()


def get_clipboard(task=None):
    """Get clipboard text independently from the OS

    Args:
        task (Task, optional): Task object to log the information of this function. Defaults to None.

    Returns:
        str: The text in the current clipboard
    """
    print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: Get clipboard contents")
    return tkinter.Tk().clipboard_get()


### FILE READ UTILS ###
def read_excel(path, task=None):
    """Read in the data from an excel file

    Args:
        path (str): Path to the excel file
        task (Task, optional): Task object to log the information of this function. Defaults to None.. Defaults to None.

    Returns:
        Dict: A dictionary that contains the information in the excel file
    """
    print(f"{datetime.strftime(datetime.now(), '%H:%M:%S')}: Reading in excel data from {path}")
    return pd.read_excel(path).to_dict(orient='records')


def cli():
    """_summary_
    """
    if len(sys.argv) == 2:
        save_location = sys.argv[1]
        print(os.getcwd(), save_location)
    print("Called aai-engine-capture")
    main(r"H:\AdAstraIndustries\aai_engine\img")

def test_edit(save_location, param2):
    """Edit stub
    """
    pass


def edit(save_location, haystack):
    """Calls the edit routine
    """
    main(save_location, haystack, editing=True)


def main(save_location, needle=r"C:\Users\Toto\Documents\AdAstraIndustries\aai_engine\img\cv.png", editing=False):
    """main
    """
    temp_screenshot = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    temp_screenshot_path = temp_screenshot.name
    if os.name == "posix":
        temp_screenshot_path = temp_screenshot_path.split(".")[0] + "_000.png"
    print("TEMP PATH: ", temp_screenshot_path)
    take_screenshot(temp_screenshot_path)
    # take_screenshot()
    # TODO: make title bar black
    # aai_window = AAIWindow()
    # root = aai_window.root

    root = tkinter.Tk()
    style = ttk.Style(root)
    # iconfile = pkg_resources.read_binary(style_dir, 'icon.ico')
    # iconfile = pkgutil.get_data(__name__, "style/icon.ico")
    # root.wm_iconbitmap(icon_path)
    root.wm_colormapwindows()

    root.tk.call('source', theme_path)
    root.tk.call("set_theme", "dark")

    if editing:
        print(" - EDIT MODE - ")
        app = ScreenShotTaker(root, save_location, needle=needle, haystack=temp_screenshot_path,
                              editing=True)  # When editing from extension
    else:
        print(" - CREATE MODE - ")
        app = ScreenShotTaker(root, save_location, haystack=temp_screenshot_path, editing=False)

    root.mainloop()
    temp_screenshot.close()
    os.unlink(temp_screenshot.name)


class AAIWindow():
    """AAI window for the GUI
    """
    def __init__(self):
        self.root = tkinter.Tk()
        style = ttk.Style(self.root)
        self.root.wm_iconbitmap(icon_path)
        self.root.wm_colormapwindows()
        self.root.overrideredirect(True)  # turns off title bar, geometry
        self.root.geometry('400x100+200+200')  # set new geometry

        # make a frame for the title bar
        title_bar = tkinter.Frame(self.root, bg='black', relief='flat', bd=2)

        # put a close button on the title bar
        close_button = ttk.Button(title_bar, text='X', command=self.root.destroy)

        # pack the widgets
        title_bar.pack(expand=1, fill=tkinter.X)
        close_button.pack(side=tkinter.RIGHT)

        # bind title bar motion to the move window function
        title_bar.bind('<B1-Motion>', self.move_window)
        title_bar.bind('<Button-1>', self.get_pos)

        # root.configure(background='#3E4149')
        self.root.tk.call('source', theme_path)
        # root.tk.call('package', 'require', 'awdark')
        # style.theme_use('dark')
        self.root.tk.call("set_theme", "dark")

    def move_window(self, event):
        """_summary_

        Args:
            event (_type_): _description_
        """
        self.root.geometry("400x400" + '+{0}+{1}'.format(event.x_root + self.xwin, event.y_root + self.ywin))

    def get_pos(self, event):
        """_summary_

        Args:
            event (_type_): _description_
        """
        xwin = self.root.winfo_x()
        ywin = self.root.winfo_y()
        startx = event.x_root
        starty = event.y_root

        self.ywin = ywin - starty
        self.xwin = xwin - startx


def take_screenshot(file_path='my_screenshot.png'):
    """
    Take a screenshot.
    Args:

    """
    print("Taking screenshot")
    # time.sleep(3)
    img = screenshot(file_path)
    print("Done")


def take_screenshot_save(save_location):
    """
    Take a screenshot.
    Args:

    """
    print("Taking screenshot")
    # time.sleep(3)
    save_path = ''.join([save_location, "/img/aai_", ''.join(choice(digits) for i in range(12)), ".png"])
    img = screenshot(save_path)
    print("Done")


def _get_theme_path():
    return theme_path
