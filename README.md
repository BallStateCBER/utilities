# CBER UTILITIES

A collection of scripts designed to automate and simplify various office operations

(Each script should get its own folder, with an associated readme file)

All of the utilities in this repository are Python (2.7) based.

## Some Basic Setup Troubleshooting
(Generally intended for new users who are unfamiliar with Python)

### Python Installation
If you don't already have a Python installation,
[you'll need one](https://www.python.org/downloads/).

If you're not sure whether your PC has Python installed, two good places to check are:
- `C:\Python*`
- `%userprofile%\Python*`

If either of these locations exists (and has a `python.exe` file inside), you're probably already set.

### PATH Variables (Windows)
This section deals with making Python tools easy to use.
This may have been done automatically on install.

To check whether Python has been added to your PATH:
  - open a command prompt (search 'cmd' in the start menu)
  - type `python -V`
  - if you get a message containing your Python version, you can skip this step
  - if you get a message saying that `python is not recognized as an internal or external command`, keep reading

To add Python to your PATH:
  - open up your environment variables editor for your account (search 'environment' in the start menu).
  - if a `PATH` variable already exists, select 'edit', otherwise create a new variables
  - add the folder where your `python.exe` lives, as well as any Scripts or Libraries folders nearby (separated by a `;`)
  - an example of a proper format: `C:\Python27;C:\Python27\Scripts;C:\Python27\Library\bin`

After making these changes _open a **new** command prompt (!)_, and try `python -V` again.
If this works, you're done!
(If it doesn't work, you'll want to find help.)

(To avoid this headache altogether, consider installing a Python package such as
[Anaconda](https://docs.continuum.io/anaconda/install),
which gives the option of setting up your environments for you.)

### Installing Requirements (Windows)
If you're experiencing problems running a tool, it's possible that your Python installation is missing a needed component.
To make sure you have the necessary requirements, look for a `requirements.txt` file in the tool folder that you're currently using.
If there is a `requirements.txt` folder, you can automatically install required packages like this:
  - open a command prompt, and navigate to the folder containing `requirements.txt`
    - (e.g. `cd C:\some\path\to\utilities\folder`)
  - run `pip install -r requirements.txt` to automatically install needed tools
  - you should be good to go after this (if you get an error message, look for help)

After making sure to install the needed requirements, try running the tool again.
(If it still crashes, you may be out of luck.
  You'll need to find a Python buddy, do some creative Google searching, or give up and go back to doing things by hand.)

## Contributing
### Code
Improvements and/or new tools are welcome.
If you need help figuring out how to add changes, the Web-Dev team can help you out.
Unfortunately, we're mainly a PHP shop, so if you need help learning Python,
[you're on your own](https://docs.python.org/2/tutorial/).
(But don't worry, Python is reasonably easy to get started in compared with most languages!)

### Non-Code
Share your knowledge!
Students are relatively short-lived employees at CBER.
If you're a student and you use these tools, try to teach new students to use these tools as well,
especially if that student is expected to do your job after you're gone!

If you think you've discovered a bug, consider filing a
[bug report](https://github.com/BallStateCBER/utilities/issues/new).
Even if no one is around to fix problems right away, a bug report will help guide future work when someone willing picks up the work.
