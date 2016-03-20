'''
Created on Mar 20, 2016

@author: AS017303
'''
from distutils.core import setup
import py2exe

#setup(windows=['BXFReader.py'])
 
setup(windows = [{
          "script":"BXFReader.py",
          "icon_resources": [(1, "machine.ico")],
          "dest_base":"RepoMaster"
          }]
      )
