# Fitbit analysis:

## Connect to fitbit:

1. run openocd in mode hardware reset:

```bash
$ openocd -f interface/stlink-v2-1.cfg -c "transport select hla_swd" -f target/stm32l1.cfg -c "adapter_khz 240" -c "reset_config srst_only srst_nogate connect_assert_srst"
```
2. connect to openocd server

```bash
$ telnet 127.0.0.1 4444
```

3. dump the frimware:

```bash
dump_image firmware.bin 0x0 0x40000
```
4. dissasemble firmware :

```bash
arm-none-eabi-objdump -D -b binary -marm openocd-firmware.bin -Mforce-thumb > disas-firmware.s
```
5. Debug using gdb server:

```bash
$ gdb-multiarch
gdb$ set arch arm
gdb$ telnet target remote 127.0.0.1:3333
```

 
## Next Steps

1. Are you able to debug the device while it is running, and for example talking to
	the phone ?

2. I think now you should look at Avatar, probably trying to set up a simple demo
example from the repository on the STM32 nucleo board, to make sure everything       -- > I have problem in avatar2
works well.

3. Then, ideally, look at the firmware and identify some function that process
Bluetooth packets (this also need you to disassemble it, which is not always
straightforward). 

	[ARM]: https://www.blackhat.com/presentations/bh-europe-04/bh-eu-04-dehaas/bh-eu-04-dehaas.pdf

4. Verify this by putting a break point in the firmware in this
suspected function, then getting the phone to connect and talk to the fitbit.

5. At this point you can try to setup the device to be used in Avatar, and set
Avatar so that when this breakpoint is reached, the execution is transferred to
the emulator. This would allow to test those pieces of code in the emulator.

