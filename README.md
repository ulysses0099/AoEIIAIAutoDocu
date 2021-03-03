# AoEIIAutoDocu
Python3 script for automatically creating simple HTML based Documentation for Age of Empires II AIs.

I purposely chose it to be a "single file" project with just simple functional programming and simple HTML formatting in the output.
Also I only import very basic python modules to keep it simple.


If you have ideas how to improve the script or how to extend the functionality of the script please commit!

==============================================================================
## Tutorial AoE II AI Auto HTML Document creator

### HOW TO DEFINE AI METADATA INSIDE .PER FILES

Start a Comment line with ";" add "!" and add one of the listed Identifiers e.g. "a"
(to get ";!a" as the first 3 symbols of the line) to define METADATA inside your AI.
The AI Code is automatically recogniced.
Define Options for this script, usind ";!o" directly in the main AI.per File.
Included in the Documentation are the main AI.per FIle as well as all .per
Files inside the AI Mainfolder, even if unused.
 
------------------------------------------------------------------------------
### VALID IDENTYFIERS

!a -> Author        First encounter triggers Name of Author of AI
!v -> Version       First encounter triggers Version Number of AI
!d -> Date          First encounter triggers Date of AI

!a,!v,!d can be used in every module as well

------------------------------------------------------------------------------
### MODULEDATA

!m -> TITLE           Title of module
!s -> SubTITLE        Subtile inside module
!r -> Name            Name of Rule, must be defined inside Rule
!a -> Author          First encounter triggers Name of Author of module
!v -> Version         First encounter triggers Version Number of module
!d -> Date            First encounter triggers Date Number of module

------------------------------------------------------------------------------
Special IDENTYFIERS

!i -> Ignore          Ignore this entire line comment
!o -> Option = Value  Define Option

------------------------------------------------------------------------------
### LIMITATIONS
 
- The closing ")" of Rules should be in a seperate line to be correctly formatted.
- The closing ")" of load-random constructs has to be in a seperate line!
- Only use utf-8 characters for the entire AI
==============================================================================
