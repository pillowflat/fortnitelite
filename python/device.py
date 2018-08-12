import subprocess

class Device():
    def __init__(self, name):
        self.name = name
        self.state = 0

    def on(self):
        if self.state == 0:
            print('Switching on...')
            self._switch('on')
            self.state = 1
        else:
            print('Switch is already on.')

    def off(self):
        if self.state == 1:
            print('Switching off...')
            self._switch('off')
            self.state = 0
        else:
            print('Switch is already off.')

    def _switch(self, state_name):
        command = 'wemo switch {} {}'.format(self.name, state_name).split()
        print('Command: {}'.format(command))
        subprocess.run(command)