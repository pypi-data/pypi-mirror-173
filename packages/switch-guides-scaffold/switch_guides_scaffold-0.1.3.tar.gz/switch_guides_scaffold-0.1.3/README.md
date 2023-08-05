# Switch Automation library for Python
This is a package for helping with the creation of Platform Guides in the Switch Automation software platform. 

You can find out more about the platform on [Switch Automation](https://www.switchautomation.com)

## Getting started

### Prerequisites
* Python 3.8 or later is required to use this package. 
* You must have a [Switch Automation user account](https://www.switchautomation.com/our-solution/) to use this package. 

### Enable Venv
Enabling virtual environment will allow us to isolate libraries per project. 
Allowing us to run multiple projects with different library requirements on the same system.

```bash
python -m venv pyenv
```

Activate the pyenv on your terminal

Windows:
```bash
./pyenv/Scripts/activate
```

Linux/MacOS:
```bash
. pyenv/Scripts/activate
```

### Install the package
Install the Switch Guides library for Python with [pip](https://pypi.org/project/pip/):

```bash
pip install switch-guides-scaffolder
```

### Create a Guide
Follow the prompts after running the following to create a new Switch Guide with a sample step that is ready to use.

```bash
switchguides create
```