#!/usr/bin/python3

__author__  = "ulysses0099"
__version__ = "v0c2"
__status__  = "Prototype"

import os, sys, glob, copy, shutil
from sys import platform as _platform



# ==============================================================================
# Functions
# ==============================================================================


# ------------------------------------------------------------------------------
# Print Function
def PrintHead(head):
    """ prints separator and head """
    print('\n\n==============================================================================\n\n\t' + head + '...\n')
    print('==============================================================================')

def PrintSubHead(subhead):
    """ prints separator and subhead """
    print('\n------------------------------------------------------------------------------\n\t' + subhead + '...\n')

def PrintMessage(message):
    """ prints message """
    print('\n\t' + message + '\n')

def PrintSubMessage(submessage):
    """ prints submessage """
    print('\t' + submessage)

def PrintDict(dict):
    """ prints dictionary """
    print('\t----------------')
    for d in dict:
        print('\t' + str(d) + '\t\t' + str(dict[d]))
    print('\t----------------')

def PrintSortedDict(dict):
    """ prints sorted dictionary """
    print('\t----------------')
    list = sorted(dict, key=dict.get)
    for i in range(min(list),max(list)+1):
        if i in list:
            print('\t' + str(i) + '\t\t' + str(dict[i]))
    print('\t----------------')

def PrintErrorAndExit(error):
    """ prints error and exit """
    print ('\t ERROR:' + error)
    exit()


# ------------------------------------------------------------------------------
# Analyse AI Functions

def InitDictionaries():
    """ Initializes Dictionaries """
    # Returns Inital Dictionaries for Counter, Statistics and Options
    Counter = {
        'Load Module':  0,
        'Load Random':  0,
        'Module':       0,
        'Rule':         0,
        'Condition':    0,
        'Constant':     0,
        'Random':       0
    }
    Statistics = {
        'Code':         0,
        'Empty':        0,
        'Ignore':       0,
        'Rule':         0,
        'Condition':    0,
        'Comment':      0,
        'Load Module':  0,
        'Random':       0,
        'Load Random':  0,
        'Constant':     0,
        'Total':        0
    }
    Options = {
        'Mainfolder': '',
        'Docfolder': 'Documentation',
        'Docpath': ''
    }
    return Counter, Statistics, Options



def switch_first3letters(case):
    """ switcher for identifying Comments """
    # returns [Identyfier, add Module]
    switcher = {
        ';!a': ['Author',       1],
        ';!v': ['Version',      1],
        ';!d': ['Date',         1],
        ';!m': ['Module Title', 1],
        ';!s': ['Sub Title',    1],
        ';!r': ['Rule Title',   0],
        ';!o': ['Option',       0],
        ';!i': ['Ignore',       0],

    }
    return switcher.get(case, ['', 0])


def switch_Code(case):
    """ switcher for identifying Code """
    # returns [Identyfier, add Module, add Statistics]
    switcher = {
        '(load':                ['Load Module',    1, 1],
        '(load-random':         ['Random',         1, 1],
        '(defconst':            ['Constant',       0, 1],
        '(defrule':             ['Rule',           1, 1],
        '#load-if-defined':     ['Condition',      1, 1],
        '#load-if-not-defined': ['Condition',      1, 1],
        '#else':                ['Condition',      0, 0],
        '#end-if':              ['Condition',     -1, 0]
    }
    return switcher.get(case, [False, 0, 0])


