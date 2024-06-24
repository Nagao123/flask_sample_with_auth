from .database import db

class CRUD:
     
    def db_insert(self, table_obj):

        try:
            db.session.add(table_obj)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return False
        finally:
            db.session.close()
        
        return True