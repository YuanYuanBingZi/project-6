from mongoengine import *


class Controls(EmbeddedDocument):
    """
    A MongoEngine EmbeddedDocument containing:
       distance: MongoEngine float field, required, (checkpoint distance in kilometers),
		   location: MongoEngine string field, optional, (checkpoint location name),
		   open_time: MongoEngine datetime field, required, (checkpoint opening time),
		   close_time: MongoEngine datetime field, required, (checkpoint closing time).
    """
    # km = request.args.get('km', 999, type=float)
    # distance = request.args.get('distance',type=float)
    # open_time = acp_times.open_time(km, distance, start_time).format('YYYY-MM-DDTHH:mm')
    # close_time = acp_times.close_time(km, distance, start_time).format('YYYY-MM-DDTHH:mm')

    km = FloatField(required=True)
    open_time_field = StringField(required=True)
    close_time_field = StringField(required=True)


class Brevet(Document):
    """
    A MongoEngine document containing:
		length: MongoEngine float field, required
		start_time: MongoEngine datetime field, required
		checkpoints: MongoEngine list field of Checkpoints, required
    """
    brevet_dist = FloatField(required=True)
    start_time = StringField(required=True)
    controls = EmbeddedDocumentListField(Controls, required=True)
