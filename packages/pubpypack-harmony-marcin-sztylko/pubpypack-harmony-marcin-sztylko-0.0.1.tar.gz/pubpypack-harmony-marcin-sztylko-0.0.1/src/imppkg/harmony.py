import sys
import termcolor
from imppkg.harmonic_mean import harmonic_mean

def main():
    args = sys.argv[1:]
    numbers = [float(x) for x in args]
    mean = harmonic_mean(numbers)    
    termcolor.cprint(mean, 'white', 'on_green', attrs=['bold'])
