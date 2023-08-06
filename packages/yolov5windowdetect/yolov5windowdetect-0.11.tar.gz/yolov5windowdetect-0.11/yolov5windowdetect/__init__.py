import os
import random
import re
import sys
from time import sleep
from typing import Union
import keyboard
import numpy as np
import requests
import torch
from windowcapture import ScreenShots
import cv2
import pandas as pd
import PILasOPENCV
from PrettyColorPrinter import add_printer

add_printer(False)


def load_torchmodel(ptfile, repo_or_dir="./yolov5", model="custom", source="local"):
    model = torch.hub.load(repo_or_dir, model, ptfile, source=source,)
    return model


def rgb_bgr(src):
    if src.shape[1] == 3:
        dst = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    else:
        dst = cv2.cvtColor(src, cv2.COLOR_BGRA2RGB)
    return dst


def open_image_in_cv(image, channels_in_output=None):
    if isinstance(image, str):
        if os.path.exists(image):
            if os.path.isfile(image):
                image = cv2.imread(image)
        elif re.search(r"^.{1,10}://", str(image)) is not None:
            x = requests.get(image).content
            image = cv2.imdecode(np.frombuffer(x, np.uint8), cv2.IMREAD_COLOR)
        else:
            image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    elif "PIL" in str(type(image)):
        image = np.array(image)
    else:
        if image.dtype != np.uint8:
            image = image.astype(np.uint8)

    if channels_in_output is not None:
        if image.shape[-1] == 4 and channels_in_output == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        elif image.shape[-1] == 3 and channels_in_output == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        else:
            pass
    return image


def get_results_as_df(path_or_np, models, confidence_thresh):
    asnumpy = open_image_in_cv(path_or_np)
    allresu = []
    for model in models:
        results = model(asnumpy)
        df = pd.concat(results.pandas().xywhn)
        df = df.rename(
            columns={
                "xcenter": "aa_center_x",
                "ycenter": "aa_center_y",
                "width": "aa_width",
                "height": "aa_heigth",
                "confidence": "aa_confidence",
                "class": "aa_id",
                "name": "aa_name",
            }
        )
        df["aa_img_width"] = asnumpy.shape[1]
        df["aa_img_height"] = asnumpy.shape[0]
        df["aa_img_abs_center_y"] = df.aa_img_height * df.aa_center_y
        df["aa_img_abs_center_y"] = df["aa_img_abs_center_y"].astype("int")
        df["aa_img_abs_center_x"] = df.aa_img_width * df.aa_center_x
        df["aa_img_abs_center_x"] = df["aa_img_abs_center_x"].astype("int")
        df["aa_img_abs_width"] = df.aa_img_width * df.aa_width
        df["aa_img_abs_width"] = df["aa_img_abs_width"].astype(int)
        df["aa_img_abs_height"] = df.aa_img_height * df.aa_heigth
        df["aa_img_abs_height"] = df["aa_img_abs_height"].astype(int)
        df["aa_haystack_start_x"] = df.aa_img_abs_center_x - df.aa_img_abs_width // 2
        df["aa_haystack_end_x"] = df.aa_img_abs_center_x + df.aa_img_abs_width // 2
        df["aa_haystack_start_y"] = df.aa_img_abs_center_y - df.aa_img_abs_height / 2
        df["aa_haystack_end_y"] = df.aa_img_abs_center_y + df.aa_img_abs_height // 2
        df.aa_haystack_start_y = df.aa_haystack_start_y.astype(int)
        df = df.loc[df.aa_confidence >= confidence_thresh].copy()
        allresu.append(df.copy())
    df = pd.concat(allresu, ignore_index=True, axis=0).drop_duplicates().reset_index()
    return df


