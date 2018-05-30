# encoding: utf-8

import gvsig

from sigpac2csv import sigpac2csv

from gvsig import currentView
from gvsig import getResource

from java.io import File
from org.gvsig.app import ApplicationLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools import ToolsLocator
from org.gvsig.tools.swing.api import ToolsSwingLocator

from org.gvsig.andami import PluginsLocator

class SIGPAC2CSVExtension(ScriptingExtension):
  def __init__(self):
    pass
    
  def canQueryByAction(self):
    return True

  def isEnabled(self,action):
    return True
    
  def isVisible(self,action):
    view = currentView()
    return view != None
    
  def execute(self,actionCommand, *args):
    actionCommand = actionCommand.lower()
    if actionCommand == "tools-sigpac-sigpac2csv":
      sigpac2csv()

def selfRegister():
  i18n = ToolsLocator.getI18nManager()
  moduleId = "sigpac2csv"
  actionName = "tools-sigpac-sigpac2csv"
  tooltip_key =  i18n.getTranslation("_Convert_SIGPAC_XML_to_CSV")
  menu_entry = "tools/SIGPAC/_Convert_XML_to_CSV"
  
  extension = SIGPAC2CSVExtension()

  application = ApplicationLocator.getManager()
  actionManager = PluginsLocator.getActionInfoManager()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()
  #
  # Registramos las traducciones
  i18n = ToolsLocator.getI18nManager()
  i18n.addResourceFamily("text",File(getResource(__file__,"i18n")))

  #
  # Registramos los iconos en el tema de iconos
  icon = File(getResource(__file__,"images",actionName + ".png")).toURI().toURL()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()
  iconTheme.registerDefault("scripting." + moduleId, "action", actionName, None, icon)

  action = actionManager.createAction(
    extension,
    actionName,    # Action name
    tooltip_key,   # Text
    actionName,    # Action command
    actionName,    # Icon name
    None,          # Accelerator
    1009000000,    # Position
    i18n.getTranslation(tooltip_key)    # Tooltip
  )
  action = actionManager.registerAction(action)

  # Añadimos la entrada en el menu herramientas
  application.addMenu(action, menu_entry)
  # Añadimos la accion como un boton en la barra de herramientas.
  #application.addTool(action, "view")

def main(*args):
  selfRegister()