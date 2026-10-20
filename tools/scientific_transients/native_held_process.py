"""Same-session Popen handle identity and observation only. Never opens a PID."""
import ctypes
import os
import subprocess

from tools.pixinsight.local_pilot.broker import require


class _FileTime(ctypes.Structure):
    _fields_ = [('low', ctypes.c_uint32), ('high', ctypes.c_uint32)]


class _WindowsProcessQueries:
    def __init__(self):
        require(os.name == 'nt', 'HELD_PROCESS_WINDOWS_REQUIRED')
        self.dll = ctypes.WinDLL('kernel32', use_last_error=True)
        self.dll.GetProcessId.argtypes = [ctypes.c_void_p]
        self.dll.GetProcessId.restype = ctypes.c_uint32
        self.dll.GetProcessTimes.argtypes = [ctypes.c_void_p] + [ctypes.POINTER(_FileTime)]*4
        self.dll.GetProcessTimes.restype = ctypes.c_int
        self.dll.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        self.dll.WaitForSingleObject.restype = ctypes.c_uint32
        self.dll.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32)]
        self.dll.GetExitCodeProcess.restype = ctypes.c_int

    def identity(self, handle):
        pid = self.dll.GetProcessId(handle)
        if not pid: raise ctypes.WinError(ctypes.get_last_error())
        created, exited, kernel, user = [_FileTime() for _ in range(4)]
        if not self.dll.GetProcessTimes(handle, ctypes.byref(created), ctypes.byref(exited),
                                        ctypes.byref(kernel), ctypes.byref(user)):
            raise ctypes.WinError(ctypes.get_last_error())
        # Exit FILETIME is deliberately ignored; it is undefined for a live process.
        return pid, format(created.high << 32 | created.low, '016x')

    def poll(self, handle):
        status = self.dll.WaitForSingleObject(handle, 0)
        if status == 258: return None
        if status == 0xffffffff: raise ctypes.WinError(ctypes.get_last_error())
        require(status == 0, 'HELD_PROCESS_WAIT_RESULT')
        code = ctypes.c_uint32()
        if not self.dll.GetExitCodeProcess(handle, ctypes.byref(code)):
            raise ctypes.WinError(ctypes.get_last_error())
        return code.value


class HeldNativeProcess:
    """Adopt the just-returned Popen object before capture can fail.

    The caller must already have stored that exact object in its live supervisor.
    This helper cannot prove which command created it or authorize a start/close.
    """
    def __init__(self, process):
        self._process = process
        require(type(process) is subprocess.Popen, 'HELD_PROCESS_POPEN_REQUIRED')
        self._attempted = False; self._uncertain = False
        self._handle = None; self._handle_value = None; self._identity = None
        self._api = None; self._exit = None

    def capture(self):
        require(not self._attempted, 'HELD_PROCESS_CAPTURE_REPLAY')
        self._attempted = True
        try:
            self._handle = self._process._handle
            value = int(self._handle)
            require(type(self._handle) is not bool and 0 < value < (1 << (8*ctypes.sizeof(ctypes.c_void_p)))-1,
                    'HELD_PROCESS_HANDLE')
            self._handle_value = value
            self._api = _WindowsProcessQueries()
            pid, creation = self._api.identity(value)
            require(type(pid) is int and 1 <= pid <= 4294967295
                    and type(self._process.pid) is int and pid == self._process.pid,
                    'HELD_PROCESS_PID')
            require(type(creation) is str and len(creation) == 16
                    and all(c in '0123456789abcdef' for c in creation), 'HELD_PROCESS_CREATION')
            self._identity = (pid, creation)
            self.verify()
            return self.identity()
        except BaseException:
            self._uncertain = True
            raise

    def verify(self):
        require(self._identity is not None and not self._uncertain, 'HELD_PROCESS_IDENTITY_UNCERTAIN')
        try:
            require(self._process._handle is self._handle and int(self._handle) == self._handle_value,
                    'HELD_PROCESS_HANDLE_CHANGED')
            require(self._api.identity(self._handle_value) == self._identity
                    and type(self._process.pid) is int and self._process.pid == self._identity[0],
                    'HELD_PROCESS_IDENTITY_CHANGED')
            require(self._process._handle is self._handle and int(self._handle) == self._handle_value,
                    'HELD_PROCESS_HANDLE_CHANGED')
        except BaseException:
            self._uncertain = True
            raise

    def identity(self):
        self.verify()
        return {'nativeProcessId': str(self._identity[0]), 'processCreationFileTime': self._identity[1]}

    def observe(self):
        """Poll the retained original handle, never a replacement Popen._handle."""
        if self._identity is not None and not self._uncertain:
            try: self.verify()
            except Exception: pass  # Sticky identity failure must not prevent observing actual exit.
        try:
            require(self._handle is not None and self._handle_value is not None
                    and int(self._handle) == self._handle_value, 'HELD_PROCESS_NO_CAPTURED_HANDLE')
            if self._api is None: self._api = _WindowsProcessQueries()
            code = self._api.poll(self._handle_value)
            require(code is None or type(code) is int and -(1 << 31) <= code <= 4294967295,
                    'HELD_PROCESS_EXIT_CODE')
            require(self._exit is None or code == self._exit, 'HELD_PROCESS_EXIT_CHANGED')
            if code is not None: self._exit = code
        except BaseException:
            self._uncertain = True
            raise
        if self._identity is not None and not self._uncertain:
            try: self.verify()
            except Exception: pass
        return {'processObservation': 'HELD_RUNNING' if code is None else 'HELD_EXITED',
                'exitCode': code, 'identityTrusted': self._identity is not None and not self._uncertain,
                'newNativeStartAllowed': False, 'processClosureAuthorized': False}
