from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey

engine = create_engine('mysql+pymysql://root:9713@localhost:3306/sa_test', echo=True)
metadata = MetaData(engine)

user_table = Table('user', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('name', String(50)),
                   Column('fullname', String(100))
                   )

# metadata.create_all()

address_table = Table('address', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('user_id', None, ForeignKey('user.id')),
                      Column('email', String(128), nullable=False)
                      )

address_table.create(checkfirst=True)

ins = user_table.insert()
conn = engine.connect()
result = conn.execute(ins, {'name': 'adam', 'fullname': 'Adam Gu'})
