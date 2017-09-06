# Amazing Codename Goes Here

Here we are to present our project and code. Make it understandable, give relevant information etc.

Let's see if i can make it do as in the tutorial...

Maybe with a different commit name it will be as foretold

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

Now all you need to do is run: 
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
pipenv run somefile.py
```

Now the Project interpreter in Pycharm needs to be set to this too.
To do this we need the path of the venv create by pipenv. This can be printed with:
```pipenv --venv```.
Now go into Pycharm's settings and paste in the path as the interpreter-path.
