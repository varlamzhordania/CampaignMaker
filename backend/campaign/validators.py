from django.core.exceptions import ValidationError
from pydub import AudioSegment
from django.conf import settings
import os


def validate_file_size(value):
    if value.size > 20 * 1024 * 1024:
        raise ValidationError("File size cannot exceed 20MB.")


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp3', '.m4a', '.wav']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Only .mp3, .m4a and .wav files are allowed.')


def validate_file_duration(value):
    try:
        audio = AudioSegment.from_file(value)
        duration_in_seconds = len(audio)
        max_duration = 45 * 1000
        if duration_in_seconds > max_duration:
            raise ValidationError('File duration cannot exceed 45 seconds.')
    except Exception as e:
        raise ValidationError(e)


def video_validator(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".webm", " .mov", ".ogg", ".mp4", ".mkv"]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Only .webm , .mov , .ogg , .mp4 , .mkv files are allowed.')


def validate_template_format(value):
    valid_extensions = ['.html', '.htm', 'html', 'htm']
    ext = value.name.lower().split('.')[-1]
    if ext not in valid_extensions:
        raise ValidationError(f'Invalid file format. Only {", ".join(valid_extensions)} files are allowed.')
