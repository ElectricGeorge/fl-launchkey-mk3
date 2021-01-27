import device
import encodings # python standard library required

BUTTON_SHIFT           = 0x6CB0
BUTTON_TRACK_LEFT      = 0x66BF
BUTTON_TRACK_RIGHT     = 0x67BF

BUTTON_UP              = 0x6ABF
BUTTON_DOWN            = 0x6BBF
BUTTON_ARROW           = 0x68B0
BUTTON_STOP_SOLO_MUTE  = 0x69B0

BUTTON_DEVICE_SELECT   = 0x33BF
BUTTON_DEVICE_LOCK     = 0x34BF

BUTTON_CAPTURE_MIDI    = 0x4ABF
BUTTON_QUANITSE        = 0x4BBF
BUTTON_CLICK           = 0x4CBF
BUTTON_UNDO            = 0x4DBF
BUTTON_PLAY            = 0x73BF
BUTTON_STOP            = 0x74BF
BUTTON_RECORD          = 0x75BF
BUTTON_LOOP            = 0x76BF

PAD_SESSION = [
	0x6090,
	0x6190,
	0x6290,
	0x6390,
	0x6490,
	0x6590,
	0x6690,
	0x6790,
	0x7090,
	0x7190,
	0x7290,
	0x7390,
	0x7490,
	0x7590,
	0x7690,
	0x7790
]

PAD_DRUM = [
	0x2899,
	0x2999,
	0x2A99,
	0x2B99,
	0x3099,
	0x3199,
	0x3299,
	0x3399,
	0x2499,
	0x2599,
	0x2699,
	0x2799,
	0x2C99,
	0x2D99,
	0x2E99,
	0x2F99
]

PAD_DEVICE_SELECT = [
	0x4090,
	0x4190,
	0x4290,
	0x4390,
	0x4490,
	0x4590,
	0x4690,
	0x4790,
	0x5090,
	0x5190,
	0x5290,
	0x5390,
	0x5490,
	0x5590,
	0x5690,
	0x5790
]

POT = [
	0x15BF,
	0x16BF,
	0x17BF,
	0x18BF,
	0x19BF,
	0x1ABF,
	0x1BBF,
	0x1CBF
]

FADER = [
	0x35BF,
	0x36BF,
	0x37BF,
	0x38BF,
	0x39BF,
	0x3ABF,
	0x3BBF,
	0x3CBF,
	0x3DBF
]

FADER_BUTTON = [
	0x25BF,
	0x26BF,
	0x27BF,
	0x28BF,
	0x29BF,
	0x2ABF,
	0x2BBF,
	0x2CBF,
	0x2DBF
]

PAD_MODE_NULL           = 0
PAD_MODE_DRUM           = 1
PAD_MODE_SESSION        = 2
PAD_MODE_SCALE          = 3
PAD_MODE_USER_CHORDS    = 4
PAD_MODE_CUSTOM_0       = 5
PAD_MODE_CUSTOM_1       = 6
PAD_MODE_CUSTOM_2       = 7
PAD_MODE_CUSTOM_3       = 8
PAD_MODE_DEVICE_SELECT  = 9
PAD_MODE_NAVIGATION     = 10

POT_MODE_NULL      = 0
POT_MODE_VOLUME    = 1
POT_MODE_DEVICE    = 2
POT_MODE_PAN       = 3
POT_MODE_SEND_A    = 4
POT_MODE_SEND_B    = 5
POT_MODE_CUSTOM_0  = 6
POT_MODE_CUSTOM_1  = 7
POT_MODE_CUSTOM_2  = 8
POT_MODE_CUSTOM_3  = 9

FADER_MODE_NULL      = 0
FADER_MODE_VOLUME    = 1
FADER_MODE_DEVICE    = 2
FADER_MODE_SEND_A    = 4
FADER_MODE_SEND_B    = 5
FADER_MODE_CUSTOM_0  = 6
FADER_MODE_CUSTOM_1  = 7
FADER_MODE_CUSTOM_2  = 8
FADER_MODE_CUSTOM_3  = 9

def sendDeviceInquiry():
	device.midiOutSysex(bytes([0xF0, 0x7E, 0x7F, 0x06, 0x01, 0xF7]))

def decodeInquiryModel(sysex):
	expected = [0xF0, 0x7E, 0x00, 0x06, 0x02, 0x00, 0x20, 0x29, 0, 0, 0x00, 0x00, 0, 0, 0, 0, 0xF7]
	isInquiryResponse = True
	for i in range(0, 8):
		if sysex[i] != expected[i]:
			isInquiryResponse = False
	if isInquiryResponse:
		return sysex[8]
	return False

