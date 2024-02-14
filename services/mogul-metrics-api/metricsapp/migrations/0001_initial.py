# Generated by Django 4.0.4 on 2022-05-03 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeographyColumns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_table_catalog', models.TextField(blank=True, null=True)),
                ('f_table_schema', models.TextField(blank=True, null=True)),
                ('f_table_name', models.TextField(blank=True, null=True)),
                ('f_geography_column', models.TextField(blank=True, null=True)),
                ('coord_dimension', models.BigIntegerField(blank=True, null=True)),
                ('srid', models.BigIntegerField(blank=True, null=True)),
                ('type', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'geography_columns',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GeometryColumns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_table_catalog', models.TextField(blank=True, null=True)),
                ('f_table_schema', models.TextField(blank=True, null=True)),
                ('f_table_name', models.TextField(blank=True, null=True)),
                ('f_geometry_column', models.TextField(blank=True, null=True)),
                ('coord_dimension', models.BigIntegerField(blank=True, null=True)),
                ('srid', models.BigIntegerField(blank=True, null=True)),
                ('type', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'geometry_columns',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SpatialRefSys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('srid', models.BigIntegerField(blank=True, null=True)),
                ('auth_name', models.CharField(blank=True, max_length=256, null=True)),
                ('auth_srid', models.BigIntegerField(blank=True, null=True)),
                ('srtext', models.CharField(blank=True, max_length=2048, null=True)),
                ('proj4text', models.CharField(blank=True, max_length=2048, null=True)),
            ],
            options={
                'db_table': 'spatial_ref_sys',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LiveStreams',
            fields=[
                ('channel_id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('channel_name', models.TextField(blank=True, null=True)),
                ('is_live', models.BooleanField(blank=True, null=True)),
                ('log_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'live_streams',
            },
        ),
    ]