def AnalyseLine(line, Counter, prevlinetype):
    """ Analyses Line and identifies content """

    # PrintSubMessage('---------------\n\tCurrent Line: ' + line)
    # print(Counter['Module'])
    # print('line: ' + line)
    # Replace / or \ with the separator for the used operating system
    if _platform == "linux":
        line = line.replace('\\', '/')
    if _platform == "win32" or _platform == "win64":
        line = line.replace('/', '\\')

    content = ''
    linetype = ''
    found = False

    # Check if line is end of Rule or end of Load Random
    if(line.strip() == ')'):

        found = True
        if Counter['Rule'] > 0:

            linetype = 'Code'
            Counter['Rule'] -= 1
            Statistics['Code'] += 1
            content = line.strip()

        elif Counter['Random'] > 0:

            linetype = 'Code'
            Counter['Random'] -= 1
            Statistics['Code'] += 1
            content = line.strip()

    # Check if line is start of AutoHTMLDocPython options section
    elif(line[0:20] == ';! AutoHTMLDocPython'):
        
        found = True
        linetype = 'Finished'
        Counter['Module'] += 1
        content = ''

    # Check if line is Empty or only ';'
    elif(len(line) < 2 or not line.strip() or line.strip() == ';'):
        
        found = True
        linetype = 'Empty'
        Statistics['Empty'] += 1
        content = ''





    # Check for Comment Characters
    if(not found):
   
        first3letters = line[0:3]
        # PrintSubMessage('first3letters = ' + first3letters)
        content = line[3:]
        content = ' '.join(content.split())
        content = content.lstrip()
        # PrintSubMessage('content = ' + content)

        # Check AutoHTMLDocPython indicators
        res = switch_first3letters(first3letters)
        linetype = res[0]
        # print(linetype)

        if linetype in ['Author', 'Version', 'Date']:
            content = content.replace('Author:', '')
            content = content.replace('Version:', '')
            content = content.replace('Date:', '')
            content = content.replace('Author', '')
            content = content.replace('Version', '')
            content = content.replace('Date', '')
            content = content.lstrip()
            Counter['Module'] += res[1]
            Statistics['Comment'] += 1

        if linetype == 'Rule Title' and Counter['Rule'] == 0:
            linetype = 'Empty'
            content = ''

        if linetype == 'Module Title':
            found = True
            Counter['Module'] += res[1]
            Statistics['Comment'] += 1
            

        if linetype == 'Sub Title':
            found = True
            Counter['Module'] += res[1]
            Statistics['Comment'] += 1
            

        if not linetype == '':
            found = True
            Statistics['Ignore'] += 1

        if linetype in ['Ignore', 'Option']:
            
            found = True
            linetype = 'Ignore'
            content = ''

        
    # Check for Code
    if not found:

        content = line
        splitline = line.split()
        # PrintSubMessage('splitline[0] = ' + splitline[0])

        # Check for AI Scripting Code
        res = switch_Code(splitline[0])

        # print(res)
        if res[0]:
            found = True
            linetype = res[0].strip()
            if linetype in ['Condition', 'Rule', 'Constant']:
                if linetype == 'Condition' and Counter['Condition'] == 0:
                    Counter['Module'] += 1
                elif linetype == 'Rule' and Counter['Condition'] == 0:
                    Counter['Module'] += 1
                elif linetype == 'Constant' and Counter['Condition'] == 0 and prevlinetype is not linetype:
                    Counter['Module'] += 1
            elif linetype == 'Load Module':
                Counter['Module'] += 1
            elif linetype == 'Random' and Counter['Random'] == 0:
                Counter['Module'] += 1

            
            Counter[linetype] += res[1]
            Statistics[linetype] += res[2]
            content = content.strip()

          
    if Counter['Random'] > 0:
       
        preventry = ''
        for entry in splitline:
            # print(entry)
            if '"' in entry:
                found = True
                linetype = 'Load Random'
                content = ' '.join([preventry, entry])
                Counter['Load Module'] += 1
                Counter['Load Random'] += 1

            preventry = entry
    

    # Check if Line is a Comment
    if not found:

        if (len(line) > 1 and line[0] == ';'):
            found = True
            linetype = 'Comment'
            if prevlinetype != 'Comment' and Counter['Rule'] == 0 and Counter['Condition'] == 0 and Counter['Random'] == 0:
                Counter['Module'] += 1
            Statistics['Comment'] += 1
            content = line[1:].strip()
    
    # Content must be Code
    if not found:

        found = True
        linetype = 'Code'
        Statistics['Code'] += 1
        content = line.strip()
        # if ';' in content:
        #     PrintSubMessage('Inline Code Comment detected')



    # PrintSubMessage(linetype + ' found: ' + content)
    Statistics['Total'] += 1
    return linetype, Counter, content
    


def AddToResources(Resources, linetype, prevlinetype, Counter, content):
    """Add linetype and content to Resources based on Counter and prevlinetype"""

    # Do not add Ignored or Empty lines
    if linetype in ['Empty', 'Ignore']:
        return Resources


    # If module does not exist, create new module
    # else add to current module
    if not Counter['Module'] in Resources:
        Resources[Counter['Module']] = [[linetype], [content]]
    else:
        Resources[Counter['Module']] = [ Resources[Counter['Module']][0] + [linetype], Resources[Counter['Module']][1] + [content]]

    return Resources


def AddLoadModule(Modules, Counter, content, parentmodul):


    splitcontent = content.split()
    content = splitcontent[1]    
    content = content.replace('"', '')
    content = content.replace('(', '')
    content = content.replace(')', '')
    content = content.replace('/', ' ')
    content = content.split()
    content[-1] = content[-1] + '.per'
    Modules[Counter['Load Module']] = [Counter['Module'], content, parentmodul.split(os.sep)]
    # print(Modules[Counter['Load Module']])


    return Modules







# ------------------------------------------------------------------------------
# HTML OUTPUT

def WriteListToFile(file, list_lines):

    for line in list_lines:            
        file.write(line + '\n')


