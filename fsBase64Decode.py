import re;

def fsShowBits(uValue, uNumberOfBits):
  if uNumberOfBits == 0:
    return "";
  sBits = bin(uValue)[2:].rjust(uNumberOfBits, "0");
  return re.sub(r"(.{8})(?=.)", r"\1 ", sBits); # Add spaces between bytes

gsWhiteSpaceChars = " \t\r\n";
gsDefaultKey = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";

def fsBase64Decode(sBase64EncodedData, s0Key = None, bDebug = False):
  sKey = s0Key if s0Key is not None else gsDefaultKey;
  assert len(sKey) == 65, \
      "Base 64 decoding requires a 65 character key, not %d!" % len(sKey);
  for sWhitespaceChar in gsWhiteSpaceChars:
    assert sWhitespaceChar not in sKey, \
        "Whitespace character %s (%02X) must not be used in the key!" % \
        (repr(sWhitespaceChar), ord(sWhitespaceChar));
  sIndexTable = sKey[:64];
  sPadChar = sKey[64];
  uBitCache = 0;
  uBitsInBitCache = 0;
  sDecodedData = "";
  uBase64Chars = 0;
  uPaddingChars = 0;
  for uIndex in xrange(len(sBase64EncodedData)):
    sBase64Char = sBase64EncodedData[uIndex];
    if sBase64Char in gsWhiteSpaceChars:
      continue;
    if sBase64Char == sPadChar:
      if uBitsInBitCache == 0:
        print "Base64 data has a superfluous padding character at offset %d: assuming end of base64 data." % uIndex;
        break;
      uBase64Chars += 1;
      uPaddingChars += 1;
      u6Bits = 0;
      uBitCache <<= 6;
      uBitsInBitCache -= 2;
      if bDebug:
        print "PAD:    %6s (%02X -> %s)   | cache: %-16s %2d bits" % (
                       repr(sBase64Char),
                            ord(sBase64Char),
                                    fsShowBits(u6Bits, 6),
                                                fsShowBits(uBitCache, uBitsInBitCache),
                                                       uBitsInBitCache
        ),;
        assert uBitCache == 0 or len(bin(uBitCache)[2:]) <= uBitsInBitCache, \
          "Expected %d bits, got %s" % (uBitsInBitCache, bin(uBitCache)[2:]);
    elif uPaddingChars == 0:
      uBase64Chars += 1;
      u6Bits = sIndexTable.find(sBase64Char);
      if u6Bits == -1:
        print "Base64 data has an invalid character at offset %d: assuming end of base64 data." % uIndex;
        break;
      uBitCache = (uBitCache << 6) + u6Bits;
      uBitsInBitCache += 6;
      if bDebug:
        print "DATA:   %6s (%02X -> %s)   | cache: %-16s %2d bits" % (
                       repr(sBase64Char),
                            ord(sBase64Char),
                                    fsShowBits(u6Bits, 6),
                                                fsShowBits(uBitCache, uBitsInBitCache),
                                                       uBitsInBitCache
        ),;
        assert uBitCache == 0 or len(bin(uBitCache)[2:]) <= uBitsInBitCache, \
          "Expected %d bits, got %s" % (uBitsInBitCache, bin(uBitCache)[2:]);
    else:
      print "Base64 data has a non-padding characters following a padding character at offset %d: assuming end of base64 data." % uIndex;
      break;
    if uBitsInBitCache >= 8:
#      print "uBitCache = 0x%X (%d bits)" % (uBitCache, uBitsInBitCache);
      uBitsInBitCache = uBitsInBitCache - 8;
#      print "uByte = 0x%X" % (uBitCache >> uBitsInBitCache);
      uByte = uBitCache >> uBitsInBitCache;
      uBitCache -= uByte << uBitsInBitCache;
      if bDebug:
        print "| OUT: %s (%02X)" % (repr(chr(uByte)), uByte),
      sDecodedData += chr(uByte);
      if uPaddingChars > 1 and (len(sDecodedData) % 3) + uPaddingChars == 3:
        break;
    if bDebug:
      print;
  if bDebug:
    print;
  uMissingPaddingChars = 0;
  while uBitsInBitCache != 0:
    uMissingPaddingChars += 1;
    uBitCache <<= 6;
    uBitsInBitCache += 6;
    if bDebug:
      print "MISSING:       (00 -> 000000)   | cache: %16s (%d bits)" % (
                                                    fsShowBits(uBitCache, uBitsInBitCache),
                                                          uBitsInBitCache
      );
    uBitsInBitCache = uBitsInBitCache - 8;
    uByte = uBitCache >> uBitsInBitCache;
    uBitCache -= uByte << uBitsInBitCache;
    if bDebug:
      print "  byte: %02X (%s), cache: %s (%d bits)" % (
        uByte, bin(uByte)[2:].rjust(8, "0"),
        re.sub(
        r"(.{8})",
        r"\1 ",
        bin(uBitCache)[2:].rjust(uBitsInBitCache, "0")
      ),
      uBitsInBitCache
      );
    sDecodedData += chr(uByte);
  if uMissingPaddingChars != 0:
    print "Base64 data is missing %d padding character%s at offset %d" % \
        (uMissingPaddingChars, "s" if uMissingPaddingChars == 1 else "", uIndex);
  return sDecodedData;

if __name__ == "__main__":
  import sys;
  sInputFilePath = None;
  sOutputFilePath = None;
  bDebug = False;
  s0Key = None;
  for sArgument in sys.argv[1:]:
    if sArgument in ["--help", "-h", "-?", "/help", "/h", "/?"]:
      print "Usage: fsBase64Decode [input file] [output file] [--debug] [--key[=<65 chars>]]";
      sys.exit(0);
    elif sArgument == "--debug":
      bDebug = True;
    elif sArgument == "--key":
      s0Key = "";
    elif sArgument.startswith == "--key=":
      s0Key = sArgument[len("--key="):];
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
  
  if s0Key == "":
    print "Please enter 65 character key (64 data + 1 padding):";
    s0Key = raw_input("");
  assert s0Key is None or len(s0Key) == 65, \
      "Key must be 65 characters, not %d" % len(s0Key);
  sDecodedData = fsBase64Decode(sBase64EncodedData, s0Key = s0Key, bDebug = bDebug);
  
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
