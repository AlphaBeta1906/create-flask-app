from InquirerPy.separator import Separator
from InquirerPy.inquirer import select

from .url import URL as url

PROMPT = [
    {
        "type": "input",
        "message": "What's your project name(empty or '.' means current dir)?",
        "name": "name",
        "default": "."
    },
    {
        "type": "list",
        "message": "select template: ",
        "choices": [name.replace("_","-") for name in url.keys()],
        "name": "template"
    },
    {
      "type": "list",
      "message": "choose database: ",
      "choices": [
          "none",
          "sqlite3",
          "mysql",
          "postgresql"
      ],
      "name": "database"
    },
    {
      "type": "list",
      "message": "choose user authentication plugin: ",
      "choices": [
          "none",
          "flask-login",
          "flask-jwt-extended"
      ],
      "name": "auth",
      "when": lambda result: result["database"] != "none"
    },
    {
        "type": "checkbox",
        "message": "Select Additional plugin(use space to select/unselect):",
        "choices": [
            Separator(),
            "flask-sqlalchemy",
            "flask-wtf",
            "flask-marshmallow",
            "flask-debugtoolbar",
            "flask-cors",
            "flask-cache",
            "flask-compress",
            
        ],
        "name": "additional_plugin"
    },
    {
        "type": "confirm",
        "message": "Are you sure to use this configuration?",
        "default": False,
        "name": "confirmation"
    },        
]
