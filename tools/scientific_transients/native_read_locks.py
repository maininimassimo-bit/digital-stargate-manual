"""Windows read-only file handles; no process start or lifecycle authority."""
import ctypes
import hashlib
import os
import re

from tools.pixinsight.local_pilot.broker import require
from tools.scientific_transients.local_registry import safe_path


class _FileInfo(ctypes.Structure):
    _fields_ = [(name, ctypes.c_uint32) for name in (
        'attributes', 'creationLow', 'creationHigh', 'accessLow', 'accessHigh',
        'writeLow', 'writeHigh', 'volume', 'sizeHigh', 'sizeLow', 'links', 'indexHigh', 'indexLow')]


class _WindowsFiles:
    def __init__(self):
        require(os.name == 'nt', 'READ_LOCK_WINDOWS_REQUIRED')
        self.dll = ctypes.WinDLL('kernel32', use_last_error=True)
        signatures = {
            'CreateFileW': ([ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p,
                             ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p], ctypes.c_void_p),
            'GetFileInformationByHandle': ([ctypes.c_void_p, ctypes.POINTER(_FileInfo)], ctypes.c_int),
            'SetFilePointerEx': ([ctypes.c_void_p, ctypes.c_int64, ctypes.POINTER(ctypes.c_int64), ctypes.c_uint32], ctypes.c_int),
            'ReadFile': ([ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32,
                          ctypes.POINTER(ctypes.c_uint32), ctypes.c_void_p], ctypes.c_int),
            'CloseHandle': ([ctypes.c_void_p], ctypes.c_int)}
        for name, (args, result) in signatures.items():
            function = getattr(self.dll, name); function.argtypes = args; function.restype = result

    def open(self, path):
        # GENERIC_READ, FILE_SHARE_READ only, OPEN_EXISTING, sequential scan.
        handle = self.dll.CreateFileW(str(path), 0x80000000, 1, None, 3, 0x08000000, None)
        if handle in {None, ctypes.c_void_p(-1).value}: raise ctypes.WinError(ctypes.get_last_error())
        return handle

    def info(self, handle):
        info = _FileInfo()
        if not self.dll.GetFileInformationByHandle(handle, ctypes.byref(info)):
            raise ctypes.WinError(ctypes.get_last_error())
        require(info.links == 1 and not info.attributes & (0x10 | 0x400), 'READ_LOCK_FILE_TYPE')
        return tuple(getattr(info, name) for name in (
            'volume', 'indexHigh', 'indexLow', 'sizeHigh', 'sizeLow',
            'creationHigh', 'creationLow', 'writeHigh', 'writeLow', 'links'))

    def digest(self, handle, size, guard):
        if not self.dll.SetFilePointerEx(handle, 0, None, 0): raise ctypes.WinError(ctypes.get_last_error())
        digest = hashlib.sha256(); remaining = size
        buffer = ctypes.create_string_buffer(65536); count = ctypes.c_uint32()
        while remaining:
            guard()
            if not self.dll.ReadFile(handle, buffer, min(remaining, len(buffer)), ctypes.byref(count), None):
                raise ctypes.WinError(ctypes.get_last_error())
            require(0 < count.value <= remaining, 'READ_LOCK_SHORT_READ')
            digest.update(buffer.raw[:count.value]); remaining -= count.value
        if not self.dll.ReadFile(handle, buffer, 1, ctypes.byref(count), None):
            raise ctypes.WinError(ctypes.get_last_error())
        require(count.value == 0, 'READ_LOCK_EXCESS_BYTES'); guard()
        return digest.hexdigest()

    def close(self, handle):
        if not self.dll.CloseHandle(handle): raise ctypes.WinError(ctypes.get_last_error())


class NativeReadLocks:
    """Acquire before Popen; caller retains this live object through verified exit.

    No finalizer/context manager releases locks on an unrelated exception. Explicit
    release is a file operation only; it does not prove the native process exited.
    """
    def __init__(self, records, *, guard, progress_guard=None):
        require(type(records) is list and 1 <= len(records) <= 128 and callable(guard), 'READ_LOCK_RECORDS')
        require(progress_guard is None or callable(progress_guard), 'READ_LOCK_PROGRESS_GUARD')
        self._api = _WindowsFiles(); self._held = []; self._released = False
        self._guard = guard
        self._progress_guard = guard if progress_guard is None else progress_guard
        paths = set(); total = 0
        try:
            for row in records:
                require(type(row) is dict and set(row) == {'path','sha256','byteLength'}, 'READ_LOCK_SCHEMA')
                path = safe_path(row['path'])
                require(type(row['path']) is str and row['path'] == path.as_posix() and path not in paths,
                        'READ_LOCK_PATH')
                require(type(row['sha256']) is str and re.fullmatch('[a-f0-9]{64}', row['sha256'])
                        and type(row['byteLength']) is int and 0 <= row['byteLength'] <= 512*1024*1024,
                        'READ_LOCK_PIN')
                paths.add(path); total += row['byteLength']
                require(total <= 544*1024*1024, 'READ_LOCK_AGGREGATE')
                guard(); handle = self._api.open(path)
                # Keep the handle before any further diagnostics can fail.
                self._held.append((handle, path, dict(row), None))
                info = self._api.info(handle)
                self._held[-1] = (handle, path, dict(row), info)
                require((info[3] << 32 | info[4]) == row['byteLength'], 'READ_LOCK_SIZE')
            self.verify()
        except BaseException:
            # Construction failed before this object can be supplied for a start.
            self.release()
            raise

    def verify(self):
        require(not self._released and self._held, 'READ_LOCK_RELEASED')
        for handle, path, row, info in self._held:
            self._guard(); require(safe_path(path) == path, 'READ_LOCK_PATH_CHANGED')
            require(self._api.info(handle) == info, 'READ_LOCK_IDENTITY_CHANGED')
            require(self._api.digest(handle, row['byteLength'], self._progress_guard) == row['sha256'], 'READ_LOCK_HASH')
            require(self._api.info(handle) == info, 'READ_LOCK_IDENTITY_CHANGED')
        self._guard()

    def release(self):
        if self._released: return
        failures = []
        for record in list(self._held):
            try: self._api.close(record[0])
            except Exception as exc: failures.append(exc)
            else: self._held.remove(record)
        if failures: raise failures[0]
        self._released = True
