# IDAPython scripts

These scripts have been tried with IDA 7.7 and Python 3.7.

## `idapythonrc.py`

It needs to be copied into the user directory, which you can get with `get_user_idadir()`, so that it is executed at the end of IDAPython’s initialization.
It imports `color.py`, `nop.py` and `p.py`, defines an `init()` method and registers the `Ctrl+Enter` hotkey to it.

The `init()` method is expected to be called after IDA initial autoanalysis has been finished.
It colors the database, loads capa explorer (running its analysis - needs modifying capa explorer) and reactivate the `IDA View-A` view.


## `color.py` :art:

Provides an `apply()` method to color and mark your database and a `clean()` method to undo it.
The `apply()` method colors `call`, `push` and `pop` instructions (sets background color).
It also adds the prefix `>>` to`call` instructions and the number of argument to its parameters (only available if the function declaration is defined).
This is useful to quickly identify function calls, their parameters and the calling convention.

![colored database](doc/color.png)

`clean()` removes the background color of all the database.
It can be used to remove the colors added by `apply()`, but it doesn't remove the prefixes.


## `nop.py`
Provides a `nop()` method and registers the `Ctrl+N` hotkey to it.
The `nop()` method nops-out the current instruction and advance the cursor to the next instruction.


## `p.py`

Provides functions to print different formated data.


## `decode.py`

Provides functions to decode strings.


## `resolve-apis.py`

It can be use to decode the apis used by a program which resolves API calls at runtime using hashing.

Alternatives to this script:
    - `C:\Program Files\IDA Pro 7.7\idc\renimp.idc`
    - `Universal Unpacker Manual Reconstruct` under plugins


## `define-strings.py`

It defines strings in a range of addresses by looking for the 0x0 byte.


## `call-decoding.py`

It uses Appcall to decode strings calling a decoding routine.
It searches for all calls to the decoding routine.

Check https://hex-rays.com/blog/practical-appcall-examples for more details on Appcall.


## `breakpoint-print.py`

This code can be used in a conditional breakpoint at the of a decoding routine (before restoring ebp) to output the decoded string.


## `RC4.py`

It inspect the whole code looking for instructions like `mov register, offset`.
It tries to decode the bytes which start at the `offset` address using RC4.
If the result is a printable string, it adds a comment in that location with the decoded string and prints a message to the output window with the decoded string and the address.


## `copy-strings.py`

It adds two actions to the strings windows:
- With `Ctrl+C` it copies the strings or list of strings selected.
  The default is to copy the whole row/s.
- With `Ctrl+P` it prints the address and the string in the output window.


## License

The code in this repository is Free Software, published under MIT license (see [LICENSE](LICENSE)).