def WriteHeadToFile(file, filename , ai):

    list_header = [
        '<!DOCTYPE html>',
        '<!--' + filename + '-->',
        '<head>',
        '<title>'+ ai + '</title>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<style>',
        '* {',
        '\tbox-sizing: border-box;',
        '}',
        'body {',
        '\tfont-family: Arial, Helvetica, sans-serif;',
        '\tmargin: 0;',
        '}',
        '.header {',
        '\tpadding: 5px;',
        '\ttext-alig       n: left;',
        '\tbackground: #52b338;',
        '\tcolor: black;',
        '\tfont-size: 20px;',
        '\twidth: 100%;',
        '}',
        'nav {',
        '\tfloat: left;',
        '\twidth: 30%;',
        '\tbackground: #98ee80;',
        '\tpadding: 10px;',
        '}',
        'nav ul {',
        '\tlist-style-type: none;',
        '\tmargin : 0'
        '\tpadding: 5px;',
        '\tcolor: black;',
        '}',
        'article {',
        '\tfloat: right;',
        '\tpadding: 20px;',
        '\twidth: 70%;',
        '}',
        'section::after {',
        '\tcontent: "";',
        '\tdisplay: table;',
        '\tclear: both;'
        '}',
        'footer {',
        '\tbackground-color: #52b338;',
        '\tpadding: 10px;',
        '\ttext-align: left;',
        '\tcolor: black;',
        '}',
        '@media (max-width: 600px) {',
        '\tnav, article {',
        '\twidth: 100%;',
        '\theight: auto;',
        '}',
        '.content {padding:20px;}',
        'th {',
        '\ttext-align: center;',
        '}',
        'tr {',
        '\ttext-align: center;',
        '}',
        'ol {',
        '\tlist-style-type: none;',
        '\tcounter-reset: item;',
        '\tmargin: 0;',
        '\tpadding: 0;',
        '}',
        'ol > li {',
        '\tdisplay: table;',
        '\tcounter-increment: item;',
        '\tmargin-bottom: 0.6em;',
        '}',
        'ol > li:before {',
        '\tcontent: counters(item, ".") ". ";',
        '\tdisplay: table-cell;',
        '\tpadding-right: 0.6em;    ',
        '}',
        'li ol > li {',
        '\tmargin: 0;',
        '}',
        'li ol > li:before {',
        '\tcontent: counters(item, ".") " ";',
        '}',
        # 'li {',
        # '\tmargin: 0;',
        # '\tpadding: 2px;',
        # '\tpadding-bottom: 5px;',
        # '}',
        '\t.folder {',
        '\tborder-style:solid;',
        '\tborder-color:#287EC7;',
        '\t}',
        '</style>',
        '</head>'
    ]
    WriteListToFile(file, list_header)

def WriteHeaderToFile(file, ai):

    list_lines = [
        '<div class="header">',
        '<p>"Age of Empires II AI"' + ' Documentation</p>',
        '<h2>' + ai +'.ai</h2>',
        '</div>'
    ]
    WriteListToFile(file, list_lines)

def WriteFooterToFile(file):

    list_footer = [
        '<footer>',
        '<p>Age of Empires II AI Documentation created by "AoE II AI Auto HTML Documentation Creator", programmed by ulysses0099</p>',
        '</footer>'   
    ]
    WriteListToFile(file, list_footer)





def AppendListOfStringsToListOfStrings(list_base, list_add):

    for add in list_add:
        list_base.append(add)

    return list_base


