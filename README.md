# Shiny Hunter

## How to use

### Running a script

Run `run.bat` or run the `shinyhunt.py` python script directly!

The script takes in 1-2 arguments, the first being the filename of the macro you want to run, and the second being `loop` if you want the macro to loop over and over again instead of ending after a single run.

For example, running my gastly hunter macro would look like this:

`./run.bat gastly_hunting.macro loop`

To exit a macro at any time, just hold the `esc` key!

### Creating a macro

#### Conventions
The script will run one line at a time, executing each macro command one at a time. 

Empty lines will be ignored, and any line prefaced with `#` will be ignored and treated as a comment.

Lines prefaced with `>` are conditionals, and will be ignored unless a conditional command successed prior, such as `debug`

#### Commands

| Command | Convention | Description |
| ------- | ---------- | ----------- |
| exit | `exit` | Interrupts and quits the program execution |
| wait | `wait <int>` | Pauses the program for `<int>` milliseconds
| standby | `standby <x> <y> <w> <h>` | Pauses the program and checks if the rectangle on your screen defined by `<x> <y> <w> <h>` coordinates is the same color as the 🟩 or 🟥 emoji on discord. If it is 🟩, it will continue and run conditional commands. If it is 🟥, the macro will quit.
| copy | `copy <x> <y> <w> <h>` | Copies the rectangle image on your screen defined by `<x> <y> <w> <h>` to your clipboard |
| down | `down <left/right>` | Sets the mouse button defined by `left` or `right` to be pressing down |
| up | `up <left/right>` | Sets the mouse button defined by `left` or `right` to be released  |
| move | `move <x> <y>` | moves the mouse position to the position defined by `<x> <y>` |
| debug | `debug <x> <y> <w> <h>` | if the rectangle on your screen defined by `<x> <y> <w> <h>` coordinates is the same color as the 🟦 or 🟥 emoji on discord. If it is 🟦, then it will run conditional commands that follow. If it is 🟥, then it will exit the program. Otherwise, nothing will happen and macro execution will continue.
| wild | `wild <x> <y> <w> <h>` | if the rectangle on your screen defined by `<x> <y> <w> <h>` coordinates is the same color as the 🟪 or 🟥 emoji on discord. If it is 🟪, then it will run conditional commands that follow. If it is 🟥, then it will exit the program. Otherwise, nothing will happen and macro execution will continue.
| hotkey | `hotkey <key1> <key2>` | presses the hotkey command series defined by `<key1> <key2>`, e.g. `ctrl v` |
| print | `print <message>` | prints out `<message>` to console. Note that `<message>` must be wrapped in quotes.
| type | `type <message>` | types out `<message>` with your keyboard. Note that `<message>` must be wrapped in quotes.
| save | `save <x> <y> <w> <h>` | saves the image rectangle defined by `<x> <y> <w> <h>` to an `images/` folder located at the same directory where the program was run in.
| press | `press <key> <int>` | presses the key defined by `<key>` for `<int>` milliseconds
| click | `click <left/right> <x> <y>` | clicks the mouse button defined by `left` or `right` at the location defined by `<x> <y>`
| check | `check <pokemon> <x> <y> <w> <h>` | checks if a shiny pokemon defined by `<pokemon>` is in the image rectangle defined by `<x> <y> <w> <h>` |

Note that the `check` command only supports looking at a 3x horde of gastly at the moment.