# MVPA-fMRI-pipeline
Código del pipeline MVPA simplificado para análisis de fMRI ds000117
MVPA – Decodificación de fMRI en espacio nativo

Autoras: Sofía Binetti & Florencia Bravo

Este repositorio contiene el código utilizado para implementar un pipeline MVPA simplificado para decodificar estímulos rostro vs. scrambled utilizando el dataset público ds000117.

Dataset utilizado

Este análisis utiliza el dataset ds000117, publicado por Wakeman & Henson (2015), disponible de forma pública en OpenNeuro.

Descargar dataset aquí:
https://openneuro.org/datasets/ds000117

Referencia APA 7 del dataset:
Wakeman, D. G., & Henson, R. N. (2015). A multi-subject, multi-modal human neuroimaging dataset. Scientific Data, 2, 150001. https://doi.org/10.1038/sdata.2015.1

Organización del dataset local

Una vez descargado desde OpenNeuro, el dataset debe colocarse en una carpeta local con esta estructura:
/ruta/a/tu/dataset/ds000117/
    ├── sub-02/
    ├── sub-03/
    ├── sub-04/
    └── sub-05/
El usuario debe modificar la variable ROOT en el script para que apunte a esa ruta.
Cómo ejecutar el pipeline

Descargar el dataset desde OpenNeuro.

Ajustar la variable ROOT en el script.

Instalar dependencias: pip install numpy pandas scikit-learn nilearn
Ejecutar el script:
python 05_decodificacion_grupo_hibrido.py

El script imprimirá el accuracy por sujeto y el promedio grupal (~0.67).
