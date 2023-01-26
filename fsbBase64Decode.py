import re;

def fsShowBits(uValue, uNumberOfBits):
  if uNumberOfBits == 0:
    return "";
  sBits = bin(uValue)[2:].rjust(uNumberOfBits, "0");
  return re.sub(r"(.{8})(?=.)", r"\1 ", sBits); # Add spaces between bytes

gauWhitespaceBytes = [0, 9, 0xA, 0xD, 0x20];
gsbDefaultKey = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";

def fsbBase64Decode(sbBase64EncodedData, sb0Key = None, bDebug = False):
  assert isinstance(sbBase64EncodedData, bytes), \
      "sBase64EncodedData muts be eithe a str or bytes, not %s (%s)" % \
      (repr(type(sbBase64EncodedData)), repr(sbBase64EncodedData));
  if sb0Key is None:
    sbKey = gsbDefaultKey;
  else:
    assert len(sb0Key) == 65, \
        "sb0Key must contain 65 characters, not %d (%s)!" % (len(sb0Key), repr(sb0Key));
    sbKey = sb0Key;
  auIndexTable = [uByte for uByte in sbKey[:64]];
  uPadByte = sbKey[64];
  for uWhitespaceByte in gauWhitespaceBytes:
    assert uWhitespaceByte not in auIndexTable, \
        "Whitespace character %s (\\x%02X) must not be used as encoding char in the key!" % \
        (repr(chr(uWhitespaceByte)), ord(uWhitespaceByte));
  assert uWhitespaceByte != uPadByte, \
      "Whitespace character %s (\\x%02X) must not be used as padding char in the key!" % \
      (repr(chr(uWhitespaceByte)), ord(uWhitespaceByte));
  uBitCache = 0;
  uBitsInBitCache = 0;
  sbDecodedData = b"";
  uBase64Chars = 0;
  uPaddingChars = 0;
  for uIndex in range(len(sbBase64EncodedData)):
    uBase64Byte = sbBase64EncodedData[uIndex];
    if uBase64Byte in gauWhitespaceBytes:
      continue;
    if uBase64Byte == uPadByte:
      if uBitsInBitCache == 0:
        print("Base64 data has a superfluous padding character at offset %d: assuming end of base64 data." % uIndex);
        break;
      uBase64Chars += 1;
      uPaddingChars += 1;
      u6Bits = 0;
      uBitCache <<= 6;
      uBitsInBitCache -= 2;
      if bDebug:
        print("PAD:    %6s (%02X -> %s)   | cache: %-16s %2d bits" % (
                       repr(chr(uBase64Byte)),
                            uBase64Byte,
                                    fsShowBits(u6Bits, 6),
                                                fsShowBits(uBitCache, uBitsInBitCache),
                                                       uBitsInBitCache
        ), end=' ');
        assert uBitCache == 0 or len(bin(uBitCache)[2:]) <= uBitsInBitCache, \
          "Expected %d bits, got %s" % (uBitsInBitCache, bin(uBitCache)[2:]);
    elif uPaddingChars == 0:
      uBase64Chars += 1;
      try:
        u6Bits = auIndexTable.index(uBase64Byte);
      except ValueError:
        print(
          "Base64 data has an invalid character %s at offset %d: assuming end of base64 data." % (
            repr(chr(uBase64Byte)) if 0x20 <= uBase64Byte <= 0x7E else "%02X" % uBase64Byte,
            uIndex,
          )
        );
        break;
      uBitCache = (uBitCache << 6) + u6Bits;
      uBitsInBitCache += 6;
      if bDebug:
        print("DATA:   %6s (%02X -> %s)   | cache: %-16s %2d bits" % (
                       repr(chr(uBase64Byte)),
                            uBase64Byte,
                                    fsShowBits(u6Bits, 6),
                                                fsShowBits(uBitCache, uBitsInBitCache),
                                                       uBitsInBitCache
        ), end=' ');
        assert uBitCache == 0 or len(bin(uBitCache)[2:]) <= uBitsInBitCache, \
          "Expected %d bits, got %s" % (uBitsInBitCache, bin(uBitCache)[2:]);
    else:
      print("Base64 data has a non-padding characters following a padding character at offset %d: assuming end of base64 data." % uIndex);
      break;
    if uBitsInBitCache >= 8:
#      print "uBitCache = 0x%X (%d bits)" % (uBitCache, uBitsInBitCache);
      uBitsInBitCache = uBitsInBitCache - 8;
#      print "uByte = 0x%X" % (uBitCache >> uBitsInBitCache);
      uByte = uBitCache >> uBitsInBitCache;
      uBitCache -= uByte << uBitsInBitCache;
      if bDebug:
        print("| OUT: %s (%02X)" % (repr(chr(uByte)), uByte), end=' ')
      sbDecodedData += bytes((uByte,));
      if uPaddingChars > 1 and (len(sDecodedData) % 3) + uPaddingChars == 3:
        break;
    if bDebug:
      print();
  if bDebug:
    print();
  uMissingPaddingChars = 0;
  while uBitsInBitCache != 0:
    uMissingPaddingChars += 1;
    uBitCache <<= 6;
    uBitsInBitCache += 6;
    if bDebug:
      print("MISSING:       (00 -> 000000)   | cache: %16s (%d bits)" % (
                                                    fsShowBits(uBitCache, uBitsInBitCache),
                                                          uBitsInBitCache
      ));
    uBitsInBitCache = uBitsInBitCache - 8;
    uByte = uBitCache >> uBitsInBitCache;
    uBitCache -= uByte << uBitsInBitCache;
    if bDebug:
      print("  byte: %02X (%s), cache: %s (%d bits)" % (
        uByte, bin(uByte)[2:].rjust(8, "0"),
        re.sub(
        r"(.{8})",
        r"\1 ",
        bin(uBitCache)[2:].rjust(uBitsInBitCache, "0")
      ),
      uBitsInBitCache
      ));
    sbDecodedData += bytes((uByte,));
  if uMissingPaddingChars != 0:
    print("Base64 data is missing %d padding character%s at offset %d" % \
        (uMissingPaddingChars, "s" if uMissingPaddingChars == 1 else "", uIndex));
  return sbDecodedData;
