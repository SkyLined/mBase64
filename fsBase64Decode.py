def fsBase64Decode(sBase64EncodedData, bDebug = False):
  uBitCache = 0;
  uBitsInBitCache = 0;
  sDecodedData = "";
  uBase64Chars = 0;
  uPaddingChars = 0;
  for uIndex in xrange(len(sBase64EncodedData)):
    sBase64Char = sBase64EncodedData[uIndex];
    if sBase64Char in " \t\r\n":
      continue;
    if sBase64Char == "=":
      if uBitsInBitCache == 0:
        print "Base64 data has a superfluous padding character at offset %d: assuming end of base64 data." % uIndex;
        break;
      uBase64Chars += 1;
      uPaddingChars += 1;
      uBitCache <<= 6;
      uBitsInBitCache -= 2;
    elif uPaddingChars == 0:
      uBase64Chars += 1;
      u6Bits = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".find(sBase64Char);
      if u6Bits == -1:
        print "Base64 data has an invalid character at offset %d: assuming end of base64 data." % uIndex;
        break;
      uBitCache = (uBitCache << 6) + u6Bits;
      uBitsInBitCache += 6;
    else:
      print "Base64 data has a non-padding characters following a padding character at offset %d: assuming end of base64 data." % uIndex;
      break;
    if bDebug:
      print "base64: %s (%02X), cache: %s (%d bits)" % (
        repr(sBase64Char), ord(sBase64Char),
        bin(uBitCache)[2:].rjust(uBitsInBitCache, "0"), uBitsInBitCache
      );
    if uBitsInBitCache >= 8:
      uBitsInBitCache = uBitsInBitCache - 8;
      uByte = uBitCache >> uBitsInBitCache;
      sDecodedData += chr(uByte);
      uBitCache -= uByte << uBitsInBitCache;
      if bDebug:
        print "  byte: %s (%02X), cache: %s (%d bits)" % (
          repr(chr(uByte)), uByte,
          bin(uBitCache)[2:].rjust(uBitsInBitCache, "0"), uBitsInBitCache
        );
      if uPaddingChars > 1 and (len(sDecodedData) % 3) + uPaddingChars == 3:
        break;
  uMissingPaddingChars = 0;
  while uBitsInBitCache != 0:
    uMissingPaddingChars += 1;
    uBitCache <<= 6;
    uBitsInBitCache += 6;
    uBitsInBitCache = uBitsInBitCache - 8;
    uByte = uBitCache >> uBitsInBitCache;
    sDecodedData += chr(uByte);
    uBitCache -= uBitCache << uBitsInBitCache;
  if uMissingPaddingChars != 0:
    print "Base64 data is missing %d padding character%s at offset %d" % \
        (uMissingPaddingChars, "s" if uMissingPaddingChars == 1 else "");
  return sDecodedData;

if __name__ == "__main__":
  import sys;
  sInputFilePath = None;
  sOutputFilePath = None;
  bDebug = False;
  for sArgument in sys.argv[1:]:
    if sArgument in ["--help", "-h", "-?", "/help", "/h", "/?"]:
      print "Usage: fsBase64Decode [input file] [output file] [--debug]";
      sys.exit(0);
    elif sArgument == "--debug":
      bDebug = True;
    elif sInputFilePath is None:
      sInputFilePath = sArgument;
    elif sOutputFilePath is None:
      sOutputFilePath = sArgument;
    else:
      print "Superfluous argument: %s" % sArgument;
  
  if sInputFilePath:
    try:
      oInputFile = open(sys.argv[1], "rb");
      sBase64EncodedData = oInputFile.read();
      oInputFile.close();
    except:
      print "Cannot read from input file %s!" % sys.argv[1];
      sys.exit(1);
  else:
    sBase64EncodedData = "";
    print "Please enter base 64 encoded data. Terminate input with an empty line:";
    while 1:
      sInput = raw_input("");
      if sInput == "": break;
      sBase64EncodedData += ("\n" if sBase64EncodedData else "") + sInput;
  
  sDecodedData = fsBase64Decode(sBase64EncodedData, len(sys.argv) > 3 and sys.argv[3] == "--debug");
  
  if sOutputFilePath:
    try:
      oOutputFile = open(sys.argv[2], "wb");
      oOutputFile.write(sDecodedData);
      oOutputFile.close();
    except:
      print "Cannot write to output file %s!" % sys.argv[1];
      sys.exit(1);
  else:
    print "Decoded data:";
    print sDecodedData;
