import os

# Ruta donde se guardará el archivo style.css
ruta = os.path.join('inicio', 'static', 'css')
os.makedirs(ruta, exist_ok=True)

# Crea un archivo CSS básico
with open(os.path.join(ruta, 'style.css'), 'w') as f:
    f.write("""
/* Estilos iniciales para el dashboard */
.linea-titulo {
    color: white;
    padding: 5px 10px;
    border-radius: 8px;
    font-weight: bold;
    display: inline-block;
    font-size: 20px;
}
.linea-1 { background-color: #8e44ad; }  /* Morado */
.linea-2 { background-color: #2980b9; }  /* Azul */
.linea-6 { background-color: #27ae60; }  /* Verde */
.linea-7 { background-color: #e67e22; }  /* Naranja */
.linea-12 { background-color: #c0392b; } /* Rojo */
.linea-13 { background-color: #f1c40f; } /* Amarillo */
.linea-18 { background-color: #34495e; } /* Gris oscuro */
""")
