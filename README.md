# Zup3x Client (0.2)

Zup3x is meant to replace Hop3x Student. This tool could avoid lot of pain in using Hop3x.
Hop3x is mandatory for L3 SPI students at Le Maine University of Le Mans (FR.). This tool allow you to
use your modern and shiny IDE and keep your project up to date in Hop3x.
This tool is still under testing, use it at your own risk.

**Functions**
  - Create, edit files/projects in Hop3x like a human being.
  - Compiles, tests with Hop3x and send result(s) through email.
  - Get logs from every update made by email.
  - Update Hop3x with remote Gits. (Bitbucket only)

**Forbidden**

    To use this tool without proper sources, don't steal sources for your own sake..
    Don't try to fool your teacher with foreign sources, exams will eventually take off your mask!

**Why does Zup3x comes to exist ?**

> Hop3x is a half failure, is was meant to improve student
> code learning, but for now it does improve teacher life. (And it's good for them of course)
> It's not enough stable, it crash all the time! (Because of Java.. And code, of course!)
> This is why I intended to create this tool.
> The student/client part of Hop3x is not the answer of how to improve code learning
> My answer is that Hop3x server side must stand as it is, but Hop3x student should be a plugin/deamon process.
> My position can be debated of course.
> Hop3x could have a future, but not like this, for now.

### Version
0.2.2

### Changelog
- Darwin OS support
- Sessions parsing improved
- File creation bug now fixed
- Minors fixes

### Tech

Zup3x uses a number of open source projects to work properly:

* [Python] - Python 3.5 (Windows, Linux and OSX)
* [Hop3x] - Java-based code editor with tracking (Not very open, but..)
* [Git] - Git command line support for Windows

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

### Development

Want to contribute? Great!
Open issue(s), spread the word, fork this repository or set us one stars!

### Todos

 - Write Tests
 - Cleanup code
 - Optimize
 - Set it more human, stealth!

License
----

MIT
**Free Software, Hell Yeah!**

[//]: # 


   [Hop3x]: <http://hop3x.univ-lemans.fr/>
   [Python]: <https://www.python.org/>
   [Git]: <https://git-scm.com/download/win>
