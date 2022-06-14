import os
import time
import sys

def hibernate(seconds):
    print("Waiting %i Seconds for Hibernation" % seconds)

    for remaining in range(seconds, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rComplete!            \n")

    print("Starting Hibernation")
    # hibernate after the parameter sweep has ended
    os.system("shutdown.exe /h")

if __name__ == '__main__':
    hibernate(10)