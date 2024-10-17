import sys
from cx_Freeze import setup, Executable

# Definir as opções de build (inclua as bibliotecas que deseja)
build_exe_options = {
    "packages": ["os", "pandas", "openpyxl", "requests", "json", "numpy", "tkinter", "dotenv", "PIL"],
    "include_files": [".env"],
}


# Base para a criação do executável
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Isso remove a janela do console se estiver usando Tkinter

# Configuração do cx_Freeze
setup(
    name="Dato_Buslog.v2",
    version="2.0",
    description="Aplicação gera e rastreia encomendas Buslog!",
    options={"build_exe": build_exe_options},
    executables=[Executable("dato_buslog.py", base=base)],  # Altere "app.py" para o nome do seu script principal
)
