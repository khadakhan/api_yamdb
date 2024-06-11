# Generated by Django 3.2 on 2024-06-11 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='rewiew',
            new_name='review_id',
        ),
        migrations.RemoveField(
            model_name='review',
            name='title',
        ),
        migrations.AddField(
            model_name='review',
            name='title_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.title'),
            preserve_default=False,
        ),
    ]
