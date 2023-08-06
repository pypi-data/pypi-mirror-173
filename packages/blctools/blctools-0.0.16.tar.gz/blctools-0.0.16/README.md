# BLC Data Analytics tools package

Data Analytics helper functions to work with inside BLC's Cloud system.

# Changelog

## Version 0.0.16
* DatosCROM()
    - Added data invalidation when processing 10 second data. Now consecutive values of P, Q, Wind, Wind_dir and PPos != 0 and != max (for Ppos) are replaced with np.nan
    - fixed bug when selecting no .parques ( [] ) and initializing a DatosCROM object.
    - fixed bug when truying to export specific reports through the generating functions (ie elaborar_curvas_de_potencia, interpretar_bajo_iec61400, etc.) and seeting the "exportar" parameter to True.
    - fixed bug. PI wasn't being correctly calculated. (* instead of / was being used).
    - Added "filtro_n" parameter to .elaborar_curvas_de_potencia(), to only show results with an n_count >= n per bin. Default 0 (deactivated)
    - Added feature. Ppos is being calculated if column doesn't exist, based on Curvas_de_potencia.xlsx on BLC's cloud under blc.get_dc_cfg() directory
    - "clientes" initializing parameter was removed (little use for it)
    - "solo_CROM" initializing parameter was removed (little use for it)
* TablasVC()
    - improved the processing of incidents, now "Origin" is "NA" and np.nan resistent. Default = "INT"
    - fixed bug through which a filter for discarded incidents wasn't working. 
    - refactored processing of incidents, it's more readable now.

## Version 0.0.15
* DatosCROM()
    - .exportar() was added. Helper function to export all loaded reports to xlsx format.
    - .explotar_incidencias() now takes in optional export parameters.
    - .incidencias_interpretar_bajo_iec61400() now takes in optional export parameters.
    - .incidencias_identificar_solapamientos() was added.
    - "curvas_de_potencia" parameter added while initializing, to force power curves to be computed automatically
    - .elaborar_curvas_de_potencia() is now more resistent to failures. Powercurves can be elaborated without having to process incidents before, although not recommended if user doesn't know what he is doing.
    - changed how __renombrar_lvl0() works, now it must be feed the equipment names.
* TablasVC()
    - fixed a bug, where .consultar_equipos_parque_no_agrupamientos would return "PLANT" twice for GRIOEO
    - "cargar_incidencias" and "cargar_datos_basicos" parameters added while initializing, with possible values being [Flase, True, 'offline', 'online']
    - now queries per default active incidents from the 1st day of two months prior to today (if True or 'online' values where passed to "cargar_incidencias" parameter). Then concatenates obtained results with offline results (if there are any).

## Version 0.0.14
* SQLConnector() now decrypts login data from BLC's secure fileserver.
* Corrected functions that took equipments from blctools.TablasVC().conjuntogeneradores, now reading from .tipoequipo
* Changed the behaviour of DatosCROM().fecha_i and DatosCROM().fecha_i setters. They now attempt to update "incidencias" and "archivos" depending on the values of fecha_i and fecha_f, but the setters dont try to order the dates automatically, which lead to an unwanted behaviour.
* Corrected bug in TablasVC(). Now Parks without any grouping of it's generators can return the generators without grouping. Special Case: PEGARCIG
* Changed completely how DatosCROM() now proceses raw data (10 seconds and Incidencias). It's more efficient, and the heavy lifting occurs while processing the 10-second data. Now index has 1 column (Time) and columns have a 3 level structure (p,e,v) = Park, Element, Variable
* DatosCROM()
    - .consultar_equipos_parque() now retrieves the right elements if the plant doesn't havy any other grouping stages
    - .consultar_equipos_por_agrupamiento() now returns an empty list if the plant doesn't havy any other grouping stages
    - .rpt_consolidado(granularidad='1D') was added.
    -  "forzar_reprocesamiento" parameter added while initializing, to force re-process 10 second data.
    - .rpt_curvas_de_potencia() was added

## Version 0.0.13
* Created SQLConnector class to migrate to SQLAlchemy
* blctools.TablasVC now inherits from SQLConnector

## Version 0.0.12
* Function blctools.fechas.obtener_periodo() was added (moved from blctools.ReporteBase())
* Added more parameter flexibility within all functions inside blctools.fechas.
* Objects PPO(), DTE() and DatosCROM() now accept the "periodo" initialization parameter (overrides fecha_i and fecha_f).
* bjects blctools.DatosCROM() and blctools.TablasVC() have now the "solo_CROM=False" initialization parameter.
* function blctools.TablasVC.consultar_nemoCammesa() has now the "solo_CROM=False" argument  

## Version 0.0.11
* Corrected blctools.PPO.periodo('mes_anterior')
* Function ReporteBase.a_excel() accepts now the parameter "exportar_consulta=bool"
* Objects PPO() and DTE() now accept the following initialization parameters
    - "filtro"
    - "periodo" (overrides fecha_i and fecha_f)
* No more unnecessary warnings on changing the "filtro" parameter
* Function blctools.fechas.mes_dia_1() and blctools.fechas.mes_ult_dia() now validate dates using blctools.fechas.validar_fechas()
* Functions blctools.fechas.validar_fecha() and .validar_fechas() now have a parameter "prevenir_futuro=True" as default, to prevent future dates or not.
* Fixed a bug, when changing "filtro" on functions of child classes of DTE() or PPO(), download and extraction directories wouldn't update properly.

## Version 0.0.10
* Attribute blctools.DatosCROM.dir_salida sets to which directory the reports go out to (didn't have much impact before)
* Improved automatic Servicios directory search

## Version 0.0.9
* Removed dependencies list
* Ability to download unfiltered PPOs/DTEs without specifying parks/plants list
* Incidents are no longer loaded by default on blctools.DatosCrom() objects

## Version 0.0.8
* Corrected dependencies list

## Version 0.0.6 ~ 0.0.7
* Bug fixes regarding file management
* Ability to customize filters when hitting CAMMESA's API
* PBA calculation according to IEC61400 is still functioning incorrectly

## Version 0.0.5
* Most of the code is Object Oriented now.
* CAMMESA's forecasts have been added.

## Version 0.0.2 ~ 0.0.4
Fixed the install issues

## Version 0.0.1
* Basic functionality is up and running

## TO DOs
* Prevenir que se intenten procesar archivos excel 10 segundales que no tengan datos
* Usar curvas de potencia de los fabricantes para recomponer la variable Ppos de los datos 10 segundales que no tienen dicho dato disponible.
    - Idealmente cargar tablas de potencia en el VisionCROM
* Crear una función de interpolación de eólicas para curva de potencia. Entra con Velocidad de Viento sale con Potencia Activa, interpolada 
* Convertir DatosCROM().parques a "nemos" automáticamente.
* TablasVC.consultar_datos_parque() que devuelva, datos de un parque, en base acualquiera de los parámetros que se usen para encontrarlo.
* Poder tomar mediciones SMEC de la BD del VC