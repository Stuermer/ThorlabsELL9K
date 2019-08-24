# ThorlabsELL9K
Command line control for Thorlabs ELL9K linear stage.

See
```
python stage.py -h 
```

for usage.

## Particular use as shutter
Use *ldls.sh* to toggle the shutter for the LDLS light source:
```bash
./ldls.sh
``` 
shows current stage position:

* slot 0 = shutter closed
* slot 1+ = shutter open

use 
```
./ldls.sh 1
```
to open shutter and
```
./ldls.sh 0
```
to close the shutter.
Prints 'OK' if successful. Errormessage otherwise.
