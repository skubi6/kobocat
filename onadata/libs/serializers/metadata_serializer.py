# coding: utf-8
import mimetypes

from django.conf import settings
from django.core.validators import URLValidator
from django.utils.translation import ugettext as _
from rest_framework import serializers

from onadata.apps.main.models.meta_data import MetaData
from onadata.apps.logger.models import XForm

METADATA_TYPES = (
    ('data_license', _("Data License")),
    ('form_license', _("Form License")),
    ('media', _("Media")),
    ('public_link', _("Public Link")),
    ('source', _("Source")),
    ('supporting_doc', _("Supporting Document")),
)


class MetaDataSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    xform = serializers.PrimaryKeyRelatedField(queryset=XForm.objects.all())
    data_value = serializers.CharField(max_length=255,
                                       required=False)
    data_type = serializers.ChoiceField(choices=METADATA_TYPES)
    data_file = serializers.FileField(required=False)
    data_file_type = serializers.CharField(max_length=255, required=False)
    from_kpi = serializers.BooleanField(required=False)

    class Meta:
        model = MetaData
        fields = (
            'id',
            'xform',
            'data_value',
            'data_type',
            'data_file',
            'data_file_type',
            'file_hash',
            'url',
            'from_kpi',
        )

    # was previously validate_data_value but the signature change in DRF3.
    def validate(self, attrs):
        """
        Ensure we have a valid url if we are adding a media uri
        instead of a media file
        """
        value = attrs.get('data_value')
        media = attrs.get('data_type')
        data_file = attrs.get('data_file')
        data_file_type = attrs.get('data_file_type')

        if media == 'media' and data_file is None:
            URLValidator(message=_("Invalid url %s." % value))(value)

        if value is None:
            msg = {'data_value': _('This field is required.')}
            raise serializers.ValidationError(msg)

        attrs['data_file_type'] = self._validate_data_file_type(
            data_file_type=data_file_type, data_file=data_file, data_value=value
        )
        return super().validate(attrs)

    def create(self, validated_data):
        data_type = validated_data.get('data_type')
        data_file = validated_data.get('data_file')
        data_file_type = validated_data.get('data_file_type')
        from_kpi = validated_data.get('from_kpi', False)
        xform = validated_data.get('xform')
        file_hash = validated_data.get('file_hash')
        data_value = (
            data_file.name if data_file else validated_data.get('data_value')
        )

        return MetaData.objects.create(
            data_type=data_type,
            xform=xform,
            data_value=data_value,
            data_file=data_file,
            data_file_type=data_file_type,
            file_hash=file_hash,
            from_kpi=from_kpi,
        )

    def _validate_data_file_type(self, data_file_type, data_file, data_value):

        data_value = (
            data_file.name if data_file else data_value
        )
        allowed_types = settings.SUPPORTED_MEDIA_UPLOAD_TYPES

        if not data_file_type:
            data_file_type = (
                data_file.content_type
                if data_file and data_file.content_type in allowed_types
                else mimetypes.guess_type(data_value)[0]
            )

        if data_file_type not in allowed_types:
            raise serializers.ValidationError(
                {'data_file_type': _('Invalid content type.')}
            )

        return data_file_type
