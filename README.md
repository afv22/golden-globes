# gg-project-master
Golden Globe Project Master

### Contributors 
Annika Amlie, Rahul Shukla, Andrew Vagliano

For this project, we used natural language processing to gather data from a set of tweets from the Golden Globes. Data included who won each award, who presented each award, etc. We used Python 3 along with certain packages such as nltk.

### To Start
Clone our repository: 
```
git clone https://github.com/afv22/golden-globes.git 
cd golden-globes 
pip install -r requirements.txt
```
Import nltk...
```
 $ python3
 import nltk
 nltk.download('stopwords')
 ```

Get gg2013.json and gg2015.json and put into same directory

Since we worked in Python 3, the proper Python packages must first be installed in order for the code to run properly. These packages can be installed by using $python3 and $pip:
```
$ pip3 install <package-name>
$ pip3 show <package-name>
 ```
Some examples include:
```
pip install gender-guesser
 pip install en_core_web_sm
```
If a package does not appear to be downloaded on the computer,
please use pip

Once it is set up properly, run gg_api:
 $ python3 gg_api.py

Enjoy! :)

