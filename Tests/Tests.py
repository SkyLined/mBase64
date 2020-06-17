from fTestDependencies import fTestDependencies;
fTestDependencies();

try:
  import mDebugOutput;
except:
  mDebugOutput = None;
try:
  try:
    from oConsole import oConsole;
  except:
    import sys, threading;
    oConsoleLock = threading.Lock();
    class oConsole(object):
      @staticmethod
      def fOutput(*txArguments, **dxArguments):
        sOutput = "";
        for x in txArguments:
          if isinstance(x, (str, unicode)):
            sOutput += x;
        sPadding = dxArguments.get("sPadding");
        if sPadding:
          sOutput.ljust(120, sPadding);
        oConsoleLock.acquire();
        print sOutput;
        sys.stdout.flush();
        oConsoleLock.release();
      fPrint = fOutput;
      @staticmethod
      def fStatus(*txArguments, **dxArguments):
        pass;
  
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
  if mDebugOutput:
    mDebugOutput.fTerminateWithException(oException, bShowStacksForAllThread = True);
  raise;
