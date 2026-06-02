# %% [markdown]
# # Proyecto: Pipeline de Ingesta (Semana 1)
#
# Este archivo usa "Celdas" para dividir el codigo y probarlo paso a paso.

# %% [markdown]
# ## 1. Configuracion Inicial
# Importamos las librerias que instalamos con 'uv'

# %% [imports]
import pandas as pd
import sys
import os

print("[OK] Librerias cargadas exitosamente")

# %% [main_function]
def main():
    print("Hello from pepeline-ingesta!")
    
    # Prueba rapida para ver que Pandas funciona
    df = pd.DataFrame({
        'columna_a': [1, 2, 3], 
        'columna_b': [10, 20, 30]
    })
    
    print("\nDataFrame de prueba:")
    print(df) 
    
    print("\n[OK] Pipeline completado correctamente")

# %% [ejecucion]
# Este bloque verifica si el script se esta corriendo directamente
if __name__ == "__main__":
    main()