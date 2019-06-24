# Fitbit analysis:

## Connect to fitbit:

1. run openocd in mode hardware reset:

```bash
$ openocd -f interface/stlink-v2-1.cfg -c "transport select hla_swd" -f target/stm32l1.cfg -c "adapter_khz 240" -c "reset_config none separate"(-c "reset_config srst_only srst_nogate connect_assert_srst")
```
2. connect to openocd server

```bash
$ telnet 127.0.0.1 4444
```

3. dump the frimware:

```bash
> dump_image firmware.bin 0x0 0x40000
```
4. dissasemble firmware :

```bash
$ arm-none-eabi-objdump -D -b binary -marm openocd-firmware.bin -Mforce-thumb > disas-firmware.s
```
5. Debug using gdb server:

```bash
$ gdb-multiarch
gdb$ set arch arm
gdb$ telnet target remote 127.0.0.1:3333
```

## Enabling gdb debugging:

1. patch firmware: this step is important to enable debuggiong otherwise the device will crash when trying to debug it 

```openocd
> init
> reset init
> halt
> flash write_image erase  firmware.bin 0x08000000
> reset run
```
2. avoid this error while debugging : " jtag status contains invalid mode value - communication failure"

 - we shoud mention this option in openocd config file "reset_config none separate" Then the reset is done internally over the SWD channel.

```bash
gdb$ monitor halt
gdb$ monitor poll
gdb$ hb *address for hardware breakpoint
gdb$ continue
``` 
## Next Steps

1. Are you able to debug the device while it is running, and for example talking to
	the phone ?

	**I think best breakpoint we can make , is to find the address of the sync function then we can check it with gdb**

	[openocd setup](https://www.allaboutcircuits.com/technical-articles/getting-started-with-openocd-using-ft2232h-adapter-for-swd-debugging/)

	[useful openocd commands](http://openocd.org/doc/html/General-Commands.html)

	[real time debugging](https://hackaday.com/2012/09/27/beginners-look-at-on-chip-debugging/)
			http://openocd.zylin.com/#/c/2196/5/tcl/target/stm32f3x.cfg
			https://nuttx.org/doku.php?id=wiki:howtos:jtag-debugging

	**check live mode**

2. [Done]: I think now you should look at Avatar, probably trying to set up a simple demo
example from the repository on the STM32 nucleo board, to make sure everything    
works well.
 
3. [Done]: Then, ideally, look at the firmware and identify some function that process
Bluetooth packets (this also need you to disassemble it, which is not always
straightforward). 

	-The library in the firmware is almost identical to an open-source library used for an Arduino BLE
	 Breakout Board.

	-we can also introduce new BLE commands to trigger certain events. One example is the configuration of the debug pins, which we describe in the following section.

	 [Bluetooth functions](https://github.com/adafruit/Adafruit_nRF8001/tree/master/utility)

	 [IDA Pro reverse engineering](https://www.youtube.com/watch?v=V6ZySLopflk)

	 [ARM](https://www.blackhat.com/presentations/bh-europe-04/bh-eu-04-dehaas/bh-eu-04-dehaas.pdf)

	 Results:
	 	 	- 0x080036E0: bluetooth_stack_bsl (BSL)

	 	basically the bluetooth functions located inside App segment

	 		- 0x0800EE62: get_bluetooth_id 
	 		- 0x08012C44: exti_bluetooth_record
	 		- 0x08018868: rf_record_bluetooth
	 		- 0x080214A0: printf_bluetooth_id

	 	**As added value we can explain more the fonctionality of each function using dynamic analysis.**

4. Verify this by putting a break point in the firmware in this
suspected function, then getting the phone to connect and talk to the fitbit.

	Test1: Using gdb I put hb at address "0x0800EE62: get_bluetooth_id " then I pressed "continue" and I tried to connect the app to the fitbit and after while the app found the device and the  break point  reached and gdb stopped at that address.

	steps
```bash
		$arm-none-eabi-gdb
		$gdb source -s gdb-conf
		$gdb monitor halt
		$gdb hb *0x0800EE62
		$gdb continue 
```

5. At this point you can try to setup the device to be used in Avatar, and set
Avatar so that when this breakpoint is reached, the execution is transferred to
the emulator. This would allow to test those pieces of code in the emulator.

	--> Here basically we should try to emulate some bluetooth functions and if it is possible using "angr" 

	-Using Avatar: At this point we try to set up br using avatar then transfer control to qemu but we get some errors(openocd_err.txt)
		1. "undefined debug reason 7 - target needs reset"
			probably OpenOCD doesn't know which state the MCU is in at the moment.So we need a halt there	
		2. "error during read: Connection reset by peer"
		3. "Unable to create rx_queue" in avatar.log
		4. each time the execution stopped before reaching the breakpoint  at a random address 
		5. I get a weird behaviour after setting up the breakpoint and begin execution then if I use 
			* fitbit.wait() : to wait for the breakpoint but the execution stop always at "0x8000082" ? 
			* fitbit.stop(blocking=True): the execution always exit at a random address ?
		6. 





## Fix bugs

### keystone problem

1. install keystone manually so avatar2 will work without errors( https://github.com/keystone-engine/keystone)
2. I wrote "test.py" script for the demo
3. I wrote a final file for openOCD configuration "fitbit.cfg"
4. for avatar script need the firmware.bin
5. after executing test.py I encountred some problems so the solution was to go to "/usr/local/lib/python2.7/dist-packages/avatar2/targets/qemu_target.py" and inside qemu_target.py change the string "configurable" with "virt-3.0"
	--> right here everything work well execept that sometime the device crash because it need to be halted ...so I think you need to search in avatar how we can add this command "monitor halt" when gdb start working (because manually everything works well and the device dosn't crash)



### others bugs 

1. 
Unhandled exception in thread started by <bound method AvatarFastQueueProcessor.__bootstrap of <AvatarFastQueueProcessor(Thread-2, stopped daemon 140533760128768)>>
Traceback (most recent call last):
  File "/usr/lib/python2.7/threading.py", line 774, in __bootstrap
    self.__bootstrap_inner()
  File "/usr/lib/python2.7/threading.py", line 814, in __bootstrap_inner

2. 
avatar.targets.QemuTarget0.RemoteMemoryProtocol.ERROR | Unable to create rx_queue:
Traceback (most recent call last):
  File "/usr/local/lib/python2.7/dist-packages/avatar2/protocols/remote_memory.py", line 134, in connect
    read=True, write=False)
ExistentialError: No queue exists with the specified name
