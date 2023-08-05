# Harbour project
---------------
This project aims to make it easier to create images in AWS ECR. There are some implementations already in place like Dump tables from Mysql and Postgres databases.
## Commands to use it
---------------
```
pip install --upgrade harbour
harbour configure
```
After installing the lib, you need to execute an image register, in this case pointing to the container's code and content. 

The harbour start a codepipeline to create and save the history on dynamodb and Register the container image. 
```
harbour register --path $(pwd)/dump/latest/ --name dumper:latest
```
```
ex:
dump/
    └── main.py
    └── Dokerfile
    └── requirements.txt
```

## Upload new versions on https://pypi.org/
---------------
We need to install, packge and send using twine
```
pip install twine
python setup.py sdist
twine upload dist/*
```

***In order to get the configuration for harbour, access it's secret on LastPass***

## Harbour Architecture
---------------
![Image of Yaktocat](harbour_diagram.png)
