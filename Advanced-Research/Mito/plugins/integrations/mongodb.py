"""MongoDB Plugin"""
import os
from typing import Dict, List

class MongoDBClient:
    def __init__(self, uri: str = None, database: str = None):
        self.uri = uri or os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
        self.database = database or os.environ.get("MONGODB_DB", "mito")
    def _get_db(self):
        from pymongo import MongoClient
        return MongoClient(self.uri)[self.database]
    def find(self, collection: str, query: Dict = None, limit: int = 100) -> List[Dict]:
        db = self._get_db()
        return list(db[collection].find(query or {}, {"_id": 0}).limit(limit))
    def insert(self, collection: str, document: Dict) -> str:
        db = self._get_db()
        return str(db[collection].insert_one(document).inserted_id)
    def update(self, collection: str, query: Dict, update: Dict) -> int:
        db = self._get_db()
        return db[collection].update_many(query, {"$set": update}).modified_count
    def delete(self, collection: str, query: Dict) -> int:
        db = self._get_db()
        return db[collection].delete_many(query).deleted_count
    def count(self, collection: str, query: Dict = None) -> int:
        db = self._get_db()
        return db[collection].count_documents(query or {})
    def aggregate(self, collection: str, pipeline: List[Dict]) -> List[Dict]:
        db = self._get_db()
        return list(db[collection].aggregate(pipeline))

def register(plugin): plugin.set_resource("client_class", MongoDBClient)
mongodb_plugin = {"metadata": {"name": "mongodb", "version": "1.0.0", "description": "MongoDB document database", "author": "Mito Team", "license": "MIT", "tags": ["mongodb", "database", "nosql"], "permissions": ["network_access", "read_env"], "min_mito_version": "1.0.0"}, "register": register}
