USE Portafolio_BI;
GO

/* ============================================================
   Proyecto: Sistema BI Tráfico Aéreo Chile
   Archivo: analisis_granularidad_trafico_aereo.sql
   Objetivo:
   Documentar las validaciones realizadas sobre la tabla staging
   para entender granularidad, duplicidad y calidad de datos.
   ============================================================ */


-- 1. Conteo general de registros cargados
SELECT COUNT(*) AS Total_Registros
FROM stg.Trafico_Aereo;


-- 2. Rango temporal y cantidad de períodos
SELECT
    MIN(Fecha) AS Fecha_Minima,
    MAX(Fecha) AS Fecha_Maxima,
    COUNT(DISTINCT Fecha) AS Periodos
FROM stg.Trafico_Aereo;


-- 3. Validación inicial de posible granularidad
-- Fecha + Operador + Ruta + Tipo de tráfico + Sentido operacional
SELECT
    Fecha,
    Cod_Operador,
    ORIG_1,
    DEST_1,
    NAC,
    OPER_2,
    COUNT(*) AS Repeticiones
FROM stg.Trafico_Aereo
GROUP BY
    Fecha,
    Cod_Operador,
    ORIG_1,
    DEST_1,
    NAC,
    OPER_2
HAVING COUNT(*) > 1
ORDER BY Repeticiones DESC;


-- 4. Validación ampliada considerando par de ciudades
SELECT
    Fecha,
    Cod_Operador,
    ORIG_1,
    DEST_1,
    ORIG_2,
    DEST_2,
    NAC,
    OPER_2,
    COUNT(*) AS Repeticiones
FROM stg.Trafico_Aereo
GROUP BY
    Fecha,
    Cod_Operador,
    ORIG_1,
    DEST_1,
    ORIG_2,
    DEST_2,
    NAC,
    OPER_2
HAVING COUNT(*) > 1
ORDER BY Repeticiones DESC;


-- 5. Duplicados exactos considerando atributos y métricas
SELECT
    Fecha,
    Cod_Operador,
    Operador,
    Grupo,
    ORIG_1,
    DEST_1,
    ORIG_1_N,
    DEST_1_N,
    ORIG_1_PAIS,
    DEST_1_PAIS,
    ORIG_2,
    DEST_2,
    ORIG_2_N,
    DEST_2_N,
    ORIG_2_PAIS,
    DEST_2_PAIS,
    OPER_2,
    NAC,
    PAX_LIB,
    PASAJEROS,
    CAR_LIB,
    CARGA_Ton,
    CORREO,
    Distancia,
    COUNT(*) AS Repeticiones
FROM stg.Trafico_Aereo
GROUP BY
    Fecha,
    Cod_Operador,
    Operador,
    Grupo,
    ORIG_1,
    DEST_1,
    ORIG_1_N,
    DEST_1_N,
    ORIG_1_PAIS,
    DEST_1_PAIS,
    ORIG_2,
    DEST_2,
    ORIG_2_N,
    DEST_2_N,
    ORIG_2_PAIS,
    DEST_2_PAIS,
    OPER_2,
    NAC,
    PAX_LIB,
    PASAJEROS,
    CAR_LIB,
    CARGA_Ton,
    CORREO,
    Distancia
HAVING COUNT(*) > 1
ORDER BY Repeticiones DESC;


-- 6. Distribución de métricas presentes por fila
SELECT
    SUM(CASE WHEN PASAJEROS > 0 THEN 1 ELSE 0 END) AS Filas_Con_Pasajeros,
    SUM(CASE WHEN CARGA_Ton > 0 THEN 1 ELSE 0 END) AS Filas_Con_Carga,
    SUM(CASE WHEN CORREO > 0 THEN 1 ELSE 0 END) AS Filas_Con_Correo
FROM stg.Trafico_Aereo;


-- 7. Filas con más de una métrica informada
SELECT
    COUNT(*) AS Filas_Multiples_Metricas
FROM stg.Trafico_Aereo
WHERE
    (CASE WHEN PASAJEROS > 0 THEN 1 ELSE 0 END)
  + (CASE WHEN CARGA_Ton > 0 THEN 1 ELSE 0 END)
  + (CASE WHEN CORREO > 0 THEN 1 ELSE 0 END) >= 2;


-- 8. Comparación entre total de filas y claves distintas
SELECT
    COUNT(*) AS Total_Filas,
    COUNT(DISTINCT
        CONCAT(
            Fecha, '|',
            Cod_Operador, '|',
            ORIG_1, '|',
            DEST_1, '|',
            NAC, '|',
            OPER_2
        )
    ) AS Claves_Distintas_Sin_Metricas
FROM stg.Trafico_Aereo;


-- 9. Comparación agregando métricas
SELECT
    COUNT(*) AS Total_Filas,
    COUNT(DISTINCT
        CONCAT(
            Fecha, '|',
            Cod_Operador, '|',
            ORIG_1, '|',
            DEST_1, '|',
            NAC, '|',
            OPER_2, '|',
            PASAJEROS, '|',
            CARGA_Ton, '|',
            CORREO
        )
    ) AS Claves_Distintas_Con_Metricas
FROM stg.Trafico_Aereo;


/* ============================================================
   Conclusión:
   La fuente no presenta una clave natural única simple basada
   únicamente en fecha, operador, ruta, tipo de tráfico y sentido
   operacional.

   La granularidad se interpreta como:
   "Registro estadístico mensual publicado para una combinación
   de operador, ruta, sentido operacional, tipo de tráfico y
   métricas reportadas."

   Se conserva la información al nivel publicado por la fuente
   para mantener trazabilidad y evitar agregaciones prematuras.
   ============================================================ */