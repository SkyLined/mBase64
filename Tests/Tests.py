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
  
  import base64, random, sys;
  from fsBase64Decode import fsBase64Decode;
  
  bDebug = "--debug" in sys.argv;
  
  for sData in [
    "Hello, world!",
    "".join([chr(u) for u in range(256)]),
  ]:
    print "sData: %s" % repr(sData);
    sEncodedData = base64.b64encode(sData);
    print "sEncodedData: %s" % repr(sEncodedData);
    assert base64.b64decode(sEncodedData) == sData, \
        "%s decodes to %s instead of %s" % (repr(sEncodedData), repr(sDecodedData), repr(sData));
    sDecodedData = fsBase64Decode(sEncodedData, bDebug = bDebug);
    print "sDecodedData: %s" % repr(sDecodedData);
    assert sDecodedData == sData, \
        "%s decodes to %s instead of %s" % (repr(sEncodedData), repr(sDecodedData), repr(sData));
    
    sNormalKey = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    asRandomChars = [chr(u) for u in xrange(0x21, 0x7E)];
    random.shuffle(asRandomChars);
    sRandomKey = "".join(asRandomChars)[:65];
    print "sRandomKey: %s" % repr(sRandomKey);
    sRandomEncodedData = "".join([
      sRandomKey[sNormalKey.find(sChar)]
      for sChar in sEncodedData
    ]);
    print "sRandomEncodedData: %s" % repr(sRandomEncodedData);
    sDecodedData = fsBase64Decode(sRandomEncodedData, s0Key = sRandomKey, bDebug = bDebug);
    print "sDecodedData: %s" % repr(sDecodedData);
    assert sDecodedData == sData, \
        "%s\ndecodes to \n%s\ninstead of\n%s" % (repr(sEncodedData), repr(sDecodedData), repr(sData));
except Exception as oException:
  if mDebugOutput:
    mDebugOutput.fTerminateWithException(oException, bShowStacksForAllThread = True);
  raise;
