from peewee import *

DATABASE = SqliteDatabase('videos.db')

class Video(Model):
	video_id = CharField(max_length=100, unique=True)
	title = CharField(max_length=250)
	publication_date = CharField(max_length=250)

	class Meta:
		database = DATABASE

	@classmethod
	def create_video(cls, video_id, title, publication_date):
		try:
			cls.create(
			video_id=video_id,
			title=title,
			publication_date=publication_date)
		except IntegrityError:
			raise ValueError('Video already exists')

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Video], safe=True)
	DATABASE.close()

if __name__ == "__main__":
	initialize()