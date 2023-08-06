import subprocess
import sys
import watchfiles
import itertools

if len(sys.argv) == 1:
    print("Program name was not provided.")
    exit(1)

last_process = subprocess.Popen(["python", *sys.argv[1:]])
try:
    while True:
        for change, _path in itertools.chain.from_iterable(watchfiles.watch(sys.argv[1])):
            last_process.terminate()
            last_process = subprocess.Popen(["python", *sys.argv[1:]])
            if change == watchfiles.Change.deleted:
                break
except KeyboardInterrupt:
    last_process.terminate()
