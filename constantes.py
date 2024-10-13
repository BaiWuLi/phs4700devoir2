import numpy as np

# Variables de sortie
coup = int
vbf = np.ndarray
ti = np.ndarray
x = np.ndarray
y = np.ndarray
z = np.ndarray

# Table
ht = 76e-2 # hauteur de la table
Lt = 2.74 # longueur de la table
lt = 1.525 # largeur de la table

# Filet
hf = 15.25e-2 # hauteur du filet
lf = 1.83 # largeur du filet
df = 15.25e-2 # debordement du filet

# Balle
mb = 2.74e-3 # masse de la balle
Rb = 1.99e-2 # rayon de la balle
Ab = np.pi * Rb**2 # aire efficace de la balle

p = 1.2 # masse volumique de l'air

Cv = 0.5 # coefficient de frottement visqueux

CM = 0.29 # coefficient de Magnus
