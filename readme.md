# Demo Web Deployment App

Simple app to demo using `flask-bootstrap` to generate web page simulating remote monitoring/deployment.

## Building with pyinstaller

```console
(.venv) C:\Users\plundeen\PyProxy\src> pyinstaller --clean --onefile --add-data 'templates;templates' --add-data 'static;static' --additional-hooks-dir=hooks .\server.py
```

* `--clean` : cleans the output directories prior to build
* `--onefile`: generate a single .exe file for the resulting output
* `--add-data`: adds folders to the output (nested within the exe file)
  * `templates` and `static` folders are added, using same relative paths
* `--addtional-hooks-dir`: points to the `hooks` folder to run custom hooks at build time
  * these include actions to ensure pyinstaller gathers external resources, like bootstrap templates
