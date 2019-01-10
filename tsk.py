#!/usr/bin/python3

import os
import json
import argparse
from subprocess import Popen, STDOUT, DEVNULL, TimeoutExpired, run
from time import sleep
from math import ceil, log


processes = []


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
        self.process = Popen(
            self.cmd, cwd=self.pwd, stdout=self.log, stderr=STDOUT
        )

    def kill(self):
        if self.dead: return

        print(f'Stopping {self.name}...')
        if os.name == 'nt':
            # process.kill() seems to be basically worthless on Windows
            run(f'taskkill /F /T /PID {self.process.pid}')

        self.process.kill()

    def toggle(self):
        self.start() if self.dead else self.kill()

    def cleanup(self):
        self.kill()
        if self.log and not self.log.closed:
            self.log.close()


def main(config):
    with open(config, 'r') as f:
        config = json.load(f)

    # Prepare log directory
    log_dir = config.get('logs', os.path.join('~', '.tsk.logs'))
    log_dir = os.path.expanduser(log_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    try:
        # Create process objects
        processes.extend(
            Process(**p, log_dir=log_dir) for p in config.get('processes', {})
        )

        if not processes:
            print('No processes to manage.')
            return

        # Main menu loop
        while True:
            menu()
            selection = input('\nSelect a process to stop or start: ').lower()
            process, quit = select(selection)

            if quit: break
            if not process: continue

            process.toggle()
            sleep(1)

    finally:
        for process in processes:
            process.cleanup()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def width(items, min_length=0):
    return max(min_length, *(len(i) for i in items)) if items else min_length


def menu():
    clear()
    print('TSK PROCESS MANAGER\n')

    iw = ceil(log(len(processes) + 1, 10))
    nw = width((p.name for p in processes), 15)
    sw = width(p.status for p in processes)
    lw = width(p.log_file for p in processes)

    print(f'{" " * iw}  {"PROCESS":{nw}}   {"STATUS":{sw}}   {"LOG FILE":{lw}}')
    for i, p in enumerate(processes):
        print(f'{i + 1:>{iw}}: {p.name:{nw}}   {p.status:{sw}}   {p.log_file:{lw}}')

    print(f'\n{"Q":>{iw}}: Quit')


def select(selection):
    if selection == 'q': return None, True

    try:
        return processes[int(selection) - 1], False
    except:
        return None, False


if __name__ == '__main__':
    default_config = os.path.expanduser(os.path.join('~', '.tsk.json'))

    parser = argparse.ArgumentParser()
    parser.add_argument('config', nargs='?', default=default_config)
    args = parser.parse_args()

    main(args.config)