def PrepareLineFromResources(list_Resources):

    # print(list_Resources)
    Restype = list_Resources[0][0]
    res = list(zip(list_Resources[0], list_Resources[1]))
    # PrintMessage(Restype)

    if Restype == 'Module Title':

        newline = '<h2>=====   ' + list_Resources[1][0] +'   =====</h2>'
        # print(newline)

    elif Restype == 'Sub Title':

        newline = '<h1>::::::   ' + list_Resources[1][0] +'   ::::::</h1>'
        # print(newline)

    elif Restype == 'Comment':

        newline = '<p>'
        for comment in list_Resources[1]:
            newline += comment + '\n'
        newline += '</p>'


    elif Restype in ['Author', 'Date', 'Version']:

        newline = '<p>' + Restype +  ':<b> ' + list_Resources[1][0] + '</b></p>'


    elif Restype == 'Load Module':

        newline = '<p>' + list_Resources[1][0] + '</p>'
        newline = newline.replace('(load', '<b>(load</b>')
        newline = newline.replace(')', '<b>)</b>')
        # print(newline)

    elif Restype == 'Random':
        # print(list_Resources)
        

        for entry in list_Resources[1]:
            # print(entry)
            if '(load-random' in entry:
                newline = '\t<dl>\n\t\t<dt><b>' + list_Resources[1][0] + '</b></dt>'
            elif ')' in entry:

                newline = newline + '\n\t\t<dt><b>)</b></dt>'
            else:
                newline = newline + '\n\t\t<dd>' + entry + '</dd>'
            

        newline = newline + '\n\t</dl>' 
        # print(newline)

   
    elif Restype == 'Finished':

        newline = '<hr>'


    elif Restype == 'Rule':

        for restype, resentry in res:
            if restype == 'Rule':
                newline = '\t<dl>\n\t\t<dt><b>' + list_Resources[1][0] + '</b></dt>'
            elif restype == 'Code' and resentry == ')':
                newline = newline + '\n\t\t<dt><b>)</b></dt>'
            elif restype == 'Code' and resentry == '=>':
                newline = newline + '<dt><b>=></b></dt>'
            elif restype == 'Rule Title':
                newline = newline + '<dd><i>' + resentry + '</i></dd>'
            else:
                newline = newline + '\n\t\t<dd>' + resentry + '</dd>'
        
        
    elif Restype == 'Condition':

        newline = '<dl>'
        for res in list_Resources[1]:
            if '#' in res:
                newline = newline + '\n\t\t<dt><b>' + res + '</b></dt>'

            else:
                newline = newline + '\n\t\t<dd>' + res + '</dd>'
        
        newline = newline.replace('<dd>(defrule</dd>', '<dt><b>(defrule</b></dt>')
        newline = newline.replace('<dd>=></dd>', '<dt><b>=></b></dt>')
        newline = newline.replace('<dd>)</dd>', '<dt><b>)</b></dt>')

        newline = newline + '\n\t</dl>'

    elif Restype == 'Load Random':

        newline = '<dl>'
        for res in list_Resources[1]:

            if ')' in res:
                res = res.replace(')', '')

            if 'load-random' in res:
                newline = newline + '<dt><b>(load-random</b></dt>'
                if '"' in res:
                    newline = newline + '\n\t\t<dd>' + res.replace('(load-random', '') + '</dd>'
            else:
                newline = newline + '\n\t\t<dd>' + res + '</dd>'
    
        newline = newline + '\n\t<b>)</b></dl>'


    elif Restype == 'Constant':

        newline = '<ul>' + list_Resources[1][0] + '</ul>'
        newline = newline.replace('(defconst', '<b>(defconst</b>')
        newline = newline.replace(')', '<b>)</b>')


    else:

        newline = '<p>' + Restype + '</p>'

    # PrintSubMessage(newline)
    return '\t' + newline










# ==============================================================================
# Programm
# ==============================================================================



# ==============================================================================
PrintHead('Tutorial AoE II AI Auto Documentation HTML creator')

PrintSubHead('Initialization')
Counter, Statistics, Options = InitDictionaries()
Structure = {}     # Folder and File Structure
Resources = {}     # Contents from reading the Files
Modules = {}       # Module Structure based on (load and (load-random statements




# ==============================================================================
PrintSubHead('Gathering Resources')


# Search for .ai File in current Folder,
PrintMessage('Searching for  AI')
list_ai = glob.glob('./*.ai')
if len(list_ai) == 1:
    ai = list_ai[0]
    ai = ai[2:-3]
    PrintSubMessage('AI: "' + ai + '" found')
    Options['Mainfolder'] = ai
else:
    PrintErrorAndExit('No distinct .ai found or multiple .ai files found ... exit')





# ============================================================================
# Read Main AI.per File
mainfilename = ai + '.per'
PrintMessage('Start Reading Main AI file: ' + mainfilename)
mainfile = open(mainfilename, 'r')
mainlines = mainfile.readlines()









# ==============================================================================
# Search for Options
PrintSubMessage('Searching for Options:')
for line in mainlines:

    # print(line)
    if len(line)>3 and line.strip()[0:3] == ';!o':
            
        splitline = line.strip().split(' ')
        
        if splitline[1] in Options.keys():
            Options[splitline[1]] = splitline[3]

PrintSubMessage('\n\tOptions:')
PrintDict(Options)


mainfile.close()









# ==============================================================================
# Investigate File and Folder Structure of AI
PrintMessage('Investigate File and Folder Structure of AI:')


Options['Docpath'] = Options['Mainfolder'] + os.sep + Options['Docfolder']
PrintDict(Options)
if os.path.isdir(Options['Docpath']):
    PrintSubMessage('Delete Documentation Folder: ' + Options['Docpath'])
    input("\n\tPress Enter to continue...")
    shutil.rmtree(Options['Docpath'], ignore_errors=True)

itx = 0
for x in os.walk(Options['Mainfolder']):
    if not x[0] == Options['Docpath']:
        Structure[itx] = [x[0], x[1], x[2]]
        itx += 1


