# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class LiveStreams(models.Model):
    channel_id = models.CharField(max_length=256, primary_key=True)
    channel_name = models.TextField(blank=True, null=True)
    is_live = models.BooleanField(blank=True, null=True)
    log_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'live_streams'

class VideoLifecycle(models.Model):
    video_id = models.CharField(max_length=256)
    video_title = models.TextField(blank=True, null=True)
    channel_id = models.CharField(max_length=256)
    channel_name = models.TextField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    favorites = models.IntegerField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True)
    dislikes = models.IntegerField(blank=True, null=True)
    video_duration = models.TextField(blank=True, null=True)
    thumbnail_url = models.TextField(blank=True, null=True)
    date_uploaded = models.DateTimeField(blank=True, null=True)
    record_timestamp = models.DateTimeField(primary_key=True)

    class Meta:
        managed = False
        unique_together = (('video_id', 'record_timestamp'),)
        db_table = 'video_view_lifecycle'

class GeographyColumns(models.Model):
    f_table_catalog = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_table_schema = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_table_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_geography_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    coord_dimension = models.BigIntegerField(blank=True, null=True)
    srid = models.BigIntegerField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geography_columns'

class GeometryColumns(models.Model):
    f_table_catalog = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_table_schema = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_table_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_geometry_column = models.TextField(blank=True, null=True)  # This field type is a guess.
    coord_dimension = models.BigIntegerField(blank=True, null=True)
    srid = models.BigIntegerField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geometry_columns'


class SpatialRefSys(models.Model):
    srid = models.BigIntegerField(blank=True, null=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.BigIntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'
