#
# Thanks for visiting this project
#
#   Author:
#       shijian-wow@github, https://github.com/shijian-wow
#
#   Details:
#       This project made with Love by shijian-wow@github, if you want to see more
#       projects which those made by me, check out https://github.com/shijian-wow
#
#   License:
#       This project is licensed under MIT license, and here is the license content:
#   
#           MIT License
#       
#           Copyright (c) 2024 Shijian
#           
#           Permission is hereby granted, free of charge, to any person obtaining a copy
#           of this software and associated documentation files (the "Software"), to deal
#           in the Software without restriction, including without limitation the rights
#           to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#           copies of the Software, and to permit persons to whom the Software is
#           furnished to do so, subject to the following conditions:
#           
#           The above copyright notice and this permission notice shall be included in all
#           copies or substantial portions of the Software.
#           
#           THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#           IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#           FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#           AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#           LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#           OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#           SOFTWARE.
#

#
# This Makefile helps you quickly set up dependencies and run the main program.
# To get started, follow these easy steps:
#
#   1. Open a terminal window on your computer.
#   2. Change the active directory to where this Makefile is located.
#   3. Execute 'make install-deps' to automatically install all required dependencies.
#   4. Once completed, simply execute 'make run' to start the main program.
#
ifeq ($(OS),Windows_NT)
    SYSTEM = WINDOWS
else ifeq ($(shell uname),Linux)
    SYSTEM = LINUX
else
    $(error Unsupported operating system detected)
endif

.install-deps:
    ifeq ($(SYSTEM),WINDOWS)
        pip install -r requirements.txt
    else ifeq ($(SYSTEM),LINUX)
        pip3 install -r requirements.txt

.run:
    ifeq ($(SYSTEM),WINDOWS)
        py chess-gui.py
    else ifeq ($(SYSTEM),LINUX)
        python3 chess-gui.py