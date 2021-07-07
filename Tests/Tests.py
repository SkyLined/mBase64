from fTestDependencies import fTestDependencies;
fTestDependencies();
try: # mDebugOutput use is Optional
  import mDebugOutput as m0DebugOutput;
except ModuleNotFoundError as oException:
  if oException.args[0] != "No module named 'mDebugOutput'":
    raise;
  m0DebugOutput = None;

try:
  try:
    from mConsole import oConsole;
  except:
    import sys, threading;
    oConsoleLock = threading.Lock();
    class oConsole(object):
      @staticmethod
      def fOutput(*txArguments, **dxArguments):
        sOutput = "";
        for x in txArguments:
          if isinstance(x, str):
            sOutput += x;
        sPadding = dxArguments.get("sPadding");
        if sPadding:
          sOutput.ljust(120, sPadding);
        oConsoleLock.acquire();
        print(sOutput);
        sys.stdout.flush();
        oConsoleLock.release();
      fPrint = fOutput;
      @staticmethod
      def fStatus(*txArguments, **dxArguments):
        pass;
  
  import base64, random, sys;
  from fsbBase64Decode import fsbBase64Decode;
  
  bDebug = "--debug" in sys.argv;
  
  for sbData in [
    b"Hello, world!",
    b"".join([bytes([u]) for u in range(256)]),
  ]:
    print("sbData: %s" % repr(sbData));
    sbEncodedData = base64.b64encode(sbData);
    print("sbEncodedData: %s" % repr(sbEncodedData));
    sbDecodedData = base64.b64decode(sbEncodedData);
    assert sbDecodedData == sbData, \
        "base64 library error: %s decodes to %s instead of %s" % (repr(sbEncodedData), repr(sbDecodedData), repr(sbData));
    sbDecodedData = fsbBase64Decode(sbEncodedData, bDebug = bDebug);
    print("sbDecodedData: %s" % repr(sbDecodedData));
    assert sbDecodedData == sbData, \
        "%s decodes to %s instead of %s" % (repr(sbEncodedData), repr(sbDecodedData), repr(sbData));
    
    sbNormalKey = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    asbRandomChars = [bytes((u,)) for u in range(0x21, 0x7E)];
    random.shuffle(asbRandomChars);
    sbRandomKey = b"".join(asbRandomChars)[:65];
    print("sbRandomKey: %s" % repr(sbRandomKey));
    sbRandomEncodedData = bytes([
      sbRandomKey[sbNormalKey.find(uCharCode)]
      for uCharCode in sbEncodedData
    ]);
    print("sbRandomEncodedData: %s" % repr(sbRandomEncodedData));
    sbDecodedData = fsbBase64Decode(sbRandomEncodedData, sb0Key = sbRandomKey, bDebug = bDebug);
    print("sbDecodedData: %s" % repr(sbDecodedData));
    assert sbDecodedData == sbData, \
        "%s\ndecodes to \n%s\ninstead of\n%s" % (repr(sbEncodedData), repr(sbDecodedData), repr(sbData));
except Exception as oException:
  if m0DebugOutput:
    m0DebugOutput.fTerminateWithException(oException, bShowStacksForAllThread = True);
  raise;
