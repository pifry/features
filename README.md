1. Quickstart

   - install dependencies: `pip install -r requirements` . You may want to setup virtual environment first.
   - run python main.py -h

2. Features implemented

3. Contribution

   - Before commit run `make format` .
   - If you add new source file, update Makefile SRC variable.
   - name your commits with tags:

     - [DOC] - for documentation update
     - [CODE] - for functionality changes
     - [CI/CD] - for CI/CD related changes
     - [REFACTOR] - for refactoring

4. How to implement feature

Loook at [features.py](features.py) file. You can add feature by implementing Feature class method which name starts with `feature_` , accepts video object as a parameter and return scalar.
