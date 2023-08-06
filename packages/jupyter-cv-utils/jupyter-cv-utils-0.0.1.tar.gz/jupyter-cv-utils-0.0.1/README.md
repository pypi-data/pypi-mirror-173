# Jupyter CV Utils

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://img.shields.io/badge/License-MIT-blue.svg)

This package contains utility functions to make life easier when using Jupyter notebooks.

## Installation

* With pip:
[Under construction]

* Editable mode to develop and run tests, run the following in your virtualenv:

    ```
    # Clone the repository.
    git clone https://github.com/saratrajput/jupyter_cv_utils.git

    cd jupyter_cv_utils/
    pip install -e .[dev]
    ```

## Usage

* Import package.

    ```
    import jupyter_cv_utils as jutils
    ```

* Install package.

    ```
    jutils.install("numpy")
    ```

* Show image in matplotlib fashion.

    ```
    jutils.imshow("numpy")
    ```

* Show image in OpenCV window.

    ```
    jutils.imshow_opencv("numpy")
    ```

* Reload a module.

    ```
    jutils.reload(<module_name>)
    ```

* Segment image based on color.

    ```
    lower_hsv = (Hue, Saturation, Value)
    upper_hsv = (Hue, Saturation, Value)
    jutils.segment_color(img, lower_hsv, upper_hsv)
    ```

    Hue is in the range 0 ~ 180.
    Saturation and Value are in the range 0 ~ 255.
