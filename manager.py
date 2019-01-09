#!/usr/bin/python3

import os
import json
import argparse
from subprocess import Popen, PIPE, TimeoutExpired, run
from time import sleep


processes = []


class Process:
    def __init__(self, name, cmd, pwd):
        self.name = name
        self.cmd = cmd
        self.pwd = pwd
        self.process = None

    def start(self):
        if not self.dead:
            print(f'{self.name} is already running!')
            return

        print(f'Starting {self.name}...')
        self.process = Popen(self.cmd, cwd=self.pwd, stdout=PIPE, stderr=PIPE)

    @property
    def dead(self):
        return not self.process or self.process.returncode is not None

    @property
    def status(self):
        if not self.process:
            return 'Not Started'
        if self.dead:
            return f'Stopped (Code {self.process.returncode})'
        return 'Running'

    def kill(self):
        if self.dead: return

        print(f'Killing the {self.name} process...')
        if os.name == 'nt':
            # process.kill() seems to be basically worthless on Windows
            run(f'taskkill /F /T /PID {self.process.pid}')

        self.process.kill()

    def kill_for_output(self):
        if not self.process:
            print(f'No output: the {self.name} process has not been started.')
            return

        try:
            # This will block until the process terminates
            print(f'Waiting for the {self.name} process to finish...')
            out, err = self.process.communicate(timeout=5)
        except TimeoutExpired:
            print(f'Killing the {self.name} process.')
            self.kill()
            out, err = self.process.communicate()

        print('\n----- STDOUT -----')
        print(out.decode(encoding='utf-8'))
        print('\n----- STDERR -----')
        print(err.decode(encoding='utf-8'))


def main(config):
    with open(config, 'r') as f:
        processes.extend(Process(**p) for p in json.load(f))

    if not processes:
        print('No processes to manage.')
        return

    # Main menu loop
    while True:
        clear()
        print('PROCESS MANAGER\n')

        for i, process in enumerate(processes):
            print(f'{i + 1}: {process.name:{name_width()}}   {process.status}')
        print('Q: Quit')

        selection = input('\nMake a selection: ').lower()
        process, done = select_for_menu(selection)

        if done: break
        if not process: continue

        # Process menu loop
        while not done:
            process_menu(process)
            selection = input('Make a selection: ').lower()
            done = select_for_process(process, selection)

    for process in processes:
        process.kill()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def name_width():
    return max(15, max(len(p.name) for p in processes))


def process_menu(process):
    clear()
    print('PROCESS MANAGER')
    print(f'Process: {process.name:{name_width()}}   Status: {process.status}\n')
    print(f'S: {"Start" if process.dead else "Stop"} Process')
    print(f'O: {"" if process.dead else "Stop and "}View Output')
    print('Q: Back to Menu\n')


def select_for_menu(selection):
    if selection == 'q': return None, True

    try:
        return processes[int(selection) - 1], False
    except:
        return None, False


def select_for_process(process, selection):
    if selection == 's':
        if process.dead:
            process.start()
        else:
            process.kill()
        sleep(1)

    elif selection == 'o':
        process.kill_for_output()
        input('\nPress ENTER to continue.')

    elif selection == 'q':
        return True

    return False


if __name__ == '__main__':
    default_config = os.path.expanduser(os.path.join('~', '.manager.json'))

    parser = argparse.ArgumentParser()
    parser.add_argument('config', nargs='?', default=default_config)
    args = parser.parse_args()

    main(args.config)
