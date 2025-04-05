import arcpy
import os

# Configuración
arcpy.env.overwriteOutput = True
ruta_txt = arcpy.GetParameterAsText(0)
sistema_coordenadas = arcpy.GetParameterAsText(1)
ruta_salida = os.path.dirname(ruta_txt)
nombre_output = str(os.path.basename(ruta_txt).split('.')[0])
nombre_output1 = nombre_output
arcpy.AddMessage("\nby_SAFP\n")

# 1. Verificar/crear carpeta
if not os.path.exists(ruta_salida):
    os.makedirs(ruta_salida)

# 2. Leer archivo .txt con estructura fija
puntos = []
with open(ruta_txt, 'r') as archivo:
    # Saltar encabezados si existen
    primera_linea = archivo.readline().strip().lower()
    if any(palabra in primera_linea for palabra in ["punto", "x", "y", "norte", "este"]):
        arcpy.AddMessage(
            "\nEncabezados detectados: {0}".format(primera_linea))
    else:
        archivo.seek(0)  # Volver al inicio si no hay encabezados

    for linea in archivo:
        linea = linea.strip()
        if not linea:
            continue

        datos = [d.strip() for d in linea.split('\t') if d.strip()]
        if len(datos) >= 3:  # Requiere: Punto\tX\tY
            try:
                punto = datos[0]  # Columna 1: Punto (antes ID)
                x = float(datos[1].replace(',', '.'))  # Columna 2: X/Este
                y = float(datos[2].replace(',', '.'))  # Columna 3: Y/Norte
                puntos.append((punto, x, y))
            except ValueError as e:
                arcpy.AddMessage("Error")

# 3. Crear Shapefile
nombre_output = 'Puntos_{0}'.format(nombre_output)
output_path = os.path.join(ruta_salida, nombre_output + ".shp")

if arcpy.Exists(output_path):
    arcpy.Delete_management(output_path)

arcpy.CreateFeatureclass_management(
    out_path=ruta_salida,
    out_name=nombre_output,
    geometry_type="POINT",
    spatial_reference=sistema_coordenadas
)

# 4. Agregar campos (todos renombrados)
campos = [
    ("Punto", "TEXT", 50),  # Antes "ID"
    ("Este", "DOUBLE"),      # Antes "X"
    ("Norte", "DOUBLE")      # Antes "Y"
]

for campo in campos:
    nombre = campo[0]
    tipo = campo[1]
    try:
        # Si es texto y tiene longitud definida
        if tipo == "TEXT" and len(campo) > 2:
            arcpy.AddField_management(
                output_path, nombre, tipo, field_length=campo[2])
        else:  # Para otros tipos de campo
            arcpy.AddField_management(output_path, nombre, tipo)
    except arcpy.ExecuteError as e:
        arcpy.AddWarning(
            "Error al agregar campo {}: {}".format(nombre, str(e)))

# 5. Insertar datos
if puntos:
    with arcpy.da.InsertCursor(output_path, ["SHAPE@XY", "Punto", "Este", "Norte"]) as cursor:
        for punto, x, y in puntos:
            cursor.insertRow([(x, y), punto, x, y])
    arcpy.AddMessage("\n{0} puntos insertados".format(len(puntos)))
else:
    arcpy.AddMessage("\n! Advertencia: No se encontraron datos válidos")

arcpy.AddMessage("\nResultado final creado en:\n{0} \n\nPuntos_{1} generado!".format(
    ruta_salida, nombre_output))

ruta_line = os.path.join(ruta_salida, 'linea_{0}.shp'.format(nombre_output))

# Paso 6: Crear línea cerrada directamente
arcpy.PointsToLine_management(
    Input_Features=output_path,
    Output_Feature_Class=ruta_line,
    Line_Field=None,
    Sort_Field='id',
    Close_Line="CLOSE"  # Esto asegura que la línea se cierre
)

ruta_polygon = os.path.join(
    ruta_salida, 'Polygon_{0}.shp'.format(nombre_output1))
# Convertir línea cerrada a polígono
arcpy.FeatureToPolygon_management(
    in_features=ruta_line,
    out_feature_class=ruta_polygon,
    cluster_tolerance="",  # Valor predeterminado
    attributes="ATTRIBUTES"  # Mantiene atributos
)

arcpy.management.Delete(ruta_line)

arcpy.AddMessage("\nPolygon_{0} generado!\n".format(nombre_output1))

mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]

# Agregar capas
for capa in [output_path, ruta_line, ruta_polygon]:
    if arcpy.Exists(capa):
        arcpy.mapping.AddLayer(df, arcpy.mapping.Layer(capa), "AUTO_ARRANGE")

# Refrescar sin guardar
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
