from click import echo
from jinja2 import Template

from pathlib import Path
from distutils.errors import DistutilsError

import os


class Create_Project:
    path = os.path.join(Path.home(),".create-flask-app/")
    cache_path = os.path.join(Path.home(),".create-flask-app-cache/")
    
    def __init__(self,name: str,plugins: list,database: str,output_dir: str, css: str,additional: list,auth: str):
        self.name = name
        self.plugins = plugins
        self.database = database
        self.output_dir = output_dir
        self.css = css
        self.additional = additional
        self.auth = auth
    
    def error_msg(self):
        """
        display error message when template not found
        """
        echo(f"template with name '{self.template}' not found")
        quit()       
    
    def create_project(self):  
        output = self.output_dir       
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        try:
            self.add_additional_files()
        except DistutilsError:
            echo("flask template not found,clone new one from remote...")            
        else:
            echo("flask template exist,copying...")
            echo(f"successfully cretate project template ")
            echo(f"run 'cd {output}' to change to project directory")
            echo("\n")
            echo("run 'pip install -r requirements.txt' to install dependencies")
            echo("\n")
            echo("run `python app.py` to start the flask development server")
            echo("\n")
            echo("app will start at http://localhost:5000 (or try http://localhost:5000/api/v1/ if the first one is 404 not found)")
            echo("\n")
            echo("make sure to README.md first to know more about the template")
        
    def render_and_copy(self,filename: str,filepath: str):
        """
        `:param:filename` : name of the file that will be copied
        `:param:filepath` : destination of copy
        """
        
        _file = f"cfa/additionalFiles/{filename}"
        content = open(_file,"r").read()
        
        template = Template(content)
        render: Template = template
        content =  render.render(
                    additional_plugin=self.plugins,
                    database=self.database,
                    generate_key=self.generate_random_string,
                    css=self.css,
                    auth=self.auth
                    )
        new_content = open(os.path.join(os.getcwd(),filepath),"w")
        new_content.write(content)
    
    def generate_random_string(self,n: int):
        """
        generate random string that will be used in config.py file
        `:param:n` : length of char
        """
        import random
        import string
        
        letters = string.ascii_letters + string.digits
        _string = "".join(random.choice(letters) for i in range(n))
        
        return _string
        
    
    def add_additional_files(self):
        dir = self.output_dir
        database = self.database
        
        if database == "sqlite3":
            self.render_and_copy(filename="dbase.db", filepath=f"{dir}/dbase.db")
        
        if database != "none":
            destination =f"{dir}/app/model/" 
            os.makedirs(destination,exist_ok=True)
            open(f"{destination}/__init__.py","a").close()
            self.render_and_copy(filename="model.py",filepath=f"{dir}/app/model/model.py")
          
        if "Heroku procfile" in self.additional:
            self.render_and_copy(filename="Procfile",filepath=f"{dir}/Procfile")
            
        if "Dokcerfile(empty)" in self.additional:
            self.render_and_copy(filename="dockerfile",filepath=f"{dir}/dockerfile")
        
        if "Tests" in self.additional:
            os.mkdir(f"{dir}/test")
            test_file = open(f"{dir}/test/__init__.py","w")
            test_file.write("")
                
        for file in os.listdir("cfa/additionalFiles/"):
            _file = f"cfa/additionalFiles/{file}"
            if not os.path.isdir(_file):

                filename = os.path.splitext(file)[0]
                if filename in ("config","__init__"):
                    self.render_and_copy(filename=file,filepath=f"{dir}/app/{file}")
                elif filename == "requirements":
                    self.render_and_copy(filename=file,filepath=f"{dir}/{file}")
                elif filename == "example":
                    destination = f"{dir}/app/controller/"
                    os.makedirs(destination)
                    open(f"{destination}/__init__.py","a").close()
                    self.render_and_copy(filename=file,filepath=f"{destination}{file}")
                elif filename == "wsgi":
                    self.render_and_copy(filename=file,filepath=f"{dir}/{file}")
                elif filename == "index":
                    template_path = f"{dir}/app/templates/"
                    static_path = f"{dir}/app/static/"
                    os.mkdir(template_path)
                    os.makedirs(f"{static_path}css")
                    os.makedirs(f"{static_path}js",exist_ok=True)
                    self.render_and_copy(filename=file,filepath=f"{template_path}/index.html")
                else:
                    pass
        
        