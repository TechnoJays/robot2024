# Team 94 FIRST Robotics 2024 FRC Robot Code

[FIRST Robotics FRC] is a high school robotics program. This repository contains the code used in the
Southfield High School Team 94 (Retrojays) robot for the year 2024.

## Getting Started

### Development Requirements

* **Python 3.11**: This codebase uses Python 3.11
* [robotpy]: Be sure to follow the [robotpy instructions] for the latest robotPy setup. This is largely handled by
  installing the project as mentioned below.

It is highly recommended that you use a python environment manager with python to help as the version of python required
by pyfrc changes year over year.

* [pyenv] is useful for managing multiple python versions on your computer: **NOTE your python version and pip
  version/dependencies are highly correlated**
    * The most sane method for installing pyenv is using the [pyenv installer]
        * If you are more confident, you can use `brew install pyenv` for macOS and [Homebrew]
        * On windows, you can use`scoop install python` with [Scoop] as the closest thing to Homebrew
          (if you have the misfortune to be using Windows and possibly follow [this page] for more instructions on
          supporting different python versions
* [pipenv] is useful for dependency management for this project as well
    * `pipenv --python 3.11` to create a python 3.11 environment for this project
    * `pipenv install -r requirements.txt` to setup this project in the created virtualenv
    * `pipenv shell` to enter the environment for this project
    * `pip install tox` to install tox in the environment
    * `tox` after that to run the tests

IDEs like [Pycharm also support pipenv].

It is very important that you have updated pip to the latest version. You can do so with the command below:

```bash
# update `pip` and `setuptools` to the latest versions available
pip install -U pip setuptools
```

Note: If you are confident that your system version of python is exactly python 3.8, then you can simply use:

```bash
pip install -r requirements.txt
pip install tox
tox
```

Good luck!

## Deploying to the Robot

### Accessing the Robot

The robot can be reached over ethernet or local usb connection.

With the robot connected to your laptop over USB, your best bet is to attempt to connect with

```bash
# lvuser is the user where robot code is deployed, the `94` here is as programmed when flashing the roborio
ssh lvuser@roborio-94-frc.local
```

If you know the IP of the robot, it can be accessed at:

```bash
# note IP assignment is done dynamically through DHCP, so this IP address may
# not always be true
ssh lvuser@169.254.171.191
```

These steps are useful for confirming connectivity to the robot before attempting to deploy.

### Running robotPy Deployment commands

Robotpy provides useful commands to copy/install all .py files in the `src/` folder to the robot.

RobotPy has some great [robot code deployment instructions and automation].

To deploy code after being connected 
```bash
python src/robot.py deploy --netconsole
```

## Running Tests

1. Make sure, you have `tox` installed:

    ```bash
    pipenv install -r requirements.txt
    pipenv shell
    ```

2. Run the projects tests:

   ```bash
   tox
   ```

`tox` is running `python src/robot.py coverage test` from [RobotPy Unit Testing]

If you would like to run the tests without coverage, you can execute

```bash
python src/robot.py test
```

And individual tests can be run by passing pytest arguments to the `test` option of the [pyfrc] test command

```bash
python src/robot.py test -- ./tests/test_oi.py
```

## Running the Camera Server (CSCore)

It is often useful to test the vision processing code independently of the robot code. Especially since the
[robotpy cscore] **SPECIFICALLY STATES THAT YOU MUST NOT IMPORT `wpilib` IN VISION CODE OR VICE VERSA**

Use the handy commands below to run vision code locally on your laptop

```bash
python -m cscore src/vision/vision.py:start_camera
```

TODO setup GitHub actions for the robot code. Examples are provided directly from the wpilib docs,
[setting up CI for robot code]

### Project Formatting

To be soothing to your mind, the project attempts to make python/PEP formatting not an issue. Given you
think you are ready to commit your code changes. Just run:

```bash
black --check .
```

To show which files **[black]** will reformat.

```bash
black --diff .
```

Shows the changes black will make, and then:

```bash
black .
```

will let the reformatting goodness happen. Black comes with the `pipenv install -e .` of the project.


[black]: https://github.com/ambv/black

[FIRST Robotics FRC]: http://www.usfirst.org/

[Homebrew]: https://brew.sh/

[pipenv]: https://github.com/pypa/pipenv

[pyenv]: https://github.com/pyenv/pyenv

[pyenv installer]: https://github.com/pyenv/pyenv-installer

[Pycharm also support pipenv]: https://www.jetbrains.com/help/pycharm/pipenv.html

[pyfrc]: https://github.com/robotpy/pyfrc

[pyfrc instructions]: http://pyfrc.readthedocs.org/en/latest/

[robot code deployment instructions and automation]: https://robotpy.readthedocs.io/en/stable/guide/deploy.html

[robotpy]: https://robotpy.readthedocs.io/en/stable/index.html

[robotpy cscore]: https://robotpy.readthedocs.io/en/stable/vision/roborio.html#image-processing

[robotpy instructions]: https://robotpy.readthedocs.io/en/stable/getting_started.html

[RobotPy Unit Testing]: https://robotpy.readthedocs.io/en/stable/guide/testing.html

[Scoop]: https://scoop.sh/

[setting up CI for robot code]: https://docs.wpilib.org/en/stable/docs/software/advanced-gradlerio/robot-code-ci.html

[this page]: https://github.com/lukesampson/scoop/wiki/Switching-Ruby-and-Python-Versions









