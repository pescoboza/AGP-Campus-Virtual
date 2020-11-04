# AGP Campus Virtal


## TODO
- Finish the footer: replace mock content. (Yes, YOU reading this can do this...)
- Fix PDFKit issue: not able to load fonts from the same subset.
- Add data dashboard integration: MongoDB to embedded tableau.
    - Add CSV/Excel report generator.
    - Admin users.
    - Automation: generate CSV report and update tableau public.


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