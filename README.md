# BootCamp Check-in
> Auto check-in to bootcampspot.com


Do you forget to check-in when you go to your class that uses bootcampspot.com? Use this code to auto check-in to class by running the .bat file with a task scheduler(Windows). Just set the trigger as the time you are supposed to be in class, with a conditional that the school wifi is available.


## Installation

Windows:
- Clone this repository to a local directory
- cd to the directory where requirements.txt is located.
- Activate your virtualenv.
- Run: 
```sh
pip install -r requirements.txt
```
in your shell

- Open user.py in your preferred IDE

- Edit the username and password fields with your login info and save the file
![](images/user.PNG)

- Edit the .bat file with the path to your installation of Python and to checkin.py 

![](images/path.PNG)

- Setup task scheduler to run program at the beginning of class. I had mine run 10 minutes after class starts to account for being late

- First create a new task
![](images/createtask.PNG)

- Give the task a name
![](images/nametask.PNG)

- Under triggers, add a schedule for your task. Multiple triggers can be added.
![](images/scheduletask.PNG)

- Set the action as the path to checkin.bat
![](images/action.PNG)

- Set any conditions. I set mine to check for the school wifi before running
![](images/conditions.PNG)

You're all set!


## Release History

* 0.0.1
    * Work in progress

## Meta

Joseph Villavicencio – [@Hone1er](https://twitter.com/hone1er)

Distributed under the XYZ license. See ``LICENSE`` for more information.


