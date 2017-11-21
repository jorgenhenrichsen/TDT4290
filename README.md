# NVF Resultregistration System

Result registration for NVF, written in Django.

## How To Get Started 🙌

First go ahead and clone the repo with: 
```
git clone git@github.com:jorgenhenrichsen/TDT4290.git
```

Make sure you have Python 3.6.x and pip installed.
Dependencies are managed with a Pipfile so we need Pipenv. It can be grabbed with:
```
pip install --user pipenv
```
Use pip3 if Python2 is your global python version!

Make sure pipenv is runnable in the terminal.

**If it is, you may skip this next part. 

If it is not, you probably need to add it to the path(**if using windows**).
To do this you need to know where it lies, and the easiest way to find it is by running:
```
pip show pipenv
```
For macOS and Linux:
```
pip --venv
```

You will probably get something that looks like this:
```
...
Location: c:\users\[yourUserName]\appdata\roaming\python\python36\site-packages
...
```
Windows:
Now go to edit your environmental variables, and edit the PATH in system variables.
Add the location you found in the step above as a new entry, but switch out **site-packages** with **scripts**.
Click **OK** and relaunch your terminal. 

macOS and Linux:
Add the python executable to the PATH variable in your shell config file.

## Pipenv should now be runnable. 

If it is, all you need to do is navigate to the project folder and run:
```
pipenv install
``` 
and all neccesary dependencies will be installed to a dedicated virutal environment!

To access the Python executable within the venv run: 
```
pipenv shell
```
Now python commands from the terminal will be run with the venv's Python executable.
Alternatively, if you want to run a single python-file within the venv use: 
```
pipenv run python somefile.py
```

Now the Project interpreter in Pycharm needs to be set to this too.
To do this we need the path of the venv create by pipenv. This can be printed with:
```pipenv --venv```.
Now go into Pycharm's settings and paste in the path as the interpreter-path.

### Installing new dependencies for the project

To install new dependencies, navigate to the project root and run:
```
pipenv install somepackage
```

This will install the package in the virtualenv and add it to the Pipfile and Pipfile.lock.

# PostgreSQL

Here is a tutorial on how to install the database PostgreSQL
https://www.youtube.com/watch?v=e1MwsT5FJRQ

The database should now be connected to Django

# Pull Request

When a pull request is made, use the words close, closes, closed, fix, fixes, fixed, resolve, resolves or resolved
in front of the issue number it fixes, either in the title or the description. Example: Closes #42, description of the pull request. 
The pull request will then be linked with the issue and the task on Waffle.io. Also check that all of your tasks/issues and pull reguest
is closed on waffle.io when the merge is complete.

# Linting
Flake8 is used for linting the project. CircleCI will fail your build if flake8 throws any warnings. This means we cannot merge code that don't follow the code standards defined in Flake8. This can be customized and we can ignore files that are unpractical to lint (some are already ignored, like f.ex django migrations). Rules can be excluded to.
By installing the dependencies for the project with pipenv you should have flake8 installed in your virtual environment.

To run flake8 on your local machine, just navigate to the project root, activate the virtualenv and run:
```
flake8
```
It should the print out any warnings found.

## Integrating with Pycharm
Pycharm has no real plugin support, but flake8 can be added as an external tool.
To do this go to Pycharm preferences and search for "External Tools".

Then add an external tool:
![](https://i.imgur.com/pt7gbpK.png)

And input the fields like this (Values can be found below the image):
![](https://i.imgur.com/pbMjcyp.png)

Program: `$PyInterpreterDirectory$/python`

Parameters: `-m flake8 --max-complexity 10`

Working directory: `$ProjectFileDir$`

Then linting for files should be available like this:
![](https://i.imgur.com/WsDEplj.png)

## Code Style
Not everything will be captured by the linter, so the creator and reviewer of a Pull Reqeust must enforce some rules themselves. Here are some general rules (Some of them is covered by the linter):
### Naming

#### Variables and functions
- Avoid camelcase!
- Make descriptive names.

DO:
```
SOME_CONSTANT = ""
some_property = ""
def some_function_yeah(param_one, param_two)
```

DON'T:
```
SomeConstant = ""
someProperty = ""
def someFunctionYeah(paramOne, paramTwo)
```

#### Classes
- Use capitalized camelcase.
```
class SomeClass(ParentClass):
```

# Testing
Run: python manage.py test. This will execute all the tests!
  
