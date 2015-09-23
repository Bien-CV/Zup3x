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

    Using this tool without proper sources, you have to use what you made !
    Don't try to fool your teacher with foreign sources, exams will eventually take off your mask!

> Hop3x is a stunning failure, is was meant to improve student
> code learning, but for now it does nothing but improving teacher life.
> It's not enough stable, it crash all the time! (Because of Java..)
> This is why I intended to create this tool.
> When they impose something such as Hop3x, 
> they had to made sure that it is beyond reproach.

### Version
0.2.1

### Changelog
- Darwin OS support
- Sessions parsing improved
- File creation bug now fixed
- Minors fixes

### Tech

Dillinger uses a number of open source projects to work properly:

* [Python] - Python 3.5 (Windows, Linux and OSX)
* [Hop3x] - Java-based code editor with tracking
* [Git] - Git command line support for Windows

### Installation

You need Python 3.5 to make this tool working:

**Mandatory tools**
```sh
$ pip install pyautogui, xerox
```

**If you are on OSX**
- You'll need to have Quartz installed
```sh
$ pip install pyobjc-core
$ pip install pyobjc
```

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


