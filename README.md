# AoEIIAIAutoDocu

Python3 script for automatically creating simple HTML based Documentation for Age of Empires II AIs.

I purposely chose it to be a "single file" project with just simple functional programming and simple HTML formatting in the output.
Also I only import very basic python modules to keep it simple.

If you have ideas how to improve the script or how to extend the functionality of the script please make a pull request!

## What do you need to use this script?
You need a python3 installation together with an Age of Empires II AI.

## How do I use this?
Copy the python3 script directly into your Folder containing the AI.
Modify your AI.per files by adding identifiers, the script can identify. More details on that later.
Run the script.
In the Main Folder of the AI a Documentation Folder is createt, which contains the created HTML Documentation.

## What does the script actually do?
1. Gather information
   1. Search the Folder for an existing ".ai" file.
   2. Search for the main Ai.per file.
   3. Loop through the main AI.per file to obtain options.
   4. Analyse the file and folder of the AI and gather all existing .per Files.
   5. Create the documentation folder structure.
2. Analyse the AI
   1. Loop through all .per files and analyse the code and comments.
      The Code is split into meaningful chunks (Rules, load, Comment blocks, ...)
   2. Sort the .per files into the order they are used in the AI.
3. Create the HTML output, one file for each .per file
   1. Headder
   2. Navigaion with hyperlinks
   3. Content
   4. Footer

## How to use identifiers in the .per files

Start a Comment line with ";" add "!" and add one of the listed Identifiers e.g. "a"
(to get ";!a" as the first 3 symbols of the line) to define METADATA inside your AI.
The AI Code is automatically recogniced.
Define Options for this script, usind ";!o" directly in the main AI.per File.
Included in the Documentation are the main AI.per FIle as well as all .per
Files inside the AI Mainfolder, even if unused.


### DEFINE AI METADATA INSIDE .PER FILES

!a -> Author        Author of current AI, module, section, ...
!v -> Version       Version number of the current AI, module, section, ...
!d -> Date          Date of the current AI, module, section, ...

!a,!v,!d can be used multiple times

### MODULEDATA

!m -> TITLE           Title of module
!s -> SubTITLE        Subtile inside module
!r -> Rule name       Name of Rule, must be defined inside a Rule
!i -> Ignore          Ignore this entire line comment

### Define Options for the documentation
Define Option in the main AI.per file:
;!o Option = Value  

Currently available options:

Mainfolder: defines Folder with all .per files; default = found Name of AI

Docfolder: defines Name of documentaton folder; default = Documentation

Docpath: defines target path of documentation folder; default = inside main folder


## LIMITATIONS
 
- The closing ")" of Rules should be in a seperate line to be correctly formatted.
- The closing ")" of load-random constructs has to be in a seperate line!
- Only use utf-8 characters for the entire AI
