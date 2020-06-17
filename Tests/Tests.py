from fTestDependencies import fTestDependencies;
fTestDependencies();

from mDebugOutput import fEnableDebugOutputForClass, fEnableDebugOutputForModule, fTerminateWithException;
try:
  import base64;
  from fsBase64Decode import fsBase64Decode;
  
  for sData in [
    "Hello, world!",
    "".join([chr(u) for u in range(256)]),
  ]:
    sEncodedData = base64.b64encode(sData);
    assert base64.b64decode(sEncodedData) == sData, \
        "%s decodes to %s instead of %s" % (repr(sEncodedData), repr(sDecodedData), repr(sData));
    sDecodedData = fsBase64Decode(sEncodedData, True);
    assert sDecodedData == sData, \
        "%s decodes to %s instead of %s" % (repr(sEncodedData), repr(sDecodedData), repr(sData));
except Exception as oException:
  fTerminateWithException(oException);