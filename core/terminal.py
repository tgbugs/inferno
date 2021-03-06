"""
    Blocking, low cpu key listener
"""
import ctypes.wintypes
import ctypes

def GetTerminalEvent():
    #http://techtonik.rainforce.org
    STD_INPUT_HANDLE = -10
    # Constant for infinite timeout in WaitForMultipleObjects()
    INFINITE = -1

    # --- processing input structures -------------------------
    # INPUT_RECORD structure
    #  events:
    EVENTIDS = dict(
      FOCUS_EVENT = 0x0010,
      KEY_EVENT = 0x0001,      # only key event is handled
      MENU_EVENT = 0x0008,
      MOUSE_EVENT = 0x0002,
      WINDOW_BUFFER_SIZE_EVENT = 0x0004,
    )
    EVENTS = dict(zip(EVENTIDS.values(), EVENTIDS.keys()))
    #  records:
    class _uChar(ctypes.Union):
      _fields_ = [('UnicodeChar', ctypes.wintypes.WCHAR),
                  ('AsciiChar', ctypes.wintypes.CHAR)]
    class KEY_EVENT_RECORD(ctypes.Structure):
      _fields_ = [
        ('keyDown', ctypes.wintypes.BOOL),
        ('repeatCount', ctypes.wintypes.WORD),
        ('virtualKeyCode', ctypes.wintypes.WORD),
        ('virtualScanCode', ctypes.wintypes.WORD),
        ('char', _uChar),
        ('controlKeyState', ctypes.wintypes.DWORD)]
    class _Event(ctypes.Union):
      _fields_ = [('keyEvent', KEY_EVENT_RECORD)]
      #  MOUSE_EVENT_RECORD        MouseEvent;
      #  WINDOW_BUFFER_SIZE_RECORD WindowBufferSizeEvent;
      #  MENU_EVENT_RECORD         MenuEvent;
      #  FOCUS_EVENT_RECORD        FocusEvent;
    class INPUT_RECORD(ctypes.Structure):
      _fields_ = [
        ('eventType', ctypes.wintypes.WORD),
        ('event', _Event)]
    # --- /processing input structures ------------------------

    # OpenProcess returns handle that can be used in wait functions
    # params: desiredAccess, inheritHandle, processId

    ch = ctypes.windll.kernel32.GetStdHandle(STD_INPUT_HANDLE)

    handle=ctypes.wintypes.HANDLE(ch)

    ctypes.windll.kernel32.FlushConsoleInputBuffer(ch)
    eventnum = ctypes.wintypes.DWORD()
    eventread = ctypes.wintypes.DWORD()
    inbuf = (INPUT_RECORD * 1)()

    WAIT_OBJECT=0x00000000 #needed to match the return type for ret

    #main loop
    stopflag = 0
    while not stopflag:
        # params: handle, milliseconds
        ret = ctypes.windll.kernel32.WaitForSingleObject(handle, INFINITE)
        #print('im here in the while loop')
        if ret == WAIT_OBJECT:
            # --- processing input ---------------------------
            ctypes.windll.kernel32.GetNumberOfConsoleInputEvents(ch, ctypes.byref(eventnum))
            for i in range(eventnum.value):
                # params: handler, buffer, length, eventsnum
                ctypes.windll.kernel32.ReadConsoleInputW(ch, ctypes.byref(inbuf), 2, ctypes.byref(eventread))
                EVENT_TYPE = EVENTS[inbuf[0].eventType]
                if EVENT_TYPE == 'KEY_EVENT':
                    stopflag = 1
                elif EVENT_TYPE == 'MOUSE_EVENT':
                    stopflag = 1
                elif EVENT_TYPE == 'FOCUS_EVENT':
                    stopflag = 1
                else:
                    print(EVENTS[inbuf[0].eventType])

        else:
            print("Warning: Unknown return value '%s'" % ret)

        ctypes.windll.kernel32.FlushConsoleInputBuffer(ch)