# PrintSubMessage('\n\tStructure:')
# PrintSortedDict(Structure)

# for root, dirs, files in os.walk(Options['Mainfolder']):

# for root, dirs, files in os.walk(Options['Mainfolder']):
#         path = root.split(os.sep)
#         print((len(path) - 1) * '---', os.path.basename(root))
#         for file in files:
#             print(len(path) * '---', file)









# ==============================================================================
# Create Folder Structure of AI Documentation
PrintMessage('Create Folder Structure of AI Documentation:')

for x in Structure:
    # print(x)
    path = Structure[x][0].replace(Options['Mainfolder'], Options['Docpath'])
    # print(path)
    if not os.path.isdir(path):
        PrintSubMessage('Folder created: ' + path)
        os.mkdir(path)














# ==============================================================================
# Analysing AI Files
PrintSubHead('Analysing AI Files:')

pathtofile = ai + '.per'

Counter['Module'] = 0

Modules[0] = [0, [ai + '.per'], ['']]

with open(pathtofile, 'r') as file:

    prevlinetype = ''
    parentmodule = pathtofile

    for line in file.readlines():

        linetype, Counter, content = AnalyseLine(line, Counter, prevlinetype)

        Resources = AddToResources(Resources, linetype, prevlinetype, Counter, content)

        if linetype in ['Load Module', 'Load Random']:

            Modules = AddLoadModule(Modules, Counter, content, parentmodule)
            # print('Module Added: ' + content)

        if linetype not in ['Ignore', 'Empty']:

            prevlinetype = linetype


    Counter['Module'] += 1
    Resources = AddToResources(Resources, 'Finished', prevlinetype, Counter, '')
    

    file.close()

# PrintSortedDict(Resources)
# PrintDict(Modules)
# PrintDict(Counter)
# PrintDict(Statistics)

imod = 0
StartIndex = {}
skip = False
for iStr in Structure.keys():

    for filename in Structure[iStr][2]:

        if not filename[-4:] == '.per':
            PrintSubMessage('Ignore File: ' + filename)
            skip = True
        # print(filename)
        PrintSubMessage('Analysing File: ' + filename)

        pathtofile = Structure[iStr][0] + os.sep + filename
        # print(pathtofile)

        if not skip:
            with open(pathtofile, 'r') as file:

                # print('file opened')
                # print(len(Resources))
                imod += 1
                prevlinetype = ''
                parentmodule = pathtofile

                StartIndex[imod] = [pathtofile, len(Resources)+1]

                for line in file.readlines():

                    linetype, Counter, content = AnalyseLine(line, Counter, prevlinetype)
                    
                    Resources = AddToResources(Resources, linetype, prevlinetype, Counter, content)

                    if linetype in ['Load Module', 'Load Random']:

                        Modules = AddLoadModule(Modules, Counter, content, parentmodule)

                    if linetype not in ['Ignore', 'Option']:

                        prevlinetype = linetype

                Counter['Module'] += 1
                Resources = AddToResources(Resources, 'Finished', prevlinetype, Counter, '')
    
                file.close()
        skip = False


# PrintDict(StartIndex)
# PrintSortedDict(Resources)
# PrintDict(Modules)
# PrintDict(Counter)
# PrintDict(Structure)
PrintSubMessage('\n\tStatistics:')
PrintDict(Statistics)



# Sort Modules to Resources Start Index
Modules[0].append(0)
for itx in StartIndex:
    # print(StartIndex[itx][0] + '   ' + str(StartIndex[itx][1]))

    for imod in Modules:

        module = os.sep.join(Modules[imod][1])
        # print(os.sep.join(Modules[imod][1]))

        if module == StartIndex[itx][0]:

            Modules[imod].append(StartIndex[itx][1])


# PrintDict(Modules)










# ==============================================================================
PrintSubHead('Sort Modules into loading order:')

# PrintDict(Modules)

SortedModules = {}
cModule = os.sep.join(Modules[0][1])
moduleid = 0
SortedModules[0] = [moduleid, cModule, 0, Modules[0][0], Modules[0][1][-1]]
# print('\tadd: ' + cModule)
cmod = 1
nmod = len(Modules)

