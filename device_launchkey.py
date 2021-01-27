# Main FL Studio script for Lanuchkey MK3 standalone mode

# name=Novation Launchkey MK3 (keyboard)
# receiveFrom=Novation Launchkey MK3 (performance)

import playlist
import channels
import mixer
import patterns
import arrangement
import ui
import transport
import device
import general
import launchMapPages
import midi

import launchkey_mk3

global midi_port
global daw_port

global variant

# this script is not very important yet. see device_launchkey_daw.py

def OnInit():
	midi_port = device.getPortNumber()
	daw_port = device.dispatchGetReceiverPortNumber(0)

	print("Script initialized!")

def OnDeInit():
	print("Script deinitialized!")

def OnMidiIn(eventData):
	if eventData.sysex is None:
		sysexData = ""
	else:
		sysexData = eventData.sysex.hex()
	print("MIDI event received:", hex(eventData.status), hex(eventData.data1), hex(eventData.data2), sysexData)