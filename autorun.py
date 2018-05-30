# encoding: utf-8

import gvsig
from gvsig.libs.formpanel import getResource

from java.io import File
from org.gvsig.tools import ToolsLocator
from actions import selfRegister

def main(*args):

  i18nManager = ToolsLocator.getI18nManager()
  i18nManager.addResourceFamily("text",File(getResource(__file__,"i18n")))
  
  selfRegister()