imod = 1
while imod < nmod:

    # print('---------------------------')
    cModule = os.sep.join(Modules[imod][1])
    pModule = os.sep.join(Modules[imod][2])
    # print('imod      = ' + str(imod))
    # print('cModule   = ' + cModule)
    # print('pModule   = ' + pModule)

    SortedModules[cmod] = [imod, cModule, 1, Modules[imod][0], Modules[imod][1][-1]]
    cmod += 1

    itx = 1
    while itx < nmod:

        # print(itx)
        sModule = os.sep.join(Modules[itx][1])
        spModule = os.sep.join(Modules[itx][2])
        # print('sModule   = ' + sModule)
        # print('spModule  = ' + spModule)
 
        if spModule == cModule:

            # print('\tadd: ' + sModule)
            SortedModules[cmod] = [itx, sModule, 2, Modules[itx][0], Modules[itx][1][-1]]
            cmod += 1

            iitx = 1
            while iitx < nmod:

                ssModule = os.sep.join(Modules[iitx][1])
                sspModule = os.sep.join(Modules[iitx][2])


                if sspModule == sModule:

                    # print('add: ' + ssModule)
                    SortedModules[cmod] = [ssModule, 3, Modules[iitx][0], Modules[iitx][1][-1]]
                    cmod += 1

                iitx += 1
        itx += 1

        if itx == nmod:  
            imod += 1

    if cmod == nmod:
        break


# PrintDict(Modules)
# PrintDict(SortedModules)
# PrintDict(Resources)










# ==============================================================================
PrintSubHead('Creating HTML Output Files')


htmlfilename = Options['Mainfolder'] + os.sep + Options['Docfolder'] + os.sep + ai + '.html'


