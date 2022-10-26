# SimpleHotkeys
Python library for creating keyboard shortcuts based on [pynput](https://github.com/moses-palmer/pynput) library.

## Usage

### Simple
```python
import simplehotkeys

number = 0
def do_something ():
  global number
  number+=1
  print("key press number", number)

simplehotkeys.add_hotkey([simplehotkeys.pynput.keyboard.Key.ctrl_l, simplehotkeys.pynput.keyboard.Key.alt_l], do_something)
input()
```

Prints message every time you press `left ctrl` and `left alt` key.   
```
key press number 1
key press number 2
key press number 3
key press number 4
key press number 5
key press number 6
key press number 7
...
```
   
   
### More advanced
```python
import simplehotkeys
import time

time.sleep(1)
print ("now press your desired hotkey")
keys = simplehotkeys.catch_hotkey()
print("\t", keys)

simplehotkeys.add_hotkey(keys, 
  lambda: print("single press"), 
  lambda: print("long press"), 
  lambda: print("too long press"), 
  lambda: print("double press")
  )

time.sleep(30)

simplehotkeys.add_hotkey(keys)
input("from now no keypresses are handled")
```
Inputs key combination and for 30 seconds react to its events, then removes all the callbacks.

```
now press your desired hotkey
         [<Key.caps_lock: <20>>]
single press
double press
long press
too long press
from now no keypresses are handled
```

## Instalation
Currently no option to install via `pip`.  
Simply add the `simplehotkeys.py` to your project directory.


## Library methods
   
```python
simplehotkeys.add_hotkey(keys_list, callback_on_press=None, callback_on_longpress=None, callback_on_toolongpress=None, callback_on_doublepress=None)
```
Sets up callbacks for given key combination. Note that there is little reaction delay that depends on what callbacks are set (
when only `callback_on_press` is set, the callback is called on keydown;
when `callback_on_longpress` or `callback_on_toolongpress` is set, it waits for the key release;
when `callback_on_doublepress` is set, waits for next keypress).  
Calling this function for the second time with same key_list will remove the old callbacks.  
To prevent blocking keypress detection, callbacks are always called as threads.

```python
simplehotkeys.catch_hotkey(timeout=10)
```
Waits for key combination being pressed and returns it as list of keys. If no key is pressed within the `timeout` nothing is returned.

## Todos
 - Use key strings list instead of list of pynput key objects.
 - Add hotkey handler that will return keypress duration, keypress number, ... (customizable mode)

