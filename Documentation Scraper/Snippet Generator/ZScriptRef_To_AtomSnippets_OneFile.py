""" This script will automatically generate Atom completions files from 
the ZBrush HTML documentation. 
"""

from bs4 import BeautifulSoup

import os
import sys

from collections import OrderedDict
import json
import cson
import codecs

#todo: figure out why US-PC python env is failing to build this. 
# Works in isolated venv though, so safe for public.

def outputHighlighting(topLevelName, commandList):
    """
    This method prints the completion keyword data.
    """

    print ('# {0}'.format(topLevelName))
    print ('|'.join(commandList))
    print ('\n')


def prepCompletions(topLevelName, 
    commandList, 
    shortcommandExampleList, 
    fullcommandExampleList, 
    docstringsList,
    finalList,
    commsDict):
    """
    This method writes the data given to completion files.
    """

    #finalList = []

    # format commands to JSON
    for comName, comShort, comLong, doc in zip(commandList, shortcommandExampleList, fullcommandExampleList, docstringsList):

        '''
        comName = comName.encode('utf-8')
        comShort = comShort.encode('utf-8')
        comLong = comLong.encode('utf-8')
        doc = doc.encode('utf-8')
        '''
        # format each dict item and add it
        ''' 
        commandEntryShort = {
            'trigger' : '{0}\t{1}'.format(comName, doc),
            'contents' : '{0}'.format(comShort)
        } 
        commandEntryLong = {
            'trigger' : '{0}\t (args)'.format(comName),
            'contents' : '{0}'.format(comLong)
        }
        '''
        commandEntryShort = {
            '{0}'.format(comName) : {
                'prefix' : '{0}'.format(comName),
                'body': '{0}'.format(comShort),
                'description': '{0}'.format(doc)
            }
        }
        
        commandEntryLong = {
            '{0} (Args)'.format(comName) : {
                'prefix' : '{0}'.format(comName),
                'body': '{0}'.format(comLong),
                'description': '{0}'.format(doc)
            }
        }

        #finalList.append(commandEntryShort)
        #finalList.append(commandEntryLong)
        comKey = '{0}'.format(comName)
        
        commsDict[comKey] = {
            'prefix' : '{0}'.format(comName),
            'body': '{0}'.format(comShort),
            'description': '{0}'.format(doc)
        }
        
        comKeyArgs = '{0} args()'.format(comName)
        commsDict[comKeyArgs] = {
            'prefix' : '{0}'.format(comName),
            'body': '{0}'.format(comLong),
            'description': '{0}'.format(doc)
        }
        
def saveCompletionsFile(finalList, commsDict):
    scopeOfSnippets = ".text.zbrushscript"
    
    finalDict = {
        scopeOfSnippets : commsDict
        #scopeOfSnippets : finalList
    }    
    
    finalData = json.dumps(
        OrderedDict(finalDict), 
        indent=4, 
        separators=(',', ': ')
    )
    
        
    #finalData = cson.dumps(OrderedDict(finalDict), indent=4)
    
    # write output files
    fileOutput = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
        "../snippets/ZBrushAPI_Snippets.json"), 'w')

    fileOutput.write(finalData)

    fileOutput.close()

    print ('Successfully wrote all snippets to ZBrushAPI_Snippets.json')

def start():
    print("Starting")
    finalList = []
    commsDict = {};
    
    html_sourceFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raw_documentation.html')
    with open(html_sourceFile, 'rb') as html:
        soup = BeautifulSoup(html, from_encoding="utf8")

    tables = soup.find_all('table')

    for table in tables:
        # get top level name
        topLevelName = table.find_previous_sibling('h2')

        if topLevelName:
            topLevelName = topLevelName.get_text()

        commandList = []
        shortcommandExampleList = []
        fullcommandExampleList = []
        docstringsList = []

        commands = table.find_all('td', {'bgcolor' : '#f1a851'})
        print("Found " + str(len(commands)) + " commands")
        for c in commands:
            
            com = c.find_all('b')[0].get_text()

            commandList.append(com)

            shortCommand = c.parent.find_next_sibling().find_next_sibling().find_next('dd').get_text()
            
            ##sys.stdout.write(shortCommand)
            
            shortcommandExampleList.append(shortCommand)

            docstring = c.parent.find_next_sibling().find_next('td').get_text()

            docstringsList.append(docstring)
        
            comexample = c.parent()[0].find_next('code').get_text()

            # format full command
            # add newline and tab for each keyword argument
            comexample = comexample.replace(',', ', \n\t')
            # add newline and untab the closing bracket
            comexample = '{0}\n{1}'.format(comexample[:-1], comexample[-1])

            fullcommandExampleList.append(comexample)

        if topLevelName:
            prepCompletions(topLevelName, commandList, shortcommandExampleList, fullcommandExampleList, docstringsList, finalList, commsDict)
            outputHighlighting(topLevelName, commandList)
    saveCompletionsFile(finalList,commsDict)

if __name__ == '__main__':
    start()