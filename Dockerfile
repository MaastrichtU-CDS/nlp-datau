# docker build --rm -t putssander/datascience-notebook-nlp-datau .

# Start from a core stack version
FROM jupyter/datascience-notebook:latest
# Install from requirements.txt file
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
RUN python -m spacy download nl_core_news_sm
RUN python -m spacy download en_core_web_sm
RUN fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER