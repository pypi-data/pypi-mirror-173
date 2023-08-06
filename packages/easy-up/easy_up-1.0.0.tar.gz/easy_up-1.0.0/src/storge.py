import firebase_admin
from firebase_admin import firestore
import os


class Storage:
    """
    Document Func
    'collection', 'collections', 'create', 'delete', 'get', 'id', 'on_snapshot',
    'parent', 'path', 'set', 'update'

    Collection
    Func 'add', 'document', 'end_at', 'end_before', 'get', 'id', 'limit',
    'limit_to_last', 'list_documents', 'offset', 'on_snapshot', 'order_by',
    'parent', 'recursive', 'select', 'start_after', 'start_at', 'stream',
    'where'
    """


    def __init__(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'E:\my-developer\cli_package_manager\update-manager-c767d-firebase-adminsdk-ukjho-bc56cea676.json'
        self.__app = firebase_admin.initialize_app()
        self.__db = firestore.client()


    def add_package(self, package_id, **kwargs) -> firestore:
        new_package = self.__db.collection('packages').document(package_id)
        new_package.set(kwargs)
        return new_package


    def get_all(self) -> list:
        packages = self.__db.collection('packages').stream()
        elements = []
        for package in packages:
            elements.append(package)
        return elements


    def get_package(self, package_id) -> firestore:
        package = self.__db.collection('packages').document(package_id)
        return package


    def is_exists(self, package_id):
        package = self.__db.collection('packages').document(package_id)
        if package.get().to_dict() is not None:
            return True
        return False


    def update_package(self, package_id, **kwargs):
        if self.is_exists(package_id):
            package = self.get_package(package_id)
            package.update(kwargs)
            return package
        raise 'Not Found Package 404.'


    def delete_package(self, package_id):
        package = self.get_package(package_id)
        package.delete()
