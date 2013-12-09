TweetBeat
=========

EECS 338 Practicum in Information Systems Project


To begin installation, first unzip or clone this repository into a clean folder on the command line interface. 

For all of the following instructions, we will be using pip, an easy-to-use Python module installer that makes it easy
to add libraries and tools. You can find the install instructions at the following url, and follow them according to your
system and setup.

pip setup:
http://www.pip-installer.org/en/latest/installing.html

The next important step is to install virtualenv which allows for this folder to install python modules and
libraries independent of the system's Python installation. To install virtualenv, you should use pip to install the 
virtualenv module. This link explains how to install virtualenv easily:

virtualenv setup:
http://www.virtualenv.org/en/latest/virtualenv.html#installation

Once virtualenv is installed on your system, you can initialize a virtualenv environment to the selected folder. To do this, you should run the following command and get an output similar to the following:

  ```
  $ virtualenv venv
  New python executable in venv/bin/python
  Installing distribute............done.
  ```

Now that virtualenv is actually installed to the directory and initialized, to run commands out of that virtual Python environment, you must activate the venv environment from the command line. To do this, you can run one of two commands:

Windows 
```
$ venv\scripts\activate
```
Mac
```
$ . venv/bin/activate
```

If run successfully, you will notice that the shell prompt of your command line has slightly changed from the default. On Mac OsX, the prefix (venv) is added before the normal shell prompt. Once you've done this, congratulations! You're successfully working out of a virtual installation of Python that is independent from your system installation.

Here are the following libraries that TweetBeat uses that you will have to import using the 'pip install' command:
Flask (http://flask.pocoo.org/)
wtforms (http://wtforms.readthedocs.org/en/latest/)
Twitter (https://github.com/sixohsix/twitter)
NLTK (http://nltk.org/)
BeautifulSoup (http://www.crummy.com/software/BeautifulSoup/)

You can use the following 5 commands from the virtualenv to install these libraries:
```
  pip install Flask
  pip install wtforms
  pip install twitter
  pip install nltk
  pip install BeautifulSoup
```

If all installed successfully, the installation of TweetBeat is now complete! All that is needed is for you to start the server (running via Flask). If you notice, there is a file called test.py in the main directory. All that you need to do to start the server is to call the following line from the commmand line.

```
  python test.py
```

The server should begin, and you will have a locally hosted url that you can navigate to! If you have any questions, feel free to contact me via github or email (philiphouse2015 at u.northwestern.edu).


