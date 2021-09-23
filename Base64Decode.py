import sys;

from fInitializeProduct import fInitializeProduct;
fInitializeProduct();

from fsbBase64Decode import fsbBase64Decode;
from mExitCodes import *;

if __name__ == "__main__":
  import sys;
  sInputFilePath = None;
  sOutputFilePath = None;
  bDebug = False;
  sb0Key = None;
  for sArgument in sys.argv[1:]:
    if sArgument in ["--help", "-h", "-?", "/help", "/h", "/?"]:
      print("Usage: fsBase64Decode [input file] [output file] [--debug] [--key[=<65 chars>]]");
      sys.exit(guExitCodeSuccess);
    elif sArgument == "--debug":
      bDebug = True;
    elif sArgument == "--key":
      sb0Key = b"";
    elif sArgument.startswith == "--key=":
      sb0Key = bytes(sArgument[len("--key="):], "utf-8");
    elif sInputFilePath is None:
      sInputFilePath = sArgument;
    elif sOutputFilePath is None:
      sOutputFilePath = sArgument;
    else:
      print("Superfluous argument: %s" % sArgument);
  
  if sInputFilePath:
    try:
      oInputFile = open(sys.argv[1], "rb");
      sbBase64EncodedData = oInputFile.read();
      oInputFile.close();
    except:
      print("Cannot read from input file %s!" % sys.argv[1]);
      sys.exit(guExitCodeCannotReadFromFileSystem);
  else:
    sbBase64EncodedData = b"";
    print("Please enter base 64 encoded data. Terminate input with an empty line:");
    while 1:
      sInput = input("");
      if sInput == "": break;
      sbBase64EncodedData += ("\n" if sbBase64EncodedData else "") + bytes(sInput, "utf-8");
  
  if sb0Key == b"":
    print("Please enter 65 character key (64 data + 1 padding):");
    sb0Key = bytes(input(""), "utf-8");
  assert sb0Key is None or len(sb0Key) == 65, \
      "Key must be 65 characters, not %d" % len(s0Key);
  sbDecodedData = fsBase64Decode(sbBase64EncodedData, sb0Key = sb0Key, bDebug = bDebug);
  
  if sOutputFilePath:
    try:
      oOutputFile = open(sys.argv[2], "wb");
      oOutputFile.write(sbDecodedData);
      oOutputFile.close();
    except:
      print("Cannot write to output file %s!" % sys.argv[1]);
      sys.exit(guExitCodeCannotWriteToFileSystem);
  else:
    print("Decoded data:");
    print(sbDecodedData);

