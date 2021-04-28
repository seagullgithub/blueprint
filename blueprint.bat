@echo off
Rem "verbose mode"

Rem get the path from where we are calling
set arg1=%CD%

Rem pass the first argument
set arg2=%1

Rem call python with the script name and one argument
Rem %~dp0 full path to batch file where also our py file is
python %~dp0\blueprint.py %arg1% %arg2%
