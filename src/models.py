from peewee import *

DATABASE = SqliteDatabase('videos.db')

class Video(Model):
    video_id = CharField(max_length=100, unique=True)
    title = CharField(max_length=250)
    publication_date = CharField(max_length=250)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Video], safe=True)

if __name__ == "__main__":
    initialize()