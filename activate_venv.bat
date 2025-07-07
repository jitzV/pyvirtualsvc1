:: filepath: d:\_MyLearnings\PycharmProjects\18_FassAPI_ModuleExample\activate_venv.bat

@echo off
:: Check if the virtual environment directory exists
if exist "venv\Scripts\activate.bat" (
    :: Activate the virtual environment
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo Error: Virtual environment not found. Please create it first.
)