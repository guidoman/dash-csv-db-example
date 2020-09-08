from sqlalchemy import Table, Column, String, MetaData, create_engine

db_file_name = 'my-data.db'

engine = create_engine(f'sqlite:///{db_file_name}', echo=True)

meta = MetaData()

my_data = Table(
    'my_data', meta,
    Column('yyyymmdd', String, primary_key=True),
    Column('csv', String),
)
