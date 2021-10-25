import signal
import sys
import time

if sys.platform == "win32":
    import msvcrt

# == Windows --------------------------------------------------------
def _input_with_timeout_win(prompt, timeout_secs: int, timer=time.monotonic) -> str:
    sys.stdout.write(prompt)
    sys.stdout.flush()
    endtime = timer() + timeout_secs
    result = []
    while timer() < endtime:
        if msvcrt.kbhit():
            endtime = timer() + timeout_secs  # Reset the timer
            ch = msvcrt.getwche()
            # result.append(msvcrt.getwche())   # XXX can it block on multibyte characters?
            if ch == "\b":
                if len(result) >= 1:
                    result = result[:-1]
                    print(' \b', end="", flush=True) 
                else:
                    # ESC [ <n> C  (move n chars right)
                    move_right = "\x1B\x5B\x31\x43"
                    print(move_right, end='', flush=True)
            elif ch == '\r':            # XXX check what Windows returns here
                print()
                # return ''.join(result[:-1])
                return ''.join(result)
            else:
                result.append(ch)
                
        time.sleep(0.04) # just to yield to other processes/threads
    print()
    raise TimeoutError('Time Expired.')

# == *nix ----------------------------------------------------------
def _alarm_handler(signum, frame):
    raise TimeoutError('time expired.')

def _input_with_timeout_nix(prompt: str, timeout_secs: int) -> str:
    # set signal handler
    signal.signal(signal.SIGALRM, _alarm_handler)
    signal.alarm(timeout_secs) # produce SIGALRM in `timeout` seconds

    try:
        return input(prompt)
    finally:
        signal.alarm(0) # cancel alarm


#====================================================================================
def input_with_timeout(prompt: str, timeout_secs: int, default: str = None) -> str:
    """Prompt for input with a timer"""
    try:
        if sys.platform == "win32":
            return _input_with_timeout_win(prompt, timeout_secs)
        else:
            return _input_with_timeout_nix(prompt, timeout_secs)
    except TimeoutError:
        return default

if __name__ == "__main__":
    timeout = 60
    default_response = "This is the default response!"
    response = input_with_timeout("The Prompt> ", timeout, default_response)
    print(f'Input prompt returns: {response}')
