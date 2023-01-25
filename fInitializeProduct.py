﻿def fInitializeProduct():
  import json, os, sys;

  from foConsoleLoader import foConsoleLoader;
  oConsole = foConsoleLoader();

  from mExitCodes import guExitCodeInternalError, guExitCodeBadDependencyError;
  from mColorsAndChars import \
      COLOR_BUSY, CHAR_BUSY, \
      COLOR_ERROR, CHAR_ERROR, \
      COLOR_INFO, CHAR_INFO, \
      COLOR_LIST, CHAR_LIST, \
      COLOR_OK, CHAR_OK, \
      COLOR_WARNING, CHAR_WARNING, \
      COLOR_HILITE, COLOR_NORMAL;

  import __main__;
  bProductIsAnApplication = hasattr(__main__, "__file__") and os.path.dirname(__main__.__file__) == os.path.dirname(__file__);
  
  bDebugOutput = "@debug-product-initialization" in sys.argv[1:]; # This flag will be remove from the arguments at the end of this code.
  
  def fo0LoadModule(sProductName, sModuleName, bOptional = False):
    if sModuleName in sys.modules:
      return sys.modules[sModuleName];
    if bDebugOutput: oConsole.fStatus(
      COLOR_BUSY, CHAR_BUSY,
      COLOR_NORMAL, " Loading module ",
      COLOR_HILITE, sModuleName,
      COLOR_NORMAL, " for ",
      COLOR_HILITE, sProductName,
      COLOR_NORMAL, "...",
    );
    try:
      oModule = __import__(sModuleName, dict(globals()), {}, [], 0);
    except Exception as oException:
      bModuleNotFound = isinstance(oException, ModuleNotFoundError) and oException.args[0] == "No module named '%s'" % sModuleName;
      if bOptional:
        if bDebugOutput:
          if bModuleNotFound:
            oConsole.fOutput(
              COLOR_WARNING, CHAR_WARNING,
              COLOR_NORMAL, " ", "Optional module" if bOptional else "Module", " ",
              COLOR_HILITE, sModuleName,
              COLOR_NORMAL, " is not available!",
            );
          else:
            oConsole.fOutput(
              COLOR_WARNING, CHAR_WARNING,
              COLOR_NORMAL, " ", "Optional module" if bOptional else "Module", " ",
              COLOR_HILITE, sModuleName,
              COLOR_NORMAL, " can not be loaded!",
            );
            oConsole.fOutput(
              COLOR_NORMAL, "  Exception: ",
              COLOR_HILITE, oException.__class__.__name__,
              COLOR_NORMAL, " - ",
              COLOR_HILITE, str(oException),
              COLOR_NORMAL, ".",
            );
        return None;
      if bProductIsAnApplication:
        if bModuleNotFound:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " ", "Optional module" if bOptional else "Module", " ",
            COLOR_HILITE, sModuleName,
            COLOR_NORMAL, " is not available!",
          );
        else:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " ", "Optional module" if bOptional else "Module", " ",
            COLOR_HILITE, sModuleName,
            COLOR_NORMAL, " can not be loaded!",
          );
          oConsole.fOutput(
            COLOR_NORMAL, "  Exception: ",
            COLOR_HILITE, oException.__class__.__name__,
            COLOR_NORMAL, " - ",
            COLOR_HILITE, str(oException),
            COLOR_NORMAL, ".",
          );
      # Dump exception stack like Python would
      import traceback;
      asExceptionReportLines = traceback.format_exception();
      for sLines in asExceptionReportLines:
        for sLine in sLines.rstrip("\n"):
          oConsole.fOutput(sLine);
      # Terminate with the appropriate exit code from mExitCodes (use standard values if it cannot be loaded).
      sys.exit(guExitCodeBadDependencyError if bModuleNotFound else guExitCodeInternalError);
    if bDebugOutput: oConsole.fOutput(
      COLOR_OK, CHAR_OK,
      COLOR_NORMAL, " Module ",
      COLOR_HILITE, sModuleName,
      COLOR_NORMAL, " loaded at ",
      COLOR_HILITE, os.path.dirname(oModule.__file__),
      COLOR_NORMAL, ".",
    );
    return oModule;
  
  # This is supposed to be the __init__.py file in the module folder.
  sProductFolderPath = os.path.normpath(os.path.dirname(__file__));
  if bProductIsAnApplication:
    # If this is not an application, the modules search path has already been set.
    # But if it is, we want to search the application's parent path for modules in the same
    # parent folder as the application (e.g. development mode) as well as modules in the "modules"
    # sub-folder (i.e. release mode).
    asOriginalSysPath = sys.path[:];
    asModulesPaths = [
      os.path.dirname(sProductFolderPath),
      os.path.join(sProductFolderPath, "modules"),
    ]
    sys.path = asModulesPaths + [sPath for sPath in sys.path if sPath not in asModulesPaths];
    if bDebugOutput:
      oConsole.fOutput(
        COLOR_INFO, CHAR_INFO,
        COLOR_NORMAL, " Module search paths:",
      );
      for sPath in sys.path:
        oConsole.fOutput(
          COLOR_NORMAL, "  ",
          COLOR_LIST, CHAR_LIST,
          COLOR_NORMAL, " ",
          COLOR_INFO, sPath,
          COLOR_NORMAL, ".",
        );
  # Load the dxProductDetails.json file and extract dependencies:
  sProductDetailsFilePath = os.path.join(sProductFolderPath, "dxProductDetails.json");
  if bDebugOutput: oConsole.fStatus(
      COLOR_BUSY, CHAR_BUSY,
      COLOR_NORMAL, " Loading product details file ",
      COLOR_HILITE, sProductDetailsFilePath,
      "...",
    );
  try:
    with open(sProductDetailsFilePath, "rb") as oProductDetailsFile:
      dxProductDetails = json.load(oProductDetailsFile);
  except Exception as oException:
    if bDebugOutput:
      oConsole.fOutput(
        COLOR_ERROR, CHAR_ERROR,
        COLOR_NORMAL, " Product details cannot be loaded from ",
        COLOR_INFO, sProductDetailsFilePath,
        COLOR_NORMAL, "!",
      );
    raise;
  if bDebugOutput:
    oConsole.fOutput(
      COLOR_OK, CHAR_OK,
      COLOR_NORMAL, " Product details for ",
      COLOR_INFO, dxProductDetails["sProductName"],
      COLOR_NORMAL, " by",
      COLOR_INFO, dxProductDetails["sProductAuthor"],
      COLOR_NORMAL, " loaded from ",
      COLOR_INFO, sProductDetailsFilePath,
      COLOR_NORMAL, ".",
    );
  for sModuleName in dxProductDetails.get("a0sDependentOnProductNames", []):
    fo0LoadModule(dxProductDetails["sProductName"], sModuleName, bOptional = False);
  for sModuleName in (
    dxProductDetails.get("a0sDebugAdditionalProductNames", []) +
    dxProductDetails.get("a0sReleaseAdditionalProductNames", [])
  ):
    fo0LoadModule(dxProductDetails["sProductName"], sModuleName, bOptional = True);
  if bDebugOutput:
    oConsole.fOutput(
      COLOR_OK, CHAR_OK,
      COLOR_NORMAL, " Product ",
      COLOR_INFO, dxProductDetails["sProductName"],
      COLOR_NORMAL, " by",
      COLOR_INFO, dxProductDetails["sProductAuthor"],
      COLOR_NORMAL, " initialized.",
    );
  # Restore the original module search path
  if bProductIsAnApplication:
    sys.path = asOriginalSysPath;
  # Remove the debug flag from the arguments if it was provided.
  # We only do this in the main product initializer, otherwise
  # it might be removed by one module initializer before another
  # module is loaded, causing the later module not to display debug
  # output even though it was requested. Once this code is executed
  # in the main product, all modules should have been loaded.
  if bDebugOutput and bProductIsAnApplication:
    sys.argv = sys.argv[:1] + [s for s in sys.argv[1:] if s != "@debug-product-initialization"];
  