# AGP Campus Virtual


## TODO
### Major
- Add custom error page handlers
- Add missing institutions
- Add missing activities
- Add terms and conditions
- Proofread all text and information
- Proofread all questions
- Deploy
- Apply domain name

#### Acceptable issues
- Fix PDFKit issue: not able to load fonts from the same subset. - non-mission-critical



## Folder structure
```
.
├── app          : Main application folder
│    ├── auth        : Authenthication blueprint
│    ├── cursos     : Course article blueprint
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
