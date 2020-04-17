# NLP-DATAU #

Data Utilities for PRE/POST-processing NLP-data and analysis of results.

- Prepare datasets for doccano annotation using an xml-file-reader and elasticsearch
- Calculate statistics over results in excel sheets
- Link subject PRE and POST responses [link](notebooks/link_subject_pre_post_responses.ipynb)
- Template parsing [link](notebooks/xlsx_template_parsing.ipynb)


## Dependencies ##

REQUIRED:
- docker [https://hub.docker.com/](https://hub.docker.com/) 

RECOMMENDED:
- git [https://git-scm.com/downloads](https://git-scm.com/downloads) 



## Install ##

1. Clone or download (button) this repository

    git clone https://github.com/putssander/nlp-datau.git

## Run ##
1. Navigate to the cloned or downloaded project using the terminal or cmd
    
2. Start docker-compose

        docker-compose up
    
3. Find the Jupyter link in the log file and copy the link in the browser. 

        jupyter-nlp-datau             | [I 12:06:45.669 NotebookApp]  or http://127.0.0.1:8888/?token=0c01e853a34a4bb0db3a542ca15c3af036cab7a11fd64bb2

6. Navigate to the desired notebook in the browser (directory notebooks)

7. Data can be copied to the resources/data folder (needs to be created)
