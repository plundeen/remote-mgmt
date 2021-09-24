from subprocess import Popen, PIPE, STDOUT
import datetime

# Constants
NIPKG = 'C:\\Program Files\\National Instruments\\NI Package Manager\\nipkg.exe'

def query(arg:str) -> str:
    """Function to perform an nipkg.exe query and return the results"""
    return ""

def install(package:str, version:str) -> None:
    """Function to trigger a package install and stream the stdout/stderr output"""
    # Question: can we provide a pipe as an input that this function can stream to?
    # Probably should be a websocket, right? Can we pass the socket in?
    # Or should this function just handle the full websocket stuff?
    pass