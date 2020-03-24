# NLP-DATAU #

Data Utilities for PRE/POST-processing NLP-data and analysis of results.

- Prepare datasets for doccano annotation using an xml-file-reader and elasticsearch
- Calculate statistics over results in excel sheets


## Calculate statistics over results in excel sheets ##

requirements:
- docker
- git

install

Clone the repository

    git clone https://github.com/putssander/nlp-datau.git
    
Navigate to the project

    cd nlp-datau
    
Start docker-compose

    docker-compose up
    
Find the Jupyter token in the log and navigate to

[http://127.0.0.1:10000/notebooks/work/notebooks/result-analysis.ipynb](http://127.0.0.1:10000/notebooks/work/notebooks/result-analysis.ipynb)