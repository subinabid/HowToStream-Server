"""App settings."""

import os

# Configurations
prod_db_path = os.path.join(os.path.dirname(__file__), "hts.db")
test_db_path = os.path.join(os.path.dirname(__file__), "hts-test.db")

# test or prod mode
MODE = "test"  # test or prod

# database path
db_path = prod_db_path if MODE == "prod" else test_db_path
