from pydal import DAL, Field
import os
class database():
    def __init__(self,):
        self.migrate = True
        if os.path.exists(os.path.abspath('database/banco.db')):
            self.migrate = False
        self.DATABASE_TYPE = 'sqlite://'
        self.DATABASE = self.DATABASE_TYPE+os.path.abspath('database/banco.db')
        self.db = DAL(self.DATABASE,migrate=self.migrate)

    def create(self,):
        self.db.define_table('log',
            Field('date','datetime'),
            Field('time','datetime'),
            Field('phrase')
            )
        return self.db
