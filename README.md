# Analyzing the security of a fitbit wearable

In this project we made made static and dynamic analysis of a fitbit wereabale.So to begin we connect to the device through SWD interface(more detail in the report) then we dumped the firmware .We start by the static analysis of the firmware using IDA and identifying important functions as Bluetooth functions. after that we proceed with dynamic analysis using avatar2.

## Static analysis

Under the directory static_analysis_IDAPro:

	* firmware.bin: the firmware that we dumped from the fitbit
	* disas-firmware.s: assembly code of the firmware

## Dynamic analysis

Under the directory dynamic_analysis_Avatar:

	* fitbit.cfg: openocd configration file 
	* avatar-hitbr.py: avatar script (more description in the report)

## Links:  related work  

1. http://homepages.inf.ed.ac.uk/ppatras/pub/imwut18.pdf
2. https://recon.cx/2018/montreal/schedule/system/event_attachments/attachments/000/000/045/original/RECON-MTL-2018-Fitbit_Firmware_Hacking.pdf
3. https://arxiv.org/pdf/1706.09165.pdf
