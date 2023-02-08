from rest_framework import serializers


class FileSerializer(serializers.Serializer):
    file_to_upload = serializers.FileField(required=True)