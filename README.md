# Línea de producción de MVPA-fMRI  
Código del pipeline MVPA simplificado para análisis de fMRI (ds000117)

## MVPA – Decodificación de fMRI en espacio nativo  
Autoras: Sofía Binetti & Florencia Bravo  

Este repositorio contiene el código utilizado para implementar un pipeline MVPA simplificado para decodificar estímulos rostro vs. scrambled utilizando el conjunto de datos públicos ds000117.

## Conjunto de datos utilizado  
Este análisis utiliza el conjunto de datos ds000117, publicado por Wakeman & Henson (2015), disponible de forma pública en OpenNeuro.  
Descargar conjunto de datos: https://openneuro.org/datasets/ds000117  

### Referencia APA 7  
Wakeman, D. G., & Henson, R. N. (2015). *A multi-subject, multi-modal human neuroimaging dataset.* Scientific Data, 2, 150001. https://doi.org/10.1038/sdata.2015.1

## Organización del conjunto de datos local  
Una vez descargado desde OpenNeuro, el conjunto de datos debe colocarse en una carpeta local con esta estructura:
/ruta/a/tu/dataset/ds000117/
    ├── sub-02/
    ├── sub-03/
    ├── sub-04/
    └── sub-05/



Luego, el usuario debe modificar la variable ROOT en el script para que apunte a esta ruta:

ROOT = "/ruta/a/tu/dataset/ds000117"

## Cómo ejecutar el pipeline  
1. Descargue el conjunto de datos desde OpenNeuro.  
2. Ajuste la variable ROOT en el script.  
3. Instale las dependencias necesarias:  
pip install numpy pandas scikit-learn nilearn
4. Ejecute el script:  
python 05_decodificacion_grupo_hibrido.py
El script imprimirá la precisión por sujeto y el promedio grupal (~0.67).
