#coding=utf-8
import ctypes as c
import ctypes.wintypes as cw
# sdk api http://www.voidtools.com/zh-cn/support/everything/sdk/everything_getsearch/
"""
| ctypes type  | C type                                 | Python type                |
|--------------+----------------------------------------+----------------------------|
| c_bool       | _Bool                                  | bool (1)                   |
| c_char       | char                                   | 1-character string         |
| c_wchar      | wchar_t                                | 1-character unicode string |
| c_byte       | char                                   | int/long                   |
| c_ubyte      | unsigned char                          | int/long                   |
| c_short      | short                                  | int/long                   |
| c_ushort     | unsigned short                         | int/long                   |
| c_int        | int                                    | int/long                   |
| c_uint       | unsigned int                           | int/long                   |
| c_long       | long                                   | int/long                   |
| c_ulong      | unsigned long                          | int/long                   |
| c_longlong   | __int64 or long long                   | int/long                   |
| c_ulonglong  | unsigned __int64 or unsigned long long | int/long                   |
| c_float      | float                                  | float                      |
| c_double     | double                                 | float                      |
| c_longdouble | long double                            | float                      |
| c_char_p     | char * (NUL terminated)                | string or None             |
| c_wchar_p    | wchar_t * (NUL terminated)             | unicode or None            |
| c_void_p     | void *                                 | int/long or None           |
"""
class ES(object):
    def __init__(self,maxLength=None,config=None):
        self.maxLength = maxLength if maxLength else 260
        self.lib = c.windll.LoadLibrary("Everything.dll") if not config else c.windll.LoadLibrary(config)
    def getNumResults(self):
        self.lib.Everything_GetNumResults.argtypes = []
        self.lib.Everything_GetNumResults.restype = c.c_int
        numResults = self.lib.Everything_GetNumResults()
        return numResults
    def getResultPath(self,index):
        temp = cw.c_uint32(index)#c_ulong (index)
        self.lib.Everything_GetResultPathW.argtypes = [cw.c_uint32]
        self.lib.Everything_GetResultPathW.restype = c.c_wchar_p#c_char_p
        buf = self.lib.Everything_GetResultPathW (temp)
        return buf
    def getResultFileName(self,index):
        temp = cw.c_uint32(index)#c_ulong (index)
        self.lib.Everything_GetResultFileNameW.argtypes = [cw.c_uint32]
        self.lib.Everything_GetResultFileNameW.restype  = c.c_wchar_p
        buf = self.lib.Everything_GetResultFileNameW (temp)
        return buf
    def getResultFullPath(self,index):
        " max string length is self.maxLength"
        index = cw.c_uint32 (index)
        maxCount = cw.c_uint32 (self.maxLength)
        self.lib.Everything_GetResultFullPathNameW.argtypes = [cw.c_uint32,cw.LPWSTR,cw.c_uint32]
        self.lib.Everything_GetResultFullPathNameW.restype = None
        buf = c.c_wchar_p (" " * self.maxLength)
        self.lib.Everything_GetResultFullPathNameW (index,buf,maxCount)
        result = buf.value
        return result
    def getFullName(self,index):
        temp = cw.c_uint32(index)#c_ulong (index)
        buf1 = self.getResultPath (index)
        buf2 = self.getResultFileName (index)
        result = buf1 + "\\" + buf2
        return result
    def _setSearchW(self,string):
        temp = c.c_wchar_p (string)
        self.lib.Everything_SetSearchW.argtypes = [c.c_wchar_p]
        self.lib.Everything_SetSearchW ( temp )
        return None
    def _QueryW(self,flag):
        self.lib.Everything_QueryW.argtypes = [c.c_int]
        self.lib.Everything_QueryW ( c.c_int(flag) ) # IPC enable or disable 
        return None
    def search(self,string):
        #self.lib.Everything_SetSearchW ( temp )
        self._setSearchW (string)
        self._QueryW ( True )
        #print self.getNumResults ()
        #Files = self.lib.Everything_GetTotFileResults()
        Files = self.getNumResults () 
        #print Files
        #print self.lib.Everything_GetResultFileNameW(c_uint (1) )
        resultRange = range(Files)
        #print [self.getResultPath (i) for i in resultRange]
        #print [self.getResultFileName (i) for i in resultRange]
        #print [self.getResultFullPath (i) for i in resultRange]
        #print [self.getFullName (i) for i in resultRange]
        result = [self.getResultFullPath (i) for i in resultRange]
        return result
__all__ = ["ES"]
#del c,cw
