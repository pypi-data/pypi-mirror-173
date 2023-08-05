__version__ = "0.1.2"

import sys, os
from .CourseWatcher import watch_courses, die

def main():
    if os.getuid() == 0:
        die("Nope, I'm not doing anything as root. Come back when you've acquired a brain!")

    if len(sys.argv) != 2:
        die("A config file has to be specified as a parameter!")
    watch_courses(sys.argv[1])
