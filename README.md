# Zup3x Sigma (0.3)

Zup3x is meant to replace Hop3x Student. This tool could avoid lot of pain in using Hop3x.
Hop3x is mandatory for L3 SPI students at Le Maine University of Le Mans (FR.). This tool allow you to
use your modern and shiny IDE and keep your project up to date in Hop3x.
This tool is still under testing, use it at your own risk.

Zup3x v0.3 aka. Sigma is the first RC. Multiplatform bot assistant for Hop3x.

**Functions**
  - Create, edit files/projects in Hop3x like a human being.
  - Compiles and tests with Hop3x and send result(s) through email.
  - Get report by email when something is done.
  - Get remote git and update them in Hop3x

**Forbidden**

    To use this tool without proper sources, don't steal sources for your own sake..
    Don't try to fool your teacher with foreign sources, exams will eventually take off your mask!

**Why does Zup3x comes to exist ?**

> Hop3x is a half failure, is was meant to ?improve student
> code learning?, but for now it does improve teacher life. (And it's good for them of course)
> It's not enough stable, it cannot replace modern IDE and it crash too much! (Because of Java.. And code, of course!)
> This is why I intended to create this tool.
> The student/client part of Hop3x is not the answer of how to improve code learning
> My answer is that Hop3x server side must stand as it is, but Hop3x student should be a plugin/deamon process.
> My position can be debated of course.
> Hop3x could have a future, but not like this, for now.

### Version
0.3.0 Codename Sigma

### Changelog
- Get lastest Hop3x version from internet.
- Support for multi-sessions and project session target.
- Huge stability improvement & bunch of fixes.
- GMail notification and remote control.
- Support for AZERTY layout with unofficial pyautogui @Ousret
- Support for file deletion.
- Bot is more human, support for "take a nap/go pee" included.
- Support for import project to avoid writing all project to the ground.
- Modification is much more stealth and quicker.
- Ability to find file much quicker in Hop3x explorer.
- & More..

### Tech

Zup3x uses a number of open source projects to work properly:

* [Python] - Python 3.5 (Windows, Linux and OSX)
* [Hop3x] - Java-based code editor with tracking. (Limited, closed sources)
* [Git] - Git command line support for Windows.
* [Pyautogui] - Multiplatform input controller for GUI manipulation.

### Installation

You need Python 3.5 to make this tool working:

**Mandatory tools**
```sh
$ pip install pyautogui
$ pip install httplib2
```

**If you are on OSX**
- You'll need to have Quartz installed
```sh
$ pip install pyobjc-core
$ pip install pyobjc
```
**Zup3x command line**
```sh
$ python Zup3x.py -u [Hop3x username] -p [Hop3x password]
```

- [-u] Hop3x username
- [-p] Hop3x password
- [-ugit] Bitbucket username
- [-pgit] Bitbucket password
- [-nu] GMail user (without @gmail.com)
- [-np] GMail password

### Q&A

- I'm using AZERTY keyboard and it seems to write like he recognize QWERTY one, why ?
	- pyautogui does not support azerty layout for now, but I have fixed this issue on my own. Check my pyautogui repository. Or change your keyboard layout to QWERTY!
	- Or install my pyautogui patched version.

**Backup solution**
```sh
$ git clone https://github.com/Ousret/pyautogui.git
$ cd pyautogui/
$ python setup.py install
```

- Something wrong!! Help me.. please ?
	- Open issue, I'll do my best when available.

- I can't use my GMail account, I get "You need to activate low security level application on GMail for Zup3x!" all the time.
	- https://support.google.com/accounts/answer/6010255?hl=en

- How do I stop Zup3x when I'm outside ?
	- Send you a email containing the word "STOP", then if you want to re-activate it later, send "OK". Not in the subject message, place it in email body.

- Can I use other provider than Bitbucket and GMail ?
	- Yes! Change the code accordingly to your needs, it’s not that hard. Try it!

- My teacher yelled at me when he found out that I'm using this beautiful tool, what to do now ?
	- apologise.

- Is it truly stealth ?
	- Yes, in a certain measure.

- What the best way to use this tool ?
	- Create VM and let it run all the time.

- How to make sure it will do what ever I ask him ?
	- Try it once to find out.

### Development

Want to contribute? Great!
Open issue(s), spread the word, fork this repository or set us one stars!

### Todos

 - Write Tests
 - Cleanup

License
----

MIT
**Free Software, Hell Yeah!**

![alt text](http://i.imgur.com/OXahO7l.png "Python always better than Java.")

[//]: # 


   [Hop3x]: <http://hop3x.univ-lemans.fr/>
   [Python]: <https://www.python.org/>
   [Git]: <https://git-scm.com/download/win>
   [Pyautogui]: <https://github.com/asweigart/pyautogui>