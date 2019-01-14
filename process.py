import os
import platform
from subprocess import Popen, run, STDOUT
from getch import getch


class Process:
    def __init__(self, name, cmd, pwd, log_dir):
        self.name = name
        self.cmd = cmd
        self.pwd = os.path.expanduser(pwd) if pwd else None
        self.log_file = os.path.join(log_dir, f'{name}.log')
        self.log = None
        self.process = None

    @property
    def dead(self):
        return not self.process or self.process.poll() is not None

    @property
    def status(self):
        if not self.process:
            return 'Not Started'
        if self.dead:
            return f'Stopped (Code {self.process.poll()})'
        return 'Running'

    def start(self):
        if not self.dead:
            print(f'{self.name} is already running!')
            return

        if not self.log:
            self.log = open(self.log_file, 'w+')

        print(f'Starting {self.name}...')
        try:
            self.process = Popen(
                self.cmd, cwd=self.pwd, stdout=self.log, stderr=STDOUT
            )
        except Exception as e:
            return e

    def kill(self):
        if self.dead: return

        print(f'Stopping {self.name}...')
        if platform.system() == 'Windows':
            # process.kill() seems to be basically worthless on Windows
            run(f'taskkill /F /T /PID {self.process.pid}')

        self.process.kill()

    def toggle(self):
        return self.start() if self.dead else self.kill()

    def cleanup(self):
        self.kill()
        if self.log and not self.log.closed:
            self.log.close()

