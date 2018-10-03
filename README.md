# macOS installer

Installs various package formats in macOS.

    macOS Mojave note: Automated installs from the Apple Store fail.

## Requirements

* Install as user with admin privileges

  Accept any requests to login or allow installation of system extensions

* Homebrew and Homebrew Cask

  From [here](https://brew.sh/)
     
  ```    
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  ```
    
  Then install [Homebrew Cask](http://caskroom.io/) using Homebrew
    
  ```
  brew tap caskroom/cask
  ```
       
* mas (Mac Appstore command-line interface)

    You will need to log into the Apple Store manually first.

    ```
    brew install mas
    mas list
    ```

* Python3

  Install however you will. For instance:

  `brew install python3`
    
* standard_logger (https://github.com/tflynn/standard_logger)

    ```
    pip3 install git+https://github.com/tflynn/standard_logger.git@master#egg=standard_logger
    ```
    
* run_command (https://github.com/tflynn/run_command)

    ```
    pip3 install git+https://github.com/tflynn/run_command.git@master#egg=run_command
    ``` 

## Installing this package

Get the source code

  * `pip3 install .`
  
Or:

```
pip3 install git+https://github.com/tflynn/macos_installer.git@master#egg=macos_installer
``` 
  
  
## Using this package

```
from macos_installer import installer

installer.PackageManager.all_actions(data)
```

*data* is a JSON structure. See 'package_data.py' for examples.

Example:

```
[
    {"full_name": "Atom Editor 1.31.1", "name": "atom", "package_type": "brewcask", "state" : "present" },
    {"full_name": "lzip 1.2.0", "name": "lzip", "package_type": "brew", "state" : "absent" },
    {"full_name": "Keep It (1.5.2)", "name": "Keep It", "package_type": "mas", "mas_id": "1272768911" , "state" : "absent" }     
]
```

