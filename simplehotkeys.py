import threading, time

IN_WHILE_SLEEP = 0.01
PRESS_VS_LONGPRESS = 370/1000
LONGPRESS_VS_TOOLONGPRESS = 1600/1000
DOUBLEPRESS_BETWEEN = 300/1000
CALL_THREADED = True

# (TO CHOOSE BETWEEN pynput AND keyboard EDIT "def pressed ()" AND CHECK WHICH KEY FORMAT IS USED IN YOUR CODE (string VS pynput.Key)) - NOW AUTODETECTED (depends on whether you give <class 'str> or <enum 'Key'>)

## pynput ##
import pynput.keyboard 

pynput_keys_DOWN = []

def pynput_on_press_lambda (key):
    global pynput_keys_DOWN
    if not key in pynput_keys_DOWN:
        pynput_keys_DOWN.append(key)

def pynput_on_release_lambda (key):
    global pynput_keys_DOWN
    pynput_keys_DOWN=[x for x in pynput_keys_DOWN if x != key]

pynput_listener = pynput.keyboard.Listener(
    on_press=pynput_on_press_lambda,
    on_release=pynput_on_release_lambda 
    ).start()
    
def pynput_pressed(keys=[]):  # are these keys pressed? dont care about other keys
    for k in keys:
        if k not in pynput_keys_DOWN:
            return False
    return True
    
def pynput_pressed_exclusively(keys=[]):  # are exactly these keys pressed? other keys cant be pressed
    if len(pynput_keys_DOWN) == len(keys):
        return pynput_pressed(keys)
    else:
        #print(pynput_keys_DOWN)
        return False   
## pynput ##


## keyboard ## - keyboard library can be also used (but was removed because contained bugs) - https://github.com/boppreh/keyboard/issues/41
import keyboard

def keyboard_pressed(keys=[]): ## IF PRESSED + DONT CARE ABOUT OTHER KEYS => ITS NOT EXCLUSIVELY PRESSED
    for k in keys:
        if not keyboard.is_pressed(k):
            return False
    return True
    
 ## keyboard ##




def pressed (keys=[]):
    # TODO: convert keys=<string list> to pynput key list
    if type(keys[0]) == str:
        return keyboard_pressed(keys)
    elif type(keys[0]) == pynput.keyboard.Key:
        return pynput_pressed_exclusively(keys)
    else:
        print ('simplehotkeys: ERROR key list "'+keys+'" is not in valid format')
        return False



def _keys_are_same(k1, k2):
    if len(k1) == len(k2):
        for k in k1:
            if not k in k2:
                return False
        return True
    else:
        return False

def _handler_is_running(id):
    global registered_hotkeys
    for r in registered_hotkeys:
        if id in r:
            return True
    return False
    
def _get_handler_id(k):
    global registered_hotkeys
    for i in range(len(registered_hotkeys)):
        if _keys_are_same(registered_hotkeys[i][0],k):
            return registered_hotkeys[i][-1]
    return 0
 
 
## HAMDLERS ##

#TODO: def key_press_time(...): # return values to callback function (for custom press types)
#TODO:    call_function (keydown_or_keyup, number, time_before, duration, [<the_real_order_of_keys>])

def press (keys=[], on_press=lambda: None):
    id = _get_handler_id(keys)
    while True:
        while not pressed(keys):
            time.sleep(IN_WHILE_SLEEP)
            if not _handler_is_running(id): return
            
        on_press()
        
        while pressed(keys):
            time.sleep(IN_WHILE_SLEEP)

def press_longpress_toolongpress (keys=[], on_press=lambda: None, on_longpress=lambda: None, on_toolongpress=lambda: None):
    id = _get_handler_id(keys)
    while True:
        while not pressed(keys):
            time.sleep(IN_WHILE_SLEEP)
            if not _handler_is_running(id): return
            
        t = time.time()
        
        while pressed(keys):
            time.sleep(IN_WHILE_SLEEP)
            
        t = time.time() - t
        
        if t < PRESS_VS_LONGPRESS:
            on_press()
        elif t < LONGPRESS_VS_TOOLONGPRESS:
            on_longpress()
        else:
            on_toolongpress()

def press_doublepress_longpress_toolongpress (keys=[], on_press=lambda: None, on_doublepress=lambda: None, on_longpress=lambda: None, on_toolongpress=lambda: None):
    id = _get_handler_id(keys)
    while True:
        while not pressed(keys):
            time.sleep(IN_WHILE_SLEEP)
            if not _handler_is_running(id): return
            
        t = time.time()
        
        while pressed(keys):
            time.sleep(IN_WHILE_SLEEP)
            
        t = time.time() - t
        
        if t < PRESS_VS_LONGPRESS:
            tt = time.time()
            while not pressed(keys) and time.time()-tt <= DOUBLEPRESS_BETWEEN:
                time.sleep(IN_WHILE_SLEEP)
              
            tt = time.time()-tt 
            if tt < DOUBLEPRESS_BETWEEN:
                on_doublepress()
            else:
                on_press()
                
            while pressed(keys):
                time.sleep(IN_WHILE_SLEEP)
            
        elif t < LONGPRESS_VS_TOOLONGPRESS:
            on_longpress()
        else:
            on_toolongpress()



registered_hotkeys = [] # [keys,on_..., inique_id]
last_thread_number = 0

def catch_hotkey (timeout=10):
    global pynput_keys_DOWN
    t = time.time() + timeout
    keys = []
    while t > time.time():
        if len(keys) < len(pynput_keys_DOWN):
            keys = pynput_keys_DOWN
        elif len(keys) > len(pynput_keys_DOWN):
            return keys
        time.sleep(IN_WHILE_SLEEP)


def add_hotkey (keys=[], _callback_press=None, _callback_longpress=None, _callback_toolongpress=None, _callback_doublepress=None):
    global registered_hotkeys, last_thread_number
    
    for i in range(len(registered_hotkeys)):
        if _keys_are_same(registered_hotkeys[i][0], keys):
            registered_hotkeys.pop(i)
            break
            
    if CALL_THREADED:
        callback_press = lambda: threading.Thread(target=_callback_press).start()  #  if _callback_press is not None else None
        callback_longpress = lambda: threading.Thread(target=_callback_longpress).start()
        callback_toolongpress = lambda: threading.Thread(target=_callback_toolongpress).start()
        callback_doublepress = lambda: threading.Thread(target=_callback_doublepress).start()
    else:
        callback_press = _callback_press
        callback_longpress = _callback_longpress
        callback_toolongpress = _callback_toolongpress
        callback_doublepress = _callback_doublepress


    last_thread_number = last_thread_number+1 
    registered_hotkeys.append([keys, callback_press, callback_longpress, callback_toolongpress, callback_doublepress, last_thread_number])
        

    if _callback_press is None and _callback_doublepress is None and _callback_longpress is None and _callback_toolongpress is None: # remove
        return
    elif _callback_press is not None and (_callback_doublepress is None and _callback_longpress is None and _callback_toolongpress is None): # press
        th = threading.Thread(target=press, args=(keys, callback_press))        
    elif _callback_doublepress is None: # press_longpress_toolongpress
        th = threading.Thread(target=press_longpress_toolongpress, args=(keys, callback_press, callback_longpress, callback_toolongpress))
    else:
        th = threading.Thread(target=press_doublepress_longpress_toolongpress, args=(keys, callback_press, callback_doublepress, callback_longpress, callback_toolongpress)) # press_doublepress_longpress_toolongpress
        
    th.daemon = True
    th.start()