with open(htmlfilename, 'w') as htmlfile:

    PrintMessage('HTML File: ' + htmlfilename + ' created')

    PrintSubMessage('Create Head')
    WriteHeadToFile(htmlfile, htmlfilename, ai)

    # Start Body
    htmlfile.write('<body>\n')

    PrintSubMessage('Write Header')
    WriteHeaderToFile(htmlfile, ai)






    PrintSubMessage('Add Navigation')
    list_lines = ['<nav>', '\t<ul>']

    list_lines.append('\t\t<li><b>' + ai + '.per</b></li><hr><hr>')
    list_lines.append('\t\t<br>')
    
    
    list_lines.append('\t\t<li><b>Page Navigation</b></li><hr>')

    link = 'href="#Code"'
    list_lines.append('\t\t<li><a ' + link + '>Code</a></li>')
    link = 'href="#Statistics"'
    list_lines.append('\t\t<li><a ' + link + '>Statistics</a></li>')
    link = 'href="#LoadStructure"'
    list_lines.append('\t\t<li><a ' + link + '>Load Structure</a></li>')
    link = 'href="#FolderStructure"'
    list_lines.append('\t\t<li><a ' + link + '>Folder and File Structure</a></li>')
    list_lines.append('\t\t<br>')
    
    
    list_lines.append('\t\t<li><b>File Navigation</b> (load)</li><hr>')


    # list_lines.append('\t</ul>')
    # list_lines.append('\t<ul>')

    level = SortedModules[0][2]
    # print(SortedModules[0])
    link = 'href="' + ai + '.html"'

    for imod in range(0,len(SortedModules)):

        # print(SortedModules[imod])
        if imod < 1:
            file = SortedModules[imod][1].replace('.per', '.html')
        else:
            path = SortedModules[imod][1].split(os.sep)
            file = os.sep.join(path[1:]).replace('.per', '.html')
        # print(file)
        link = 'href="' + file + '"'
        # print(link)
        prevlevel = level
        level = SortedModules[imod][2]
        name = SortedModules[imod][4]

        tabs = level*'\t'
        if level > prevlevel:
            depth = level - prevlevel
        elif level < prevlevel:
            depth = prevlevel - level
        else:
            depth = 0

        

        if level > prevlevel:
            list_lines.append(depth*'<ul>')

        if level < prevlevel:
            list_lines.append(depth*'</ul>')

        list_lines.append(tabs + '<li><a ' + link + '>' + name + '</a></li>')


    

    list_lines.append('</ul>')
    list_lines.append('\t\t<br>')



    list_lines.append('\t\t<li><b>File Navigation</b> (all)</li><hr>')




    list_lines.append('\t<li>' + ai + '.ai</li>')
    list_lines.append('\t<li>' + ai + '.per</li>')

    for root, dirs, files in os.walk(Options['Mainfolder']):
        path = root.split(os.sep)
        # print(os.path.basename(root))
        if Options['Docfolder'] not in path:
            # print((len(path) - 1) * '---', os.path.basename(root))
            tabs = (len(path) - 1) * '\t'
            list_lines.append(tabs + '<li><b>' + os.path.basename(root) + '</b></li>')
            if len(files) > 0:
                list_lines.append('\t<ul>')
            
                for file in files:
                    # print(len(path) * '---', file)
                    # print(path)
                    # print(file)
                    if len(path) > 1:
                        filelink = os.sep.join(path[1:]) + os.sep + file.replace('.per', '.html')
                    else:
                        filelink = file.replace('.per', '.html')
                    # print(filelink)
                    link = 'href="' + filelink + '"'
                    tabs = len(path) * '\t'
                    list_lines.append(tabs + '<li><a ' + link + '>' + file + '</a></li>')
            
                list_lines.append('\t</ul>')







    list_lines = AppendListOfStringsToListOfStrings(list_lines, ['\t</ul>', '</nav>'])
    WriteListToFile(htmlfile, list_lines)





    htmlfile.write('<section><a id="Code"></a>\n')

    moduleid = 0
    PrintSubMessage('Add Resource Content')
    list_lines = [
        '<article>',
        '\t<h2 id="m' + str(moduleid) + '">' + ai +'</h2>',
        '\t<p>Path:<b> ' + ai + '.per</b></p><hr><hr>'
    ]


    istart = min(Resources.keys())
    for i in range(istart,len(Resources)):
        
        # print(Resources[i])
        newline = PrepareLineFromResources(Resources[i])
        list_lines.append(newline)
        if(Resources[i][0][0] == 'Finished'):
            istart = i
            break


    WriteListToFile(htmlfile, list_lines)






    PrintSubMessage('Add Statistics')
    htmlfile.write('\t<hr><h2 id="Statistics">Statistics</h2><hr>\n')
    
    list_lines = ['\t<table style="width:50%">']
    list_lines.append('\n\t\t<tr>\n\t\t\t<th>Type</th>')
    list_lines.append('\n\t\t\t<th>Number of Lines</th>\n\t\t<tr>')

    for stat in Statistics:

        list_lines.append('\n\t\t<tr align=center>\n\t\t\t<td>' + stat + '</td>')
        list_lines.append('\n\t\t\t<td>' + str(Statistics[stat]) + '</td>\n\t\t<tr>')

    list_lines = AppendListOfStringsToListOfStrings(list_lines, ['\t</table>'])
    WriteListToFile(htmlfile, list_lines)














    PrintSubMessage('Add Load and Module Structure')
    htmlfile.write('\t<hr><h2 id="LoadStructure">Load and Module Structure</h2><hr>\n')


    list_lines = ['<ol>']
    
    level = SortedModules[0][2]

    for imod in range(0,len(SortedModules)):


        prevlevel = level
        level = SortedModules[imod][2]
        name = SortedModules[imod][4]

        tabs = level*'\t'
        # print('-----------')
        # print('name      = ' + name)
        # print('prevlevel = ' + str(prevlevel))
        # print('level     = ' + str(level))
        if level > prevlevel:
            depth = level - prevlevel
            # print('   depth  = ', str(depth))
        elif level < prevlevel:
            depth = prevlevel - level
            # print('   depth  = ', str(depth))
        else:
            depth = 0

        

        if level > prevlevel:
            list_lines.append(depth*'<ol>')

        if level < prevlevel:
            list_lines.append(depth*'</ol>')

        list_lines.append(tabs + '<li>' + '<b>' + name + '</b>' + '</li>')

        

    list_lines.append('</ol>\n</ol>')
    WriteListToFile(htmlfile, list_lines)












    PrintSubMessage('Add Folder and File Structure')
    htmlfile.write('\t<hr><h2 id="FolderStructure">Folder and File Structure</h2><hr>\n')

    htmlfile.write('<p> The Folder and File Structure includes all Files and Folder within the Main Folder even if they are not loaded. </p>')


    # PrintSortedDict(Structure)


    # for root, dirs, files in os.walk(Options['Mainfolder']):
    #     path = root.split(os.sep)
    #     if Options['Docfolder'] not in path:
    #         print((len(path) - 1) * '---', os.path.basename(root))
    #         # print(path)
    #         for file in files:
    #             print(len(path) * '---', file)


    list_lines = ['<ul>']

    list_lines.append('\t<li>' + ai + '.ai</li>')
    list_lines.append('\t<li>' + ai + '.per</li>')

    for root, dirs, files in os.walk(Options['Mainfolder']):
        path = root.split(os.sep)
        # print(os.path.basename(root))
        if Options['Docfolder'] not in path:
            # print((len(path) - 1) * '---', os.path.basename(root))
            tabs = (len(path) - 1) * '\t'
            list_lines.append(tabs + '<li><b>' + os.path.basename(root) + '</b>  |(' + os.sep.join(path) +  ')</li>')
            if len(files) > 0:
                list_lines.append('\t<ul>')
            
                for file in files:
                    # print(len(path) * '---', file)
                    tabs = len(path) * '\t'
                    list_lines.append(tabs + '<li>         ' + tabs + file + '</li>')
            
                list_lines.append('\t</ul>')



    list_lines.append('</ul>')
    WriteListToFile(htmlfile, list_lines)



    



    
    htmlfile.write('</article>\n')
    htmlfile.write('</section>\n')

    PrintSubMessage('Create Footer')
    WriteFooterToFile(htmlfile)


    list_lines = [
        '</body>',
        '</html>'
    ]
    WriteListToFile(htmlfile, list_lines)

    

    PrintSubMessage('HTML File Finished')
    htmlfile.close()











