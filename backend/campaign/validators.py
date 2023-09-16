def validate_file_size(value):
    if value.size > 20 * 1024 * 1024:
        raise ValidationError("File size cannot exceed 20MB.")


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp3', '.m4a', '.wav']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Only .mp3, .m4a and .wav files are allowed.')


def validate_file_duration(value):
    audio = AudioSegment.from_file(value.path)
    duration_in_seconds = len(audio)
    if duration_in_seconds > 45:
        raise ValidationError('File duration cannot exceed 45 seconds.')
