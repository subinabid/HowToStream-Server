# HowToStream-Server
FastAPI server for **HowToStream**

## Setup
Open the `htsserver.code-workspace` file if you are using VS Code. The workspace will suggest that you install the recommended extensions. Install the extensions

The project uses `pre-commit`to handle git hooks.

```shell
pip install pre-commit
pre-commit install
```

We love unit tests
```shell
pip install pytest
```

## Requirements
```shell
pip install fastapi
```

## Configuration
In `main.py` set `MODE` to `test` or `prod` to switch between test and production modes. Default is test.

## Initiate database
Sqlite is used for the project. If you are unsing the `hts.db` file in the repository, you can skip this step. You may also run the below command to setup a local copy.

```shell
python hts/scripts/seeddb.py
```

You may have to run ```python3 db.py``` based on your machine setup. This initiates the db, creates the required tables and populate the `movies` table with IMDb top 250 movies. This will also create a `streams` table.

Since the IMDb list is dynamic, if you run the command multiple times, it may add more movies to the list and the total rows in the `movies` table could be >250. This is not an error and can be ignored.

## Running the development server
```shell
fastapi dev main.py
```
Open http://127.0.0.1:8000/docs in the browser.
