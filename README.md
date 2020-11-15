# AGP Campus Virtal


## TODO LAST SPRINT
### Major
- Finish landing page - Javier
- Fix footer outspill bug - Juan
- Fix navbar merge conflict - Alex
- Add activities to all article pages. One page per person - To assign, ETA 15/11/2020.
- Add information to Diagnostico page - To assign, ETA 15/11/2020
- Remove debug flashes and messages - Pedro

#### Minor
- Set Google Drive account and Tebleau connection - Pedro
- Translate page routes
- Improve usability
- Improve responsiveness
- Fix PDFKit issue: not able to load fonts from the same subset.



## Folder structure
```
.
├── app          : Main application folder
│    ├── auth        : Authenthication blueprint
│    ├── courses     : Course article blueprint
│    ├── main        : Main blueprint
│    ├── static      : Static page files
│    ├── templates   : Jinja templates (ordered by blueprint folders)
│    ├── scheduler   : Schedodule init
│    ├── email.py    : Email service
│    └── models.py   : Database models
├── temp         : Temporary files
├── .gitignore   : Ignored files and extensions
├── .flaskenv    : Flask environment variables
├── .env         : Secret environtment variables
├── Pipfile      : Pipenv dependiencies
├── Pipfile.lock : Pipenv dependencies lock
├── README.md    : This file
└── web_app.py   : Run file


```

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