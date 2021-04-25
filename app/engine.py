import sqlalchemy

user = 'postgres'
password = '1234'
server = 'localhost'
port = '5432'
db = 'COVID'

connection = 'postgresql://{user}:{password}@{server}:{port}/{db}'.format(user=user,
                                                             password=password,
                                                             server=server,
                                                             port=port,
                                                             db=db
                                                            )

engine = sqlalchemy.create_engine(connection)