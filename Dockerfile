FROM python:3.6-slim-jessie

RUN apt-get update && apt-get install -y curl

RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add -

RUN curl -sL https://deb.nodesource.com/setup_13.x | bash - && apt-get install -y git nodejs cloc

WORKDIR /usr/jquery-data

COPY prep.py .

COPY jquery_releases.csv .

RUN python prep.py

RUN python -m pip install -U --force-reinstall pip
RUN pip install seaborn
RUN pip install matplotlib
RUN pip install pandas

RUN rm -rf jquery_releases.csv

# Docker caches results, so if you want to add custom steps to this dockerfile
# (maybe you want to copy in more files) then consider adding these steps below here.
# Otherwise you will need to download all versions of jQuery everytime you add new 
# steps. 

WORKDIR /usr

COPY jsinspect jsinspect

RUN npm install -g ./jsinspect

# Increase the amount of memory nodejs can allocate, this
# prevents JsInspect from running into the GC issues.
ENV NODE_OPTIONS=--max-old-space-size=4000

WORKDIR /usr/jquery-data

COPY scripts scripts
COPY snippets snippets

# Open a bash prompt, such that you can execute commands
# such as `cloc`. 
ENTRYPOINT ["bash"]