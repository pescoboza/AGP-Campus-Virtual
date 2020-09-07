# AGP Campus Virtal

## Running for the first time
Install pipenv:
```
pip install pipenv
```

Install virtual environment packages:
```
pipenv install --dev
```

## Regular run
Enter virtual environment shell:
```
pipenv shell
```

\
Call the flask command to run the app (from inside the virtual environment):
```
flask run
```

\
Full example:
```
pip install pipenv
pipenv install --dev
pipenv shell
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
- Create teplates and macros to represent widgets and forms from database objects.
- Fix templates.
- Add exam verification and user grades-
- Improve database query efficiency.
- Explore chaching options.