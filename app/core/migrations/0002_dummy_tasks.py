from django.db import migrations

def create_dummy_tasks(apps, schema_editor):
    Task = apps.get_model('core', 'Task')

    Task(title='Workout', content='Squat, bench press, deadlift.').save()
    Task(title='Shopping', content='Whey protein, creatine, BCAAs.').save()
    Task(title='Counting', content='1, 2, 3 and so on.').save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_dummy_tasks),
    ]