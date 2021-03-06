import sys
sys.path.append('../helpers')
import fileHelper
import config_classes
import directoryHelper
import gitHelper
from datetime import datetime


configData = fileHelper.load_yaml_config_file()
DEBUG = configData["debug"]

repository = config_classes.Repository(configData)
platform = config_classes.Platform(configData)

gitHelper.checkout(repository.baseBranch, DEBUG)

if not fileHelper.file_exists(repository.mdPagesPath, DEBUG):
    directoryHelper.make_directory(repository.mdPagesPath, DEBUG)

def format_front_matter(layout, title, categories, swagger, ghPagesSiteName):
    return "---\n" \
           "layout: %s\n" \
           "title: %s\n" \
           "categories: %s\n" \
           "swagger: %s\n" \
           "ghPagesSiteName: %s\n" \
           "---" % \
            (layout, title, categories, swagger, ghPagesSiteName)

for api in platform.apiList:
    fileToLoad = repository.outputYamlPath + api + ".yml"

    if (fileHelper.file_exists(fileToLoad, DEBUG)):
        data = fileHelper.load_yaml_file(fileToLoad, DEBUG)

        apiTitle = data["info"]["title"]
        markdownFile = repository.mdPagesPath + api + ".md"
        layout = repository.mdLayout
        title = apiTitle
        categories = "api_docs"
        swagger = fileToLoad
        ghPagesSiteName = repository.ghPagesSiteName
        mdData = format_front_matter(layout, title, categories, swagger, ghPagesSiteName)
        fileHelper.create_file_from_data(mdData, markdownFile, DEBUG)

        gitHelper.add(markdownFile, DEBUG)

    else:
        print "Could not get Swagger specification from " + fileToLoad + " ."

commitMessage = repository.baseDeployCommitMessage + str(datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
gitHelper.commit_all(commitMessage, DEBUG)

gitHelper.push(DEBUG)
