#### Capture window - run yolov5 - show results

```python
pip install yolov5windowdetect
```

### Update 2022/10/25

#### Run multiple detection models

```python
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
```

```python
from yolov5windowdetect import Yolov5WindowDetect
winca = (
    Yolov5WindowDetect(
        pt_file=r"C:\Users\.....\best.pt",
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

# window capture -> don't show results, only results as df
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
```

#### Example

<div align="left">
      <a href="https://www.youtube.com/watch?v=-jXqL39Tf5w">
         <img src="https://img.youtube.com/vi/-jXqL39Tf5w/0.jpg" style="width:100%;">
      </a>
</div>