class Yolov5WindowDetect:
    r"""
    winca = (
        Yolov5WindowDetect(
            pt_file=r"C:\Users\Gamer\anaconda3\envs\dfdir\yolov5\runs\train\playerbutton7\weights\best.pt",
            repo_or_dir="./yolov5",
            model="custom",
            source="local",
        )
        .add_models(
            pt_file=r"C:\Users\Gamer\anaconda3\envs\dfdir\yolov5\runs\train\playerbutton6\weights\best.pt",
            repo_or_dir="./yolov5",
            model="custom",
            source="local",
        )
        .get_hwnd_window(window_title_regex=r"[Bb]lue[sS]tacks.*")
        .take_screenshot_and_run_yolov(
            confidence_thresh=0.3,
            show_results=True,
            quit_key="q",
            sleep_time=0.04,
            rununtilstopped=True,
        )
    )

        winca = (
        Yolov5WindowDetect(
            pt_file=r"C:\.......\best.pt",
            repo_or_dir="./yolov5",
            model="custom",
            source="local",
        )
        .get_hwnd_window(window_title_regex=r"[Bb]lue[Ss]tacks.*")
        .take_screenshot_and_run_yolov(
            confidence_thresh=0.3,
            show_results=True,
            quit_key="q",
            sleep_time=0.04,
            rununtilstopped=True,
        )
    )

    # window capture
    winca.get_hwnd_window(
        window_title_regex=r"[Bb]lue[Ss]tacks.*"
    ).take_screenshot_and_run_yolov(
        confidence_thresh=0.3, show_results=False, rununtilstopped=False,
    ).get_results_as_df()


    # adb capture
    winca.get_adb_window(
        adb_path=r"C:\ProgramData\adb\adb.exe", adb_serial="localhost:5555",
    ).take_screenshot_and_run_yolov(
        confidence_thresh=0.3, show_results=False, rununtilstopped=False,
    ).get_results_as_df()
    """

    def __init__(
        self,
        pt_file: str,
        repo_or_dir: str = "./yolov5",
        model: str = "custom",
        source: str = "local",
    ):
        self.model = [
            load_torchmodel(
                pt_file, repo_or_dir=repo_or_dir, model=model, source=source
            )
        ]
        self.sc = None
        self.last_screenshot = None
        self.adb = False
        self.df = pd.DataFrame()
        self.quit_key = "q"
        self.stop = False

    def add_models(
        self,
        pt_file: str,
        repo_or_dir: str = "./yolov5",
        model: str = "custom",
        source: str = "local",
    ):
        self.model.append(
            load_torchmodel(
                pt_file, repo_or_dir=repo_or_dir, model=model, source=source
            )
        )
        return self

    def get_adb_window(
        self,
        adb_path: str = r"C:\ProgramData\adb\adb.exe",
        adb_serial: str = "localhost:5555",
    ):
        self.sc = ScreenShots(hwnd=None, adb_path=adb_path, adb_serial=adb_serial)
        self.adb = True
        return self

    def get_hwnd_window(
        self, hwnd: Union[int, None] = None, window_title_regex: Union[str, None] = None
    ):
        self.sc = ScreenShots(hwnd=hwnd)
        if window_title_regex is not None:
            self.sc.find_window_with_regex(window_title_regex)
        return self

    def get_screenshot(self):
        if not self.adb:
            self.last_screenshot = rgb_bgr(self.sc.imget_hwnd()).copy()
        else:
            self.last_screenshot = rgb_bgr(self.sc.imget_adb()).copy()

        return self

    def activate_stop(self):
        self.stop = True

    def get_results_as_df(self) -> pd.DataFrame:
        return self.df

    def take_screenshot_and_run_yolov(
        self,
        confidence_thresh: Union[float, int] = 0.3,
        show_results: bool = True,
        quit_key: str = "q",
        sleep_time: Union[float, int] = 0.05,
        rununtilstopped: bool = False,
    ):
        if show_results:
            self.sc.imshow_hwnd(sleep_time=sleep_time, quit_key=self.quit_key)
            sleep(1)
            self.sc.enable_show_edited_images()
        if rununtilstopped is False:
            number_of_loops = 1
        else:
            number_of_loops = sys.maxsize

        self.quit_key = quit_key
        keyboard.add_hotkey(self.quit_key, self.activate_stop)

        for _ in range(number_of_loops):
            if self.stop:
                break
            self.get_screenshot()
            self.df = get_results_as_df(
                path_or_np=self.last_screenshot,
                models=self.model,
                confidence_thresh=confidence_thresh,
            )
            if show_results:
                bi = PILasOPENCV.fromarray(self.last_screenshot.copy())
                ba = PILasOPENCV.ImageDraw(bi)

                for key, item in self.df.iterrows():

                    if item.aa_confidence < confidence_thresh:
                        continue
                    r_, g_, b_ = (
                        random.randrange(50, 255),
                        random.randrange(50, 255),
                        random.randrange(50, 255),
                    )
                    self.df.ds_color_print_all()
                    ba.rectangle(
                        xy=(
                            (item.aa_haystack_start_x, item.aa_haystack_start_y),
                            (item.aa_haystack_end_x, item.aa_haystack_end_y),
                        ),
                        outline="black",
                        width=4,
                    )
                    ba.rectangle(
                        xy=(
                            (item.aa_haystack_start_x, item.aa_haystack_start_y),
                            (item.aa_haystack_end_x, item.aa_haystack_end_y),
                        ),
                        outline=(r_, g_, b_),
                        width=2,
                    )
                    ba.text(
                        xy=((item.aa_haystack_start_x, item.aa_haystack_start_y + 10)),
                        text=f"{str(item.aa_confidence)} - {item.aa_name}",
                        fill="black",
                        font=cv2.FONT_HERSHEY_SIMPLEX,
                        scale=0.50,
                        thickness=3,
                    )
                    ba.text(
                        xy=((item.aa_haystack_start_x, item.aa_haystack_start_y + 10)),
                        text=f"{str(item.aa_confidence)} - {item.aa_name}",
                        fill=(r_, g_, b_),
                        font=cv2.FONT_HERSHEY_SIMPLEX,
                        scale=0.50,
                        thickness=1,
                    )
                self.sc.show_edited_image(bi.getim())

        self.stop = False
        keyboard.clear_all_hotkeys()
        return self