# PrintDict(Structure)
# PrintDict(SortedModules)
PrintDict(Modules)
    

for moduleid in range(1, len(Modules)):

    # print('\n----------------------------')
    # print(moduleid)
    # print(Modules[moduleid])

    modulename = Modules[moduleid][1][-1]
    modulepath = os.sep.join(Modules[moduleid][1])

    folder = Options['Mainfolder'] + os.sep + Options['Docfolder']
    # print('folder = ' + folder)
    filename = os.sep.join(Modules[moduleid][1][1:])
    # print('filename = ' + filename)
    htmlfilename = folder + os.sep + filename
    htmlfilename = htmlfilename.replace('.per', '.html')
    # print('htmlfilename = ' + htmlfilename)
    

    with open(htmlfilename, 'w') as htmlfile:

        PrintMessage('HTML File: ' + htmlfilename + ' created')


        PrintSubMessage('Create Head')
        WriteHeadToFile(htmlfile, htmlfilename, ai)
        # Start Body 
        htmlfile.write('<body>\n')
        PrintSubMessage('Write Header')
        WriteHeaderToFile(htmlfile, ai)
        PrintSubMessage('Add Navigation')
        list_lines = ['<nav>', '\t<ul>']


        list_lines.append('\t\t<li><b>File Navigation</b> (load)</li><hr>')
        level = len(Modules[moduleid][1])-1
        # print('level = ' + str(level))
        folderlevel = len(Modules[moduleid][1])-1
        # print('folderlevel = ' + str(folderlevel))
        for imod in range(0,len(SortedModules)):
            # print('-------------------')
            # print(SortedModules[imod])
            splitpath = SortedModules[imod][1].split(os.sep)
            targetfolderlevel = len(splitpath)-1
            # print('targetfolderlevel = ' + str(targetfolderlevel))
            
        
                
            if imod == 0:
                back = ('..' + os.sep) * (folderlevel -1)
                subpath = splitpath
            else:
                back = ('..' + os.sep) * (folderlevel -1)
                subpath = splitpath[1:]
            
            # print(subpath)
            path = os.sep.join(splitpath[1:-2])
            # print(path)
            targetfilename = back + path + os.sep.join(subpath).replace('.per', '.html')
            
            link = 'href="' + targetfilename + '"'
            # print('link = ' + link)
            prevlevel = level
            level = SortedModules[imod][2]
            name = SortedModules[imod][4]
            tabs = level*'\t'
            if level > prevlevel:
                depth = level - prevlevel
            elif level < prevlevel:
                depth = prevlevel - level
            else:
                depth = 0

        

            if level > prevlevel:
                list_lines.append(depth*'<ul>')

            if level < prevlevel and imod > 0:
                list_lines.append(depth*'</ul>')

            list_lines.append(tabs + '<li><a ' + link + '>' + name + '</a></li>')



        list_lines.append('</ul>')
        list_lines.append('\t\t<br>')




        list_lines = AppendListOfStringsToListOfStrings(list_lines, ['\t</ul>', '</nav>'])
        WriteListToFile(htmlfile, list_lines)










        htmlfile.write('<section><a id="Code"></a>\n')

        PrintSubMessage('Add Resource Content')
        list_lines = [
            '<article><hr><hr>',
            '\t<h2 id="m' + str(moduleid) + '">' + str(modulename) +'</h2><hr>',
            '\t<p>Path:<b> ' + str(modulepath) + '</b></p><hr><hr>'
        ]


        istart = Modules[moduleid][3]
        # print('istart = ' + str(istart))

        for i in range(istart,len(Resources)):

            newline = PrepareLineFromResources(Resources[i])
            list_lines.append(newline)
            if(Resources[i][0][0] == 'Finished'):
                istart = i
                # print('break = ' + str(i))
                break


        WriteListToFile(htmlfile, list_lines)




        htmlfile.write('</article>\n')
        htmlfile.write('</section>\n')

        PrintSubMessage('Create Footer')
        WriteFooterToFile(htmlfile)


        list_lines = [
            '</body>',
            '</html>'
        ]
        WriteListToFile(htmlfile, list_lines)

    

        PrintSubMessage('HTML File Finished')
        htmlfile.close()













# ==============================================================================
PrintHead('Finished')

# ==============================================================================
# End Programm
# ==============================================================================



# PrintSortedDict(Resources)