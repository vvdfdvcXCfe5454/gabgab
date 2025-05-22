from gabby_config import Config
import sys


def __list_all_modules():
    import glob
    from os.path import basename, dirname, isfile

    # This generates a list of gabby_modules in this folder for the * in __main__ to work.
    mod_paths = glob.glob(f"{dirname(__file__)}/*.py")
    all_modules = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    LOAD = getattr(Config, 'LOAD', [])
    NO_LOAD = getattr(Config, 'NO_LOAD', [])
    LOGGER = getattr(Config, 'LOGGER', True)

    if LOAD or NO_LOAD:
        to_load = LOAD
        if to_load:
            if not all(
                    any(mod == module_name for module_name in all_modules)
                    for mod in to_load
            ):
                print("[Gabby] Invalid loader names. Quitting.")
                sys.exit(1)

            all_modules = sorted(set(all_modules) - set(to_load))
            to_load = list(all_modules) + to_load
        else:
            to_load = all_modules

        if NO_LOAD:
            print(f"[Gabby] Not loading: {NO_LOAD}")
            return [item for item in to_load if item not in NO_LOAD]
        return to_load
    return all_modules


ALL_MODULES = __list_all_modules()

__all__ = ALL_MODULES + ["ALL_MODULES"]

from pymongo import MongoClient

MONGO_DB_URI = Config.MONGO_DB_URI
client = MongoClient(MONGO_DB_URI)
main_db = client["GABBY_DB"]
Gabbydb = main_db


def get_collection(name: str):
    return Gabbydb[name]


class MongoDB:
    def __init__(self, collection):
        self.collection = Gabbydb[collection]

    # Insert one entry into collection
    def insert_one(self, document):
        result = self.collection.insert_one(document)
        return repr(result.inserted_id)

    # Find one entry from collection
    def find_one(self, query):
        result = self.collection.find_one(query)
        if result:
            return result
        return False

    # Find entries from collection
    def find_all(self, query=None):
        if query is None:
            query = {}
        return list(self.collection.find(query))

    # Count entries from collection
    def count(self, query=None):
        if query is None:
            query = {}
        return self.collection.count_documents(query)

    # Delete entry/entries from collection
    def delete_one(self, query):
        self.collection.delete_many(query)
        return self.collection.count_documents({})

    # Replace one entry in collection
    def replace(self, query, new_data):
        old = self.collection.find_one(query)
        _id = old["_id"]
        self.collection.replace_one({"_id": _id}, new_data)
        new = self.collection.find_one({"_id": _id})
        return old, new

    # Update one entry from collection
    def update(self, query, update):
        result = self.collection.update_one(query, {"$set": update})
        new_document = self.collection.find_one(query)
        return result.modified_count, new_document

    @staticmethod
    def close():
        return client.close()


def __connect_first():
    _ = MongoDB("test")


__connect_first()