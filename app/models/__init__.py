from app.models.app_registry import AppRegistryModel
from app.models.auth import TokenBlocklistModel
from app.models.dataset import HousingModel
from app.models.dataset import LabourMarketModel
from app.models.dataset import TravelModel
from app.models.subscription import SubscriptionModel
from app.models.subscription import SubscriptionRecycledModel
from app.models.user import UserModel
from app.models.user import UserRecycledModel

# Notes: AUTOINCREMENT feature in SQLite & SQLAlchemy
# 1 - SQLite has an implicit “auto increment” feature. If a table contains a column of type `INTEGER PRIMARY KEY`,
#     then that column becomes an alias for the ROWID.
# 2 - Declared the column as `INTEGER PRIMARY KEY AUTOINCREMENT` to enable the generic autoincrement feature.
# 3 - To specifically render the AUTOINCREMENT keyword on the primary key column when rendering DDL,
#     add the flag `sqlite_autoincrement=True` to the Table construct.
