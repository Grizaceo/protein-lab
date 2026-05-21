#!/usr/bin/env python3
"""
Script para añadir números de línea a un archivo markdown.
Crea una versión numerada del archivo original.
"""

import os
from pathlib import Path

def add_line_numbers(input_file, output_file=None):
    """
    Añade números de línea al principio de cada línea del archivo.
    
    Args:
        input_file: ruta del archivo de entrada
        output_file: ruta del archivo de salida (si es None, crea uno con sufijo _numbered)
    """
    
    # Validar que el archivo existe
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: El archivo {input_file} no existe")
        return False
    
    # Definir archivo de salida
    if output_file is None:
        output_path = input_path.parent / f"{input_path.stem}_numbered{input_path.suffix}"
    else:
        output_path = Path(output_file)
    
    try:
        # Leer el archivo
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Determinar el ancho para numerar (ej: si hay 1000 líneas, usar 4 dígitos)
        line_count = len(lines)
        width = len(str(line_count))
        
        # Añadir números de línea
        numbered_lines = []
        for i, line in enumerate(lines, 1):
            # Formato: "0001 | contenido original"
            numbered_line = f"{str(i).zfill(width)} | {line}"
            numbered_lines.append(numbered_line)
        
        # Escribir archivo de salida
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(numbered_lines)
        
        print(f"✓ Archivo procesado exitosamente")
        print(f"  Entrada:  {input_path}")
        print(f"  Salida:   {output_path}")
        print(f"  Líneas:   {line_count}")
        print(f"\nAhora puedes abrir '{output_path.name}' y exportarlo a PDF desde VS Code")
        return True
        
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return False


if __name__ == "__main__":
    # Ruta del archivo markdown
    input_file = "investigacion-fibromialgia/preprint_dopaminergic_convergence_FM.md"
    
    # Ejecutar
    add_line_numbers(input_file)
