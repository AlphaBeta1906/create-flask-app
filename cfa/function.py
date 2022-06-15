from requests.exceptions import ConnectionError
from click import echo
from jinja2 import Template

import requests

from pathlib import Path
from distutils.errors import DistutilsError
from shutil import copytree,ignore_patterns,unpack_archive,rmtree

import os
import zipfile 

from .url import URL as url

class Create_Project:
    path = os.path.join(Path.home(),".create-flask-app/")
    cache_path = os.path.join(Path.home(),".create-flask-app-cache/")
    
    def __init__(self,name: str,plugins: list,database: str,template: str,output_dir: str):
        self.name = name
        self.plugins = plugins
        self.database = database
        self.template = template
        self.output_dir = output_dir
    
    def error_msg(self):
        """
        display error message when template not found
        """
        echo(f"template with name '{self.template}' not found")
        quit()
        
    
    def download_file(self):
        template = self.template.replace('-','_')
        echo(f"downloading template '{template}' from {url[template][0]} ")
        repo =  requests.get(url[template][0]) 
        with open(f"{self.cache_path}{template}.zip","wb") as file:        
            file.write(repo.content)
            file.close()        
    
    def create_project(self):
        template = self.template.replace("-", "_")    
        output = self.output_dir
        path = self.path
        
        try:
            try:
                url[template]
                copytree(f"{path}/{template}/",output,ignore=ignore_patterns(".git"), dirs_exist_ok=True)
            except KeyError:
                self.error_msg(template)
                quit()
            except FileNotFoundError:
                echo("flask template not found,clone new one from remote...")
            
                # download/clone template
                self.copy_file(copy=True)            
        except DistutilsError:
            echo("flask template not found,clone new one from remote...")
            
            # download/clone template
            self.copy_file(copy=True)
        else:
            echo("flask template exist,copying...")
            echo(f"successfully copying {template} project template ")
            echo(f"run 'cd {output}' to change to project directory")
            echo("\n")
            echo("run 'pip install -r requirements.txt' to install dependencies")
            echo("\n")
            echo("run `python app.py` to start the flask development server")
            echo("\n")
            echo("app will start at http://localhost:5000 (or try http://localhost:5000/api/v1/ if the first one is 404 not found)")
            echo("\n")
            echo("make sure to README.md first to know more about the template")
            self.parse_and_overide()
        
    def copy_file(self,path: str,copy: bool=False,is_update: bool=False):
        cache_path = self.cache_path
        template = self.template 
        output = self.output_dir
        path = self.path
        
        if not os.path.exists(path):
            os.makedirs(path)
        
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        
        try:
            TEMPLATE_ARCHIVE = f"{cache_path}{template}.zip"
            
            if not os.path.exists(TEMPLATE_ARCHIVE):            
                self.download_file(template)
            elif is_update:
                if not os.path.exists(f"{path}/{template}/"):
                    echo("template not found")
                    return 
                rmtree(TEMPLATE_ARCHIVE)
                self.download_file(template)                    
            else:
                echo("copy template from cache")
                
            zipdata = zipfile.ZipFile(TEMPLATE_ARCHIVE)
            folders_in_archive = zipdata.infolist()
            original_name = folders_in_archive[0].filename
            
            if not os.path.exists(f"{path}/{template}/"):
                unpack_archive(TEMPLATE_ARCHIVE,extract_dir=f"{path}")        
                os.rename(f"{path}/{original_name}/",f"{path}/{template}")
            
            echo(f"downloading template success,you can use this template by running `create-flask-app new -t {template} ` ")
            
            if copy:
                copytree(f"{path}/{template}/",output,ignore=ignore_patterns(".git"), dirs_exist_ok=True)            
        except KeyError:
            self.error_msg()
            return    
        except ConnectionError:
            echo("connection error")
            quit()
            return
        except FileExistsError:
            echo(f"template already exist,you can run `create-flask-app new -t {template} -o .` to start using it ")
            return
        except OSError:
            echo(f"template already exist,you can run `create-flask-app new -t {template} -o .` to start using it ")
            return        
        
    def parse_and_overide(self):
        dir = self.output_dir
        plugins = self.plugins
        database = self.database
        
        for file in os.listdir("cfa/additionalFiles/"):
            _file = f"cfa/additionalFiles/{file}"
            print(_file)
            if not os.path.isdir(_file):
                template = open(_file,"r").read()
                #print(text)
                template = Template(template)
                render = template

                rendered = render.render(additional_plugin=plugins,database=database)

                new_requirements = None
            
                if os.path.splitext(file)[0] in ("config","__init__"):
                    new_requirements = open(os.path.join(os.getcwd(),f"{dir}/app/{file}"),"w")
                else:
                    new_requirements = open(os.path.join(os.getcwd(),f"{dir}/{file}"),"w")
                new_requirements.write(rendered)
        
        