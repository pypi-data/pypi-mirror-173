import numpy as np
import array
from scipy import signal
from ctypes import Structure, c_float, c_int, c_char_p, POINTER, byref, CDLL
from . import PATH

__all__ = ['rfft', 'interpolation']


class nDsts(Structure):
    _fields_ = [("point", POINTER(c_float)), ("x", c_int), ("y", c_int), ("status", c_int)]


class interpolation():
    """
        interpolation

        Parameters
        ----------
        data_array : array.array
            1D array data.
        slice : int
            Number of slices between two numbers.

        Returns
        -------
        : np.array
    """
    __dll = CDLL(PATH)
    __ret = None

    def __init__(self, data_array: array.array, slice: int = 3) -> None:
        assert len(data_array) >= 8, "Invalid args data_array."
        assert 64 >= slice >= 3, "Invalid args slice."
        self.data_array = data_array
        self.slice = int(slice)

    def __enter__(self) -> np.array:
        Src = np.ctypeslib.as_ctypes(np.array(self.data_array).astype(np.float32))
        self.__dll.interpolation.restype = POINTER(nDsts)
        self.__ret = self.__dll.interpolation(byref(Src), len(Src), self.slice)
        if self.__ret.contents.status != 0:
            raise BaseException(self.__ret.contents.status)
        ret = np.ctypeslib.as_array(self.__ret.contents.point,
                                    shape=(self.__ret.contents.x, self.__ret.contents.y)).copy()
        return ret

    def __exit__(self, exc_type, exc_val, exc_tb):
        if (self.__ret):
            self.__dll.Ipp32fs_free.restype = c_int
            self.__dll.Ipp32fs_free.argtypes = [POINTER(nDsts)]
            self.__dll.Ipp32fs_free(self.__ret)
            self.__ret = None
        if exc_type and issubclass(exc_type, BaseException):
            print(exc_tb.tb_lineno, exc_val.args, exc_tb.tb_frame.f_code.co_filename)


class rfft():
    """
        rfft

        Parameters
        ----------
        data_array : array.array
            1D array data.
        NFFT : int
            FFT window size in [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536].
        window_type: str
            FFT window type in ['hamming', 'hann', 'blackman', 'blackmanharris', 'bartlett'].
        ret_type: str
            Spectral type in ['linear', 'logarithmic']

        Returns
        -------
        : np.array
    """
    __dll = CDLL(PATH)
    __ret = None

    def __init__(
        self,
        data_array: array.array,
        NFFT: int = 128,
        window_type: str = 'hann',
        ret_type: str = 'logarithmic',
    ) -> None:
        assert len(data_array) >= 128, "Invalid args data_array."
        assert NFFT in [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536], "Invalid args NFFT."
        assert window_type in ['hamming', 'hann', 'blackman', 'blackmanharris', 'bartlett'], "Invalid args window_type."
        assert ret_type in ['linear', 'logarithmic']
        self.NFFT = NFFT
        self.window_type = window_type
        self.ret_type = c_char_p(ret_type.encode())
        self.data_array = data_array

    def __enter__(self) -> np.array:
        Src = np.ctypeslib.as_ctypes(np.array(self.data_array).astype(np.float32))
        Win = np.ctypeslib.as_ctypes(
            np.append(signal.get_window(self.window_type, int(self.NFFT - 1)), [0.]).astype(np.float32)
        )
        overlap = 0
        while len(self.data_array) / (self.NFFT - overlap) < 1920 and overlap < (self.NFFT - 1):
            overlap += 1
        self.__dll.normalize_rfft.restype = POINTER(nDsts)
        self.__ret = self.__dll.normalize_rfft(byref(Src), byref(Win), self.NFFT, len(Src), overlap, self.ret_type)
        if self.__ret.contents.status != 0:
            raise BaseException(self.__ret.contents.status)
        ret = np.ctypeslib.as_array(self.__ret.contents.point,
                                    shape=(self.__ret.contents.x, self.__ret.contents.y))[:, :-1].copy()
        return ret

    def __exit__(self, exc_type, exc_val, exc_tb):
        if (self.__ret):
            self.__dll.Ipp32fs_free.restype = c_int
            self.__dll.Ipp32fs_free.argtypes = [POINTER(nDsts)]
            self.__dll.Ipp32fs_free(self.__ret)
            self.__ret = None
        if exc_type and issubclass(exc_type, BaseException):
            print(exc_tb.tb_lineno, exc_val.args, exc_tb.tb_frame.f_code.co_filename)