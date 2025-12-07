#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 01:17:37 2025

@author: florenciabravocatalan
"""
# --------------------------------------------------------------
# 05_decodificacion_grupo_hibrido.py
# Pipeline híbrido:
# - Usa TODOS los voxeles (sin máscara, sin resample)
# - Convierte a float32 (menos memoria)
# - Normalización por volumen (L2)
# - Estandarización voxel-wise (StandardScaler)
# - Selección de voxeles (SelectKBest, K=5000 o menos)
# - Logistic Regression
# --------------------------------------------------------------

import os
import numpy as np
import pandas as pd

from nilearn import image

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Sujetos incluidos
SUJETOS = ["sub-02", "sub-03", "sub-04", "sub-05"]

# Ruta base (ajustada a tu Mac)
ROOT = "/ruta/a/tu/dataset/ds000117"



def clasificar(nombre):
    """
    Convierte el nombre del estímulo en etiqueta binaria:
    0 = scrambled (empieza con func/s)
    1 = cara (famosa o unfamiliar)
    """
    if nombre.startswith("func/s"):
        return 0
    else:
        return 1


print("Iniciando DECODIFICACIÓN MULTISUJETO - PIPELINE HÍBRIDO\n")

resultados = {}

# --------------------------------------------------------------
# PROCESAR CADA SUJETO
# --------------------------------------------------------------
for sub in SUJETOS:

    print(f"\n===== Procesando {sub} =====")

    func_dir = os.path.join(ROOT, sub, "func")

    X_total = []
    y_total = []

    # Procesar los 9 runs
    for run in range(1, 10):

        print(f"  - RUN {run}...")

        bold_file = f"{sub}_ses-mri_task-facerecognition_run-0{run}_bold.nii"
        events_file = f"{sub}_ses-mri_task-facerecognition_run-0{run}_events.txt"

        bold_path = os.path.join(func_dir, bold_file)
        events_path = os.path.join(func_dir, events_file)

        # 1) Cargar imagen BOLD
        bold_img = image.load_img(bold_path)
        bold_data = bold_img.get_fdata().astype("float32")  # float32 = menos memoria

        # bold_data tiene shape (x, y, z, t)
        n_vols = bold_data.shape[-1]
        n_voxels = np.prod(bold_data.shape[:-1])

        # Reorganizar a (volúmenes, voxeles)
        X_run = bold_data.reshape(n_voxels, n_vols).T  # (n_vols, n_voxels)

        # 2) Cargar eventos y crear etiquetas
        events = pd.read_csv(events_path, sep="\t")
        events["label"] = events["stim_file"].apply(clasificar)

        # 3) Emparejar longitud
        min_len = min(n_vols, len(events))

        X_total.append(X_run[:min_len, :])
        y_total.append(events["label"].values[:min_len])

    # ------------------------------------------------------------
    # UNIR RUNS DEL SUJETO
    # ------------------------------------------------------------
    print("  Uniendo runs del sujeto...")
    X = np.vstack(X_total)   # (ensayos_totales, voxeles)
    y = np.hstack(y_total)   # (ensayos_totales,)

    print(f"  Dimensiones antes de preprocesar: X={X.shape}, y={y.shape}")

    # ------------------------------------------------------------
    # NORMALIZACIÓN POR VOLUMEN (norma L2)
    # ------------------------------------------------------------
    normas = np.linalg.norm(X, axis=1, keepdims=True)
    X = X / np.maximum(normas, 1e-8)

    # ------------------------------------------------------------
    # TRAIN/TEST SPLIT
    # ------------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42
    )

    # ------------------------------------------------------------
    # SELECCIÓN DE VOXELES + ESTANDARIZACIÓN + CLASIFICADOR
    # ------------------------------------------------------------
    n_features = X_train.shape[1]
    k_vox = min(5000, n_features)
    print(f"  Seleccionando {k_vox} voxeles más informativos...")

    scaler = StandardScaler()
    selector = SelectKBest(f_classif, k=k_vox)
    clf = LogisticRegression(max_iter=2000)

    # Estandarizar
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Seleccionar voxeles
    X_train = selector.fit_transform(X_train, y_train)
    X_test = selector.transform(X_test)

    print("  Entrenando modelo...")
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    resultados[sub] = acc
    print(f"  -> Accuracy {sub} (híbrido): {acc:.3f}")

# ------------------------------------------------------------
# RESULTADOS FINALES
# ------------------------------------------------------------
print("\n===== Accuracy por Sujeto (HÍBRIDO) =====")
for sub, acc in resultados.items():
    print(f"{sub}: {acc:.3f}")

media = np.mean(list(resultados.values()))
print(f"\n===== Accuracy Promedio (HÍBRIDO) =====")
print(f"Media grupo: {media:.3f}")
