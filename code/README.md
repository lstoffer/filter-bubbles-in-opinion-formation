# How to reproduce our results

__Windows:__
1. Download our code folder:
> * Download as zip

2. Download Python and follow the instructions in the installation wizzard:\
https://www.python.org/downloads/

    We recommend using version 3.8. During the installation, make sure to check the box "Add Python 3.8 to PATH" (otherwise you won't be    able to use python from the command line).
    
    Alternatively, download Anaconda here: https://www.anaconda.com/ With Anaconda, all necessary libraries are included and you can skip step 3.

3. Install all required libraries:
> * Open the command prompt
> * Check if pip is installed `py -3 -m ensurepip`
>> * if not, follow this [guide](https://www.liquidweb.com/kb/install-pip-windows/) to install it
> * type:\
  `> python -m pip install numpy`\
  `> python -m pip install matplotlib`\
  `> python -m pip install scipy`\
  `> python -m pip install tk`

4. Modify the parameters:
> * Open `model.py` in your favorite IDE or texteditor
> * Modify the parameters (marked by comments) to reproduce our results
   
5. Run our code:
> * type:\
  `> python [Path to model.py (with vertex.py, draw_graph.py in the same folder)]`<br>
  (for example C:\Users\name\Downloads\code\model.py)
  
__Linux:__
1. Download our code folder:
> * Download as zip

2. Install Python:
    ~~~
    $ sudo apt-get update
    $ sudo apt-get install python3.8
    ~~~

3. Install all required libraries:
> * Open the command prompt
> * Install pip for python
   `$ sudo apt-get install python3-pip`
> * type:\
  `$ sudo pip3 install numpy`\
  `$ sudo pip3 install matplotlib`\
  `$ sudo pip3 install scipy`\
  `$ sudo pip3 install tk`

4. Modify the parameters:
> * Open `model.py` in your favorite IDE or texteditor
> * Modify the parameters (marked by comments) to reproduce our results
   
5. Run our code:
> * type:\
  `$ python [Path to model.py (with vertex.py, draw_graph.py in the same folder)]`<br>
  (for example /home/usr/name/Desktop/code/model.py)
  
__Mac:__
1. Download our code folder:
> * Download as zip

2. Install Python:
> * Install Homebrew (package manager)
    `$ ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"`
> * Install pthon itself
    `brew install python`

3. Install all required libraries:
> * Open the command prompt
> * Install pip for python\
`$ curl -O http://python-distribute.org/distribute_setup.py`\
`$ python distribute_setup.py`\
`$ curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py`\
`$ python get-pip.py`

> * type:\
  `$ pip install numpy`\
  `$ pip install matplotlib`\
  `$ pip install scipy`\
  `$ pip install tk`

4. Modify the parameters:
> * Open `model.py` in your favorite IDE or texteditor
> * Modify the parameters (marked by comments) to reproduce our results
   
5. Run our code:
> * type:\
  `$ python [Path to model.py (with vertex.py, draw_graph.py in the same folder)]`<br>
  (for example /Users/username/Desktop/code/model.py)
