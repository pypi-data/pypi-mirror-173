import six
from pyfiglet import figlet_format

try:
    from termcolor import colored
except ImportError:
    colored = None


def clilog(string, color='white', on_color=None, font='slant', figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color, on_color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)
