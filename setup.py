from cx_Freeze import setup, Executable

setup(name = "downloader",
      version = "0.1",
      description = "",
      options = {"build_exe": {"includes": ["idna.idnadata"]}},
      executables = [Executable("downloader.py")])
