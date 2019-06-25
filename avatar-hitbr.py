import IPython 
import telnetlib
import time

from os.path import abspath 
from avatar2 import *



def main():

    # Configure the location of various files
	firmware = abspath('./accelerometer_firmware.bin')

	openocd_config = abspath('./fitbit.cfg')

	qemu_path = abspath("/root/EURECOM/projects/fitbit_project/avatar2/build/arm-softmmu/qemu-system-arm")

    # Initiate the avatar-object
	avatar = Avatar(arch=ARM_CORTEX_M3, output_directory='/tmp/avatar')

	# create openocd object and enabling gdbserver on port 3333
	fitbit = avatar.add_target(OpenOCDTarget,openocd_script=openocd_config,gdb_executable="arm-none-eabi-gdb")	
	# create qemu object to emulate 
	qemu = avatar.add_target(QemuTarget, executable=qemu_path,gdb_executable="arm-none-eabi-gdb", gdb_port=1236)
 	#Define the various memory ranges and store references to them
	rom  = avatar.add_memory_range(0x08000000, 0x40000, file=firmware)
	ram  = avatar.add_memory_range(0x20000000, 0x8000)
	mmio = avatar.add_memory_range(0x40000000, 0x1000000,forwarded=True, forwarded_to=fitbit)

	avatar.init_targets()
	
	
	# set hardware breakpoint at 0x0800EE62(get_bluetooth_id)
	fitbit.set_breakpoint(0x800ee62, hardware=True)

	print ("breakpoint at 0x0800EE62")
	
	print(" after breakpoint $pc is: 0x%x" % fitbit.regs.pc)
	
	fitbit.cont()
	print (fitbit.get_status())

	n = 0
	while True:
		time.sleep(3)
		print (fitbit.get_status())
		fitbit.wait()


		if fitbit.regs.pc == 0x0800EE62:
			n += 1
			print ("hit it %d times" % n)
			print ("we are coming from func at 0x%x" % fitbit.regs.lr)
		if n == 3:
			break
		print("didnt work, retry")
		#fitbit.protocols.monitor.reset() 
		print (fitbit.get_status())
		fitbit.cont()
		


	print(" after wait hb $pc is: 0x%x" % fitbit.regs.pc)
	print (fitbit.get_status())

	#Transfer the state from the physical device to the emulator
	avatar.transfer_state(fitbit, qemu, sync_regs=True,synced_ranges=[ram])

	print (fitbit.get_status())
	print("State transfer finished, emulator $pc is: 0x%x" % qemu.regs.pc)

	qemu.cont()

    # Further analysis could go here:
	#IPython.embed()

    # Let this example run for a bit before shutting down avatar cleanly
	time.sleep(5)
	print("we are all done, shutting done avatar")
	avatar.shutdown()

if __name__ == '__main__':
	main()
