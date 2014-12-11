import os
import subprocess
import atexit
import signal

from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import Command\
    as StaticfilesRunserverCommand


class Command(StaticfilesRunserverCommand):
    """
    Runserver that also uses grunt
    http://lincolnloop.com/blog/simplifying-your-django-frontend-tasks-grunt/
    """

    help = "Runs `grunt default` before launching Django's own runserver"

    def inner_run(self, *args, **options):
        if settings.USE_GRUNT:
            self.start_grunt()
            
        return super(Command, self).inner_run(*args, **options)

    def start_grunt(self):
        self.stdout.write('>>> Starting grunt')
        self.grunt_process = subprocess.Popen(
            ['cd %s && grunt' % settings.BASE_DIR],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=self.stdout,
            stderr=self.stderr,
        )

        self.stdout.write(
            '>>> Grunt process on pid {0}'.format(self.grunt_process.pid))

        def kill_grunt_process(pid):
            self.stdout.write('>>> Closing grunt process')
            os.kill(pid, signal.SIGTERM)

        atexit.register(kill_grunt_process, self.grunt_process.pid)
