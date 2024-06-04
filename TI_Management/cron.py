from django.core.management import call_command


def ti_management_backup():
    try:
        call_command('dbbackup')
        call_command('mediabackup')
    except:
        pass