# Amazing Codename Goes Here

Here we are to present our project and code. Make it understandable, give relevant information etc.

## How To Get Started 🙌

![](http://i.imgur.com/ZvnsY1d.gif)


First go ahead and clone the repo with: 
```
git clone git@github.com:jorgenhenrichsen/TDT4290.git
```

Make sure you have Python 3.6.x and pip installed.
Dependencies are managed with a Pipfile so we need Pipenv. It can be grabbed with:
```
pip install --user pipenv
```

Make sure pipenv is runnable in the terminal.

**If it is, you may skip this next part. 

If it is not, you probably need to add it to the path(**if using windows**).
To do this you need to know where it lies, and the easiest way to find it is by running:
```
pip show pipenv
```
You will probably get something that looks like this:
```
...
Location: c:\users\[yourUserName]\appdata\roaming\python\python36\site-packages
...
```
Now go to edit your environmental variables, and edit the PATH in system variables.
Add the location you found in the step above as a new entry, but switch out **site-packages** with **scripts**.
Click **OK** and relaunch your terminal. 

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

## CircleCI

CircleCI will pull, build and test for us whenever a pull request is opened or a commit to an open pull request is pushed.
The project's builds can be seen [here](https://circleci.com/gh/jorgenhenrichsen/TDT4290).

## TODO:
  * Linting?
  * Deploy on version release or tag?
  
