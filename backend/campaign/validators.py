import os

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from pydub.utils import which
from pydub import AudioSegment

AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

def ticket_safe_extensions(value):
    file = value.file if hasattr(value, 'file') else value

    ext = os.path.splitext(file.name)[1]
    valid_extensions = ['.mp3', '.m4a', '.wav', '.jpg', '.jpeg', '.png', '.gif', '.doc', '.docx',
                        '.xls', '.xlsx',
                        '.pdf', ".webm", " .mov", ".ogg", ".mp4", ".mkv"]

    if not ext.lower() in valid_extensions:
        raise ValidationError(
            'Only .mp3, .m4a, .wav, .jpg, .jpeg, .png, .gif, .doc, .docx, .xls, .xlsx, .webm, .mov, .ogg, .mp4, .mkv and .pdf files are allowed.'
        )


def validate_file_size(value):
    if value.size > 20 * 1024 * 1024:
        raise ValidationError("File size cannot exceed 20MB.")


@deconstructible
class FileSizeValidator:
    message = _(
        "File size %(size)sMB exceeds the limit of %(max_size)sMB."
    )
    code = "file_too_large"

    def __init__(self, max_size_mb=20, message=None, code=None):
        self.max_size_mb = max_size_mb
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):

        try:
            size = value.file.size  # from the uploaded file
        except AttributeError:
            size = value.size  # fallback (might fail with remote)

        size_mb = size / (1024 * 1024)
        if size_mb > self.max_size_mb:
            raise ValidationError(
                self.message,
                code=self.code,
                params={
                    "size": round(size_mb, 2),
                    "max_size": self.max_size_mb,
                    "value": value,
                },
            )

    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.max_size_mb == other.max_size_mb
                and self.message == other.message
                and self.code == other.code
        )


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp3', '.m4a', '.wav']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Only .mp3, .m4a and .wav files are allowed.')


def validate_file_duration(value):
    try:
        file = value.file if hasattr(value, 'file') else value

        file.seek(0)

        audio = AudioSegment.from_file(file)
        duration_ms = len(audio)  # duration in milliseconds
        max_duration_ms = 45 * 1000  # 45 seconds

        if duration_ms > max_duration_ms:
            raise ValidationError("Audio duration exceeds 45 seconds.")
    except Exception as e:
        raise ValidationError("Invalid or unreadable audio file.")


def video_validator(value):
    file = value.file if hasattr(value, 'file') else value

    ext = os.path.splitext(file.name)[1]
    valid_extensions = [".webm", " .mov", ".ogg", ".mp4", ".mkv"]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Only .webm , .mov , .ogg , .mp4 , .mkv files are allowed.')


def validate_template_format(value):
    valid_extensions = ['.html', '.htm', 'html', 'htm']
    ext = value.name.lower().split('.')[-1]
    if ext not in valid_extensions:
        raise ValidationError(
            f'Invalid file format. Only {", ".join(valid_extensions)} files are allowed.'
        )
