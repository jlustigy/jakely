import subprocess
import platform
    
def say(value, rate = 180):
    """
    Similar to the `print()` function, but for spoken text using the `say` command 
    on Mac OS
    
    Parameters
    ----------
    value : str
        String to be spoken
    rate : int
        Rate of speech in words per minute (default is 180)
    """
    
    if platform.system() != 'Darwin':
        print("`Say` only works on Macs")
    
    output = subprocess.call(["say", "-r %i" %rate, '"%s"' %value])