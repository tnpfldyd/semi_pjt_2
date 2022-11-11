
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('content', models.TextField()),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='images/')),
                ('is_closed', models.BooleanField(default=True)),
                ('password', models.CharField(blank=True, max_length=4, null=True)),
                ('location', models.CharField(choices=[('선택', None), ('노원구', '노원구'), ('송파구', '송파구')], default='선택', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('meeting_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.meeting')),
            ],
        ),
    ]
