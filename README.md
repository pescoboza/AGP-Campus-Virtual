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

Run web app (from inside the virtual environment):
```
python run.py
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