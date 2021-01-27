# Main FL Studio script for Lanuchkey MK3 DAW mode

# name=Novation Launchkey MK3 (performance)
# receiveFrom=Novation Launchkey MK3 (keyboard)

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

import launchkey_mk3 as lk

global midi_port
global daw_port

global variant

# Excuse how terribly structured this code is.
# I can't be bothered to fix it right now.
# The plan is to fix it before implementing fl studio controls,
# but right now I am working on the abstraction layer.
# See launchkey_mk3.py


def OnInit():
	daw_port = device.getPortNumber()
	midi_port = device.dispatchGetReceiverPortNumber(0)

	# TODO: functionality for communicating with other script
	#device.dispatch(0, 0xF77FF0, bytes([0xF0, 0x7F, 0x00, 0x0F, SET_PORT, midi_port, 0xF7])) # reset extension

	lk.sendDeviceInquiry()
	lk.enableDAWMode()
	print("Script initialized!")

def OnDeInit():
	lk.disableDAWMode()
	print("Script deinitialized!")

def OnMidiIn(eventData):
	if eventData.sysex is None:
		sysexData = ""
	else:
		if lk.decodeInquiryModel(eventData.sysex) != False:
			variant = lk.decodeInquiryModel(eventData.sysex)
			lk.setPadMode(lk.PAD_MODE_CUSTOM_0)
			lk.setPotMode(lk.POT_MODE_CUSTOM_0)
			lk.setFaderMode(lk.FADER_MODE_CUSTOM_0)
			lk.clearDisplay() # clear display
			lk.setDisplayLine1("LK MK3 Script")
			lk.setDisplayLine2("test 123 \xB0\xB0") # test use of latin2 characters
		sysexData = eventData.sysex.hex()
	print("MIDI event received:", hex(eventData.status), hex(eventData.data1), hex(eventData.data2), sysexData)