def decodeInquiryVersion(sysex):
	expected = [0xF0, 0x7E, 0x00, 0x06, 0x02, 0x00, 0x20, 0x29, 0, 0, 0x00, 0x00, 0, 0, 0, 0, 0xF7]
	isInquiryResponse = True
	for i in range(0, 8):
		if sysex[i] != expected[i]:
			isInquiryResponse = False
	if isInquiryResponse:
		return bytes([sysex[12], sysex[13], sysex[14], sysex[15]])
	return False

def decodeInquiryIsBootloader(sysex):
	expected = [0xF0, 0x7E, 0x00, 0x06, 0x02, 0x00, 0x20, 0x29, 0, 0, 0x00, 0x00, 0, 0, 0, 0, 0xF7]
	isInquiryResponse = True
	for i in range(0, 8):
		if sysex[i] != expected[i]:
			isInquiryResponse = False
	if isInquiryResponse:
		if sysex[9] == 0x01:
			return False
		else:
			return True
	return False

def enableDAWMode():
	device.midiOutMsg(0x7F0C9F)

def disableDAWMode():
	device.midiOutMsg(0x000C9F)

def setPadMode(mode):
	device.midiOutMsg(0x0003BF + (mode << 16))

def setPotMode(mode):
	device.midiOutMsg(0x0009BF + (mode << 16))

def setFaderMode(mode):
	device.midiOutMsg(0x000ABF + (mode << 16))

def setStationaryColor(led, color):
	setLEDOff(led)
	device.midiOutMsg((led & 0xFFF0) + 0x0 + (color << 16))

def setFlashingColor(led, color):
	setLEDOff(led)
	device.midiOutMsg((led & 0xFFF0) + 0x1 + (color << 16))

def setPulsingColor(led, color):
	setLEDOff(led)
	device.midiOutMsg((led & 0xFFF0) + 0x2 + (color << 16))

def setStationaryGrayscaleColor(led, color):
	setLEDOff(led)
	device.midiOutMsg((led & 0xFFF0) + 0xF + (color << 16))

def setDrumStationaryColor(led, color):
	setLEDOff(led)
	device.midiOutMsg((led & 0xFFF0) + 0x9 + (color << 16))

def setDrumFlashingColor(led, color):
	setLEDOff(led)
	device.midiOutMsg((led & 0xFFF0) + 0xA + (color << 16))

def setDrumPulsingColor(led, color):
	setLEDOff(led)
	device.midiOutMsg((led & 0xFFF0) + 0xB + (color << 16))

def setLEDOff(led):
	device.midiOutMsg((led & 0xFFF0) + 0x0)
	device.midiOutMsg((led & 0xFFF0) + 0x1)
	device.midiOutMsg((led & 0xFFF0) + 0x2)
	device.midiOutMsg((led & 0xFFF0) + 0xF)
	device.midiOutMsg((led & 0xFFF0) + 0x9)
	device.midiOutMsg((led & 0xFFF0) + 0xA)
	device.midiOutMsg((led & 0xFFF0) + 0xB)

def clearDisplay():
	device.midiOutSysex(bytes([0xF0, 0x00, 0x20, 0x29, 0x02, 0x0F, 0x06, 0xF7]))

def setDisplayLine1(string):
	s = bytes(string, 'iso8859_2')
	length = len(s)
	if len(string) > 16:
		length = 16
	sysex = bytearray(b'\xF0\x00\x20\x29\x02\x0F\x04\x00')
	for i in range(0, length):
		if (s[i] < 0x20) or (s[i] == 0x7F):
			sysex.append(0x20)
		if s[i] > 0x7F:
			sysex.append(0x11)
			sysex.append(s[i] - 0x80)
		else:
			sysex.append(s[i])
	sysex.append(0xF7)
	device.midiOutSysex(bytes(sysex))

def setDisplayLine2(string):
	s = bytes(string, 'iso8859_2')
	length = len(s)
	if len(string) > 16:
		length = 16
	sysex = bytearray(b'\xF0\x00\x20\x29\x02\x0F\x04\x01')
	for i in range(0, length):
		if (s[i] < 0x20) or (s[i] == 0x7F):
			sysex.append(0x20)
		if s[i] > 0x7F:
			sysex.append(0x11)
			sysex.append(s[i] - 0x80)
		else:
			sysex.append(s[i])
	sysex.append(0xF7)
	device.midiOutSysex(bytes(sysex))
