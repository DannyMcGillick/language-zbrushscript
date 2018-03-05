# ZBrush scripting for Atom

This is an atom port of Sublime_ZScript by Siu Yi Liang. It offeres syntax hilighting and API snippets for ZBrush's ZScript language. Recognises .zs extention.

## Install

Copy language-zbrushscript to /User/YourUser/.atom/packages. If you already have a ZScript project open, close and reopen to see the wonder.

## Known Issues
This is super barebones right now, I wanted to iterate right through to publishing to get the ball rolling.  

Functions with no arguments are funky, so for now always pick the args version. 

## Todo
1. Add a thingy to export .txt files.  
1. Add a better thingy to export .txt file to a target Zbrush ZStartup/Macros/Whatever folder if you don't like working from there.
1. The snippets are ripped from 3 year old docs, finish the beautifulSoup document ripper. The selector/find_all only grabs first functions due to a formatting change.