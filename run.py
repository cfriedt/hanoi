#!/usr/bin/env python3

import os
import sys

sys.path.append(os.environ['PWD'] + '/src')

from hanoi import app

if __name__ == '__main__':
    app.run(host='::', port=8080)
