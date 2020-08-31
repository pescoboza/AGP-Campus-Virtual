# AGP Campus Virtal

## Running
Install pipenv:
```
pip install pipenv
```

Install virtual environment packages:
```
pipenv install
```

Enter virtual environment shell:
```
pipenv shell
```

\
Set the Flask application environment variable:
```
set FLASK_APP=run.py
```
Set the Flask evnironment to development:
```
set FLASK_ENV=development
```

\
Run web app (from inside the virtual environment):
```
flask run
```
or
```
python run.py
```
\
Full example:
```
pip install pipenv
pipenv install
pipenv shell
set FLASK_APP=run.py
set FLASK_ENV=development
flask run
```


## Auto formatting
Please disable auto formatting for python files to keep it from messing up imports.

```
mkdir .vscode
touch .vscode/settings.json
```
.vscode/settings.json
```
{
    "[python]": {
        "editor.formatOnsave": false
    }
}
```

## TODO
- Add email integration.
- Add password recovery and change.