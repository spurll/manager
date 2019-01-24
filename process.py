import os.path
import platform
from subprocess import Popen, run, STDOUT, TimeoutExpired
from getch import getch
from logroll import logroll


class Process:
    def __init__(
        self, name, cmd, log_dir,
        cwd=None,
        stop=None,
        timeout=None,
        shell=False,
        taskkill=False,
        log_archive=10
    ):
        self.name = name
        self.cmd = cmd
        self.cwd = os.path.expanduser(cwd) if cwd else None
        self.log_file = os.path.join(log_dir, f'{name}.log')
        self.stop_cmd = stop
        self.stop_timeout = timeout if timeout else 30
        self.shell = shell
        self.taskkill = taskkill
        self.log_archive = log_archive
        self.log = None
        self.process = None

    @property
    def stopped(self):
        return not self.process or self.process.poll() is not None

    @property
    def logging(self):
        return self.log and not self.log.closed

    @property
    def status(self):
        if not self.process:
            return 'Not Started'
        if self.stopped:
            return f'Stopped (Code {self.process.poll()})'
        return 'Running'

    def start(self):
        if not self.stopped:
            print(f'{self.name} is already running!')
            return

        if not self.logging:
            try:
                logroll(self.log_file, self.log_archive)
            except Exception as e:
                print(f'Error archiving logs: {e}')
            self.log = open(self.log_file, 'w+')

        print(f'Starting {self.name}...')
        try:
            self.process = Popen(
                self.cmd,
                cwd=self.cwd,
                shell=self.shell,
                stdout=self.log,
                stderr=STDOUT
            )
        except Exception as e:
            return e

    def stop(self):
        if self.stopped:
            self.close_log()
            return

        if self.stop_cmd:
            print(f'Issuing stop command for {self.name}...')
            try:
                stop_proc = run(
                    self.stop_cmd,
                    cwd=self.cwd,
                    stdout=self.log,
                    stderr=STDOUT,
                    timeout=self.stop_timeout
                )
            except TimeoutExpired:
                print(f'Stop command for {self.name} timed out.')
                self.kill()

            self.close_log()

        else:
            self.kill()

    def kill(self):
        if self.stopped:
            self.close_log()
            return

        print(f'Killing {self.name}...')

        if self.taskkill and platform.system() == 'Windows':
            # process.kill() sometimes has problems killing child processes
            run(f'taskkill /F /T /PID {self.process.pid}')

        self.process.kill()
        self.close_log()

    def toggle(self):
        return self.start() if self.stopped else self.stop()

    def close_log(self):
        if self.logging:
            try:
                self.process.wait(timeout=10)
            except TimeoutExpired:
                print('Timed out waiting for log file to close.')
            self.log.flush()
            self.log.close()

    def cleanup(self):
        self.stop()     # Attempt to halt gracefully first
        self.kill()
        self.close_log()

