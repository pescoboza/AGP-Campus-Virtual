# AGP Campus Virtal


## TODO LAST SPRINT
### Major
- Finish landing page - Javier
- Fix footer outspill bug - Juan
- Fix navbar merge conflict - Alex
- Add activities to all article pages. One page per person
    - plmn: Alex
    - psta: Cesar
    - crvu: Juan
    - diag: Paulina
    - mama: Javier
    - tstc: Ivan
- Remove debug flashes and messages - Pedro
- Write template for email. - Javier

#### Minor
- Set Google Drive account and Tableau connection - Pedro
- Finish question upload formulary - Pedro
- Translate page routes - Pedro
- Improve usability - PENDING
- Improve responsiveness - PENDING
- Fix PDFKit issue: not able to load fonts from the same subset. - non-critical
- Change recuperation email sender.



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