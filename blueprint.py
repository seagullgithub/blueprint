import sys
import os
from configparser import ConfigParser
from glob import glob
import json
from distutils.dir_util import copy_tree
import re


# todo
# adding script support for the template?
#
# e.g.
# projectName = input('projectname')
# ...
#
#


# set debug to True to print the log() arguments
debug = True

# location of the this script
scriptPath = os.path.abspath(os.path.dirname(__file__))

# location from where the script was called
destination = os.getcwd() + '\\'


# read config.ini file
def getConfig():
    """return configuration from config.ini"""
    config_object = ConfigParser()
    config_object.read(os.path.join(scriptPath, 'config.ini'))

    config = config_object[ "CONFIG"]
    return config


def listTemplates(templates):
    """lists (prints) all available templetes under the path defined
     by config.ini into the console"""
    if len(templates) == 0:
        print('no templates found')
    else:
        print('available templates:\n')
        for template in templates:
            print(f'  * {template} - {templates[template]["description"]}')
            # print(template)


def getTemplates(templatesPath):
    """get all templates under the path defined by config.ini"""
    templates = {}
    templates_paths = glob(templatesPath + '**/')
    for template_path in templates_paths:
        template_name = template_path.split('\\')[-2]

        templateConfig = getTemplateConfig(template_path)

        tmp = {
            'path': template_path,
            'description': templateConfig['description']
        }
        templates[template_name] =  tmp
    return templates


def getTemplateConfig(template_path):
    """return configuration from a template"""
    with open(template_path + 'blueprint.json', "r") as jsonfile:
        data = json.load(jsonfile)
    return data


def copyFiles(useTemplate, templates):
    templatePath = templates[useTemplate]['path']
    data = getTemplateConfig(templatePath)
    print('gonna scaffold:', useTemplate)
    src = os.path.join(templatePath, 'root')

    log('from', src)
    log('to  ', destination)

    # print(os.listdir(src))

    files = glob(src + '/**/*', recursive=True)
    for file in files:
        file_sub_path = file.replace(os.path.join(src,''), '')
        dest = file_sub_path
        log('file_sub_path', file_sub_path)
        # rename files
        if file_sub_path in data['rename']:
            dest = data['rename'][file_sub_path]
        log(file_sub_path, '-', dest)

        with open (file, 'r') as f:
            content = f.read()

        # content = replace(content)

        with open(os.path.join(destination, dest), "w") as f:
            f.write(content)


    # copy_tree(src, destination)
    return True

config = getConfig()

templatesPath = config['templatesPath']

templates = getTemplates(templatesPath)




if len(sys.argv) == 2:
    # only the scriptname is present
    listTemplates(templates)
else:
    # destination = sys.argv[1]
    useTemplate = sys.argv[2]
    copyFiles(useTemplate, templates)



def replace(hay, needle, newString):
    """replaces all occurrences of needle within hay with newString"""
    #read the file contents
    hay = re.sub(needle, newString, hay)
    return hay



def log(*args):
    if debug:
        print(*args)
