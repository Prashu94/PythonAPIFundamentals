from sqlalchemy import MetaData, Table, create_engine
metadata = MetaData()
engine = create_engine('sqlite:///Chinook_Sqlite.sqlite')
# Load the artist table- Reflecting the artist table
artist = Table('artist', metadata, autoload=True, autoload_with=engine)
# Load the album table- Reflecting the album table
album = Table('album', metadata, autoload=True, autoload_with=engine)
# Get the column names of the artist table
print(artist.columns.keys())

# Select the data of artist table
from sqlalchemy import select
s = select([artist]).limit(10)
print(engine.execute(s).fetchall())

# Get the column names of the album table
print(album.columns.keys())

# Adding ForeignKeyConstraint to the album table
from sqlalchemy import ForeignKeyConstraint
album.append_constraint(
    ForeignKeyConstraint(['ArtistId'], ['artist.ArtistId'])
)

print(metadata.tables['album'])
print(album.foreign_keys)
# Joining Tables String representation
print(str(artist.join(album)))

# Statement to reflect the whole database
print(metadata.reflect(bind=engine))

# Reflect the table names of the database
print(metadata.tables.keys())

# Get the playlist table
playlist = metadata.tables['Playlist']

# Select the data from the playlist
from sqlalchemy import select
s = select([playlist]).limit(10)
print(engine.execute(s).fetchall())