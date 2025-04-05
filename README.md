# 📍 Script de ArcMap: Generador de Puntos, Líneas y Polígonos desde TXT

**Descripción**:  
Este script de Python para ArcMap automatiza la conversión de archivos `.txt` con coordenadas en **shapefiles** de puntos, líneas cerradas y polígonos. Ideal para procesamiento GIS de datos topográficos, levantamientos de campo o cualquier conjunto de coordenadas estructuradas.

---

## 🛠 Tecnologías utilizadas
- **Lenguaje**: Python 2.7/3.x  
- **Dependencias**:  
  - `arcpy` (ArcMap 10.x o ArcGIS Pro)  
  - `os`, `sys` (módulos estándar de Python)  
- **Entorno**: ArcMap con licencia **Advanced** (para herramientas como `FeatureToPolygon`).

---

## ⚙️ Requisitos previos
1. **Estructura del archivo TXT**:  
   - Formato: `Punto\tX\tY` (columnas separadas por tabulaciones).  
   - Opcional: Encabezados en primera línea (ej: `Punto    X    Y`).  
   - Ejemplo:  
     ```
     P1    500000    8500000  
     P2    500100    8500100  
     ```

2. **Sistema de coordenadas**:  
   - Debe especificarse al ejecutar el script (ej: `WGS 1984 UTM Zone 19S`).

---

## 🚀 Instrucciones de uso
### 1. Ejecución en ArcMap
1. Abre la **Python Window** (`Ctrl + Alt + P`).  
2. Copia y pega el script o ejecútalo como **herramienta de script personalizada**.  
3. Parámetros requeridos:  
   - **Ruta del archivo TXT**: Selecciona tu archivo de entrada.  
   - **Sistema de coordenadas**: Elige el CRS de salida.  

### 2. Resultados generados
El script crea en la misma carpeta del TXT:  
- `Puntos_[nombre].shp`: Shapefile de puntos.  
- `Polygon_[nombre].shp`: Polígono cerrado derivado de los puntos.  
- **Carga automática**: Las capas se añaden al mapa actual.  

---

## 📝 Flujo de trabajo del script
1. **Lectura de TXT**:  
   - Detecta encabezados y normaliza formatos numéricos (ej: `1,000.5` → `1000.5`).  
2. **Creación de puntos**:  
   - Genera un shapefile con campos `Punto`, `Este (X)`, `Norte (Y)`.  
3. **Conversión a polígono**:  
   - Convierte puntos → línea cerrada → polígono.  

---

## ⚠️ Notas importantes
- **Sobrescritura**: El script elimina archivos existentes con los mismos nombres.  
- **Errores comunes**:  
  - Coordenadas mal formateadas (usar punto decimal, no comas).  
  - Permisos de escritura en la carpeta de salida.  
- **Optimización**: Para datasets grandes (>10k puntos), considera usar geodatabases (.gdb).  

---

## 📜 Licencia  
[MIT](https://opensource.org/licenses/MIT) - Libre para uso y modificación.  

---

## ✨ Créditos  
**Autor**: [Sergio andrs fiallo pinto]  
**Versión**: 1.0  
**Última actualización**: `2023-10-25`  

---

> 🔍 ¿Problemas? Verifica que ArcMap tenga acceso a las rutas y que el TXT no tenga filas vacías.  
> 💡 **Tip**: Usa `arcpy.AddMessage()` para depuración personalizada.  
