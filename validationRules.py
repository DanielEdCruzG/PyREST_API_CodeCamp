from marshmallow import ValidationError, fields, Schema, EXCLUDE

class PostSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    publish = fields.Bool(required=False, default=True)
    rating = fields.Int(required=False, missing=None)

    class Meta:
        unknown = EXCLUDE

    def validate_title(self, data):
        if len(data) < 10:
            raise ValidationError('Title must be at least 10 characters long')
        if len(data) > 50:
            raise ValidationError('Title must be at most 50 characters long')

    def validate_content(self, data):
        if len(data) < 15:
            raise ValidationError('Content must be at least 15 characters long')
        if len(data) > 250:
            raise ValidationError('Content must be at most 250 characters long')
        
    def validate_rating(self, data):
        if data < 1:
            raise ValidationError('Rating must be at least 1')
        if data > 5:
            raise ValidationError('Rating must be at most 5')