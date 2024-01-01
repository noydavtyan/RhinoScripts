# Creating STL and Videos in Rhino
*Brief description of the project.*

## Prerequisites
Before running this project, you need to install the following software:

1. **Python 3.7**
    - Download and install from [Python's official website](https://www.python.org/downloads/release/python-370/).

2. **PILLOW Library for Python**
    - Install by running `pip install pillow` in your command line.

3. **Git**
    - Download and install from [Git's official website](https://git-scm.com/downloads).

## Configuration
After installing the prerequisites, follow these steps to configure the environment:

1. **Setting up `config.txt`**
    - Modify the `config.txt` file in the project directory and adjust all the variables.
    - Add `BAT_CONFIG_PATH` to your environment variables pointing to the location of `config.txt`.

## Usage Instructions
This project is used for creating 3D model videos and STL files. To use this effectively, follow these guidelines:

1. **Naming Layers**
    - If there are multiple 3D models, create layers with names in the following format:
        - `1_earring_top`, `1_earring_bottom`, `2_ring` for an earring with two parts and a ring.
    - The program will create two videos and three STL files named:
        - `model_name_earring_top.stl`
        - `model_name_earring_bottom.stl`
        - `model_name_ring.stl`

2. **Organizing Models**
    - Place the models close to each other for optimal video presentation.

3. **Folder Organization**
    - (TODO) Implement functionality to create separate folders for separate models.

4. **Scaling Rings**
    - (TODO) Implement functionality to scale rings based on given finger size.