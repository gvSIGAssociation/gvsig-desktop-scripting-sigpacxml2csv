# encoding: utf-8

import gvsig

from gvsig import getResource
from gvsig import loadLayer
from gvsig import currentView

import os
import xmltodic

from org.gvsig.tools import ToolsLocator
from org.gvsig.tools.util import ToolsUtilLocator

from gvsig.commonsdialog import confirmDialog
from gvsig.commonsdialog import openFileDialog
from gvsig.commonsdialog import YES
from gvsig.commonsdialog import NO



from java.io import File
from org.gvsig.andami import PluginsLocator

def outint(f,s, last=False):
  if s==None or s.strip()=="":
    f.write("0")
  else:
    f.write(s)
  if not last:
    f.write("; ")

def outstr(f,s, last=False):
  if s==None or s.strip()=="":
    f.write('""')
  else:
    f.write('"')
    f.write(s)
    f.write('"')
  if not last:
    f.write("; ")

def sigpac2csv():
  i18n = ToolsLocator.getI18nManager()
  initPath = ToolsUtilLocator.getFileDialogChooserManager().getLastPath("OPEN_LAYER_FILE_CHOOSER_ID", None)
  f = openFileDialog(
    i18n.getTranslation("_Select_the_SIGPAC_XML_file"), 
    initialPath=initPath.getAbsolutePath()
  )
  if f==None or len(f)==0 or f[0]==None:
    return
  xmlf = f[0]
  layername = os.path.splitext(os.path.basename(xmlf))[0]
  
  outf = os.path.splitext(xmlf)[0]+".csv"
  if os.path.exists(outf):
    if confirmDialog(i18n.getTranslation("_The_CVS_file_%s_already_existsXnlXDo_you_want_to_overwrite_itXquestionX") % os.path.basename(outf))==NO:
      return
      
  with open(getResource(__file__, xmlf), 'r') as f:
    xml = f.read()

  out = open(outf,"w")
  out.write("ID_ALE:Integer; ")
  out.write("ID_EXP:Integer; ")
  out.write("EXP_COD:String; ")
  out.write("TEX_NIF:String; ")
  out.write("ID_CROQUIS:Integer; ")
  out.write("PROV:Integer; ")
  out.write("MUN_CAT:Integer; ")
  out.write("AGREGADO:Integer; ")
  out.write("ZONA:Integer; ")
  out.write("POLIGONO:Integer; ")
  out.write("PARCELA:Integer; ")
  out.write("RECINTO:Integer; ")
  out.write("COD_TIPO_ALE:String; ")
  out.write("USO:String; ")
  out.write("SUPERFICIE_DECLARADA:Double; ")
  out.write("COEF_REG:Double; ")
  out.write("SECANO_REGADIO:Double; ")
  out.write("ELEGIBILIDAD:Double; ")
  out.write("FC_ALMENDROS:Double; ")
  out.write("FC_ALGARROBOS:Double; ")
  out.write("FC_AVELLANOS:Double; ")
  out.write("FC_NOGALES:Double; ")
  out.write("FC_PISTACHOS:Double; ")
  out.write("FC_TOTAL:Double; ")
  out.write("DN_SURFACE:Double; ")
  out.write("WKT:Geometry:polygon\n")

  d = xmltodic.parse(xml)
  for linea in d["DECLARACION"]["LINEA_DECLARACION"]:
    outint(out, linea["ID_ALE"])
    outint(out, linea["ID_EXP"])
    outstr(out, linea["EXP_COD"])
    outstr(out, linea["TEX_NIF"])
    outint(out, linea["ID_CROQUIS"])
    outint(out, linea["ID_ALE"])
    outint(out, linea["MUN_CAT"])
    outint(out, linea["AGREGADO"])
    outint(out, linea["ZONA"])
    outint(out, linea["POLIGONO"])
    outint(out, linea["PARCELA"])
    outint(out, linea["RECINTO"])
    outstr(out, linea["COD_TIPO_ALE"])
    outstr(out, linea["USO"])
    outint(out, linea["SUPERFICIE_DECLARADA"])
    outint(out, linea["COEF_REG"])
    outint(out, linea["SECANO_REGADIO"])
    outint(out, linea["ELEGIBILIDAD"])
    outint(out, linea["FC_ALMENDROS"])
    outint(out, linea["FC_ALGARROBOS"])
    outint(out, linea["FC_AVELLANOS"])
    outint(out, linea["FC_NOGALES"])
    outint(out, linea["FC_PISTACHOS"])
    outint(out, linea["FC_TOTAL"])
    outint(out, linea["DN_SURFACE"])
    outstr(out, linea["WKT"], last=True)
    out.write("\n")
  out.close()

  view = currentView()
  if view == None:
    return
    
  if confirmDialog(i18n.getTranslation("_File_%s_creaded_XnlXDo_you_want_to_load_it_in_the_current_viewXquestionX") % os.path.basename(outf)) == NO:
    return

  listfiles = (File(outf),)
  actions = PluginsLocator.getActionInfoManager()
  addlayer = actions.getAction("view-layer-add")
  addlayer.execute((listfiles,))

def main(*args):
  sigpac2csv()
  