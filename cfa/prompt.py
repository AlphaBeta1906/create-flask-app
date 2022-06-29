from .url import URL as url

PROMPT = [
    {
        "type": "input",
        "message": "What's your project name(empty or '.' means current dir): ",
        "name": "name",
        "default": "."
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
        "type": "list",
        "message": "Select css framework(cdn): ",
        "choices": [
            "none",
            "bootstrap-5",
            "bulma",
            "materialize",
            "water.css",
            "pico.css",
        ],
        "name": "css"
    },
    {
        "type": "checkbox",
        "message": "choose additional file(s): ",
        "choices":[
            "Heroku procfile",
            "Dokcerfile(empty)",
            "Tests"
        ],
        "name": "add"
    },
    {
        "type": "confirm",
        "message": "Are you sure to use these configuration?",
        "default": False,
        "name": "confirmation"
    },        
]
