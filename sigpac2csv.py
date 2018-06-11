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

from org.gvsig.fmap.geom import GeometryLocator
from org.gvsig.fmap.geom.primitive import Polygon

from gvsig import createFeatureType

from gvsig.geom import D2
from gvsig.geom import POLYGON

from gvsig import createShape


from org.gvsig.fmap.dal.feature import FeatureStore

def null2empty(n):
  if n==None:
    return ""
  return n

def null2zero(n):
  if n==None:
    return 0
  return n
  
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

def convert2cvs(data, outf):
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

  for linea in data["DECLARACION"]["LINEA_DECLARACION"]:
    outint(out, linea.get("ID_ALE"))
    outint(out, linea.get("ID_EXP"))
    outstr(out, linea.get("EXP_COD"))
    outstr(out, linea.get("TEX_NIF"))
    outint(out, linea.get("ID_CROQUIS"))
    outint(out, linea.get("PROV"))
    outint(out, linea.get("MUN_CAT"))
    outint(out, linea.get("AGREGADO"))
    outint(out, linea.get("ZONA"))
    outint(out, linea.get("POLIGONO"))
    outint(out, linea.get("PARCELA"))
    outint(out, linea.get("RECINTO"))
    outstr(out, linea.get("COD_TIPO_ALE"))
    outstr(out, linea.get("USO"))
    outint(out, linea.get("SUPERFICIE_DECLARADA"))
    outint(out, linea.get("COEF_REG"))
    outint(out, linea.get("SECANO_REGADIO"))
    outint(out, linea.get("ELEGIBILIDAD"))
    outint(out, linea.get("FC_ALMENDROS"))
    outint(out, linea.get("FC_ALGARROBOS"))
    outint(out, linea.get("FC_AVELLANOS"))
    outint(out, linea.get("FC_NOGALES"))
    outint(out, linea.get("FC_PISTACHOS"))
    outint(out, linea.get("FC_TOTAL"))
    outint(out, linea.get("DN_SURFACE"))
    outstr(out, linea.get("WKT"), last=True)
    out.write("\n")
  out.close()

def convert2shp(data, outf):
  featureType = createFeatureType() 

  featureType.append("ID_ALE", "INTEGER")
  featureType.append("ID_EXP", "INTEGER")
  featureType.append("EXP_COD", "STRING", 25)
  featureType.append("TEX_NIF", "STRING", 25)
  featureType.append("ID_CROQUIS", "INTEGER")
  featureType.append("PROV", "INTEGER")
  featureType.append("MUN_CAT", "INTEGER")
  featureType.append("AGREGADO", "INTEGER")
  featureType.append("ZONA", "INTEGER")
  featureType.append("POLIGONO", "INTEGER")
  featureType.append("PARCELA", "INTEGER")
  featureType.append("RECINTO", "INTEGER")
  featureType.append("COD_TIP_AL", "STRING", 25)
  featureType.append("USO", "STRING", 100)
  featureType.append("SUPERF_DEC", "DOUBLE")
  featureType.append("COEF_REG", "DOUBLE")
  featureType.append("SECANO_REG", "DOUBLE")
  featureType.append("ELEGIBILID", "DOUBLE")
  featureType.append("FC_ALMENDR", "DOUBLE")
  featureType.append("FC_ALGARRO", "DOUBLE")
  featureType.append("FC_AVELLAN", "DOUBLE")
  featureType.append("FC_NOGALES", "DOUBLE")
  featureType.append("FC_PISTACH", "DOUBLE")
  featureType.append("DN_SURFACE", "DOUBLE")
  featureType.append("FC_TOTAL", "DOUBLE")
  featureType.append("GEOMETRY", "GEOMETRY").setGeometryType(POLYGON, D2)
  
  shape = createShape(featureType, outf)

  store = shape.getDataStore()
  store.edit() #FeatureStore.MODE_APPEND)
  
  for linea in data["DECLARACION"]["LINEA_DECLARACION"]:
    feature = store.createNewFeature()
    feature.set("ID_ALE", null2zero(linea.get("ID_ALE")))
    feature.set("ID_EXP", null2zero(linea.get("ID_EXP")))
    feature.set("EXP_COD", null2empty(linea.get("EXP_COD")))
    feature.set("TEX_NIF", null2empty(linea.get("TEX_NIF")))
    feature.set("ID_CROQUIS", null2zero(linea.get("ID_CROQUIS")))
    feature.set("PROV", null2zero(linea.get("PROV")))
    feature.set("MUN_CAT", null2zero(linea.get("MUN_CAT")))
    feature.set("AGREGADO", null2zero(linea.get("AGREGADO")))
    feature.set("ZONA", null2zero(linea.get("ZONA")))
    feature.set("POLIGONO", null2zero(linea.get("POLIGONO")))
    feature.set("PARCELA", null2zero(linea.get("PARCELA")))
    feature.set("RECINTO", null2zero(linea.get("RECINTO")))
    feature.set("COD_TIP_AL", null2empty(linea.get("COD_TIPO_ALE")))
    feature.set("USO", null2empty(linea.get("USO")))
    feature.set("SUPERF_DEC", null2zero(linea.get("SUPERFICIE_DECLARADA")))
    feature.set("COEF_REG", null2zero(linea.get("COEF_REG")))
    feature.set("SECANO_REG", null2zero(linea.get("SECANO_REGADIO")))
    feature.set("ELEGIBILID", null2zero(linea.get("ELEGIBILIDAD")))
    feature.set("FC_ALMENDR", null2zero(linea.get("FC_ALMENDROS")))
    feature.set("FC_ALGARRO", null2zero(linea.get("FC_ALGARROBOS")))
    feature.set("FC_AVELLAN", null2zero(linea.get("FC_AVELLANOS")))
    feature.set("FC_NOGALES", null2zero(linea.get("FC_NOGALES")))
    feature.set("FC_PISTACH", null2zero(linea.get("FC_PISTACHOS")))
    feature.set("FC_TOTAL", null2zero(linea.get("FC_TOTAL")))
    feature.set("DN_SURFACE", null2zero(linea.get("DN_SURFACE")))
    feature.set("GEOMETRY", linea.get("WKT"))
    store.insert(feature)
  store.finishEditing()
  

def hasOnlyPoligons(data):
  geometryManager = GeometryLocator.getGeometryManager()
  for linea in data["DECLARACION"]["LINEA_DECLARACION"]:
    geom = geometryManager.createFrom(linea.get("WKT"))
    if not isinstance(geom, Polygon):
      return False
  return True

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
  #layername = os.path.splitext(os.path.basename(xmlf))[0]

  with open(getResource(__file__, xmlf), 'r') as f:
    xml = f.read()
  data = xmltodic.parse(xml)

  if hasOnlyPoligons(data) :
    output = "shp"
  else:
    output = "csv"
    
  outf = os.path.splitext(xmlf)[0]+"." + output
  if os.path.exists(outf):
    if confirmDialog(i18n.getTranslation("_The_file_%s_already_existsXnlXDo_you_want_to_overwrite_itXquestionX") % os.path.basename(outf))==NO:
      return

  if output == "csv":
    convert2cvs(data, outf)
  else:
    convert2shp(data, outf)
  
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
  