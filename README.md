# FastMB64
A Blender add-on that allows the import of Mario Builder 64 (.mb64) files using Fast64 for quick conversion into Super Mario 64 levels for ROM hacks, Ex Coop Deluxe, or other purposes.

## Notice

The current version has not been tested. I have never made a Super Mario 64 ROM Hack before and I haven't exported levels for SM64Ex Coop-Deluxe either. So, feel free to test and create issues on this Github and I'll get to it eventually, or someone else will.

## Usage

The add-on adds the option to import Mario Builder 64 (.mb64) files of version v1.1. This option is available via File > Import. Note, that this add-on does not support custom logic, non-vanilla behaviors, or textures. You can apply textures to the generated f3d materials. There are empty objects created for non-vanilla objects. Furthermore, some objects use vanilla-equivalent placeholders. The square brackets \[ and \] behind object names refer to imbuements. Items that drop when the object is broken or defeated.

## Installation

Install [Fast64](https://github.com/Fast-64/fast64). Make sure  N (keyboard) > Fast64 > Game is set to "SM64". 
Then download the script and open up Blender. Go to Edit > Preferences > Add-ons and select the arrow at the top right, followed by "Install from Disk" and select the .py file.
It might be needed to close and reopen Blender between updates and installments.

## Todo

* The "ground" plane for chasm boundary is not colored black yet but uses the default ground material.
* Transparent materials are currently fully transparent.
* Water level, changing water level has not been implemented yet.
