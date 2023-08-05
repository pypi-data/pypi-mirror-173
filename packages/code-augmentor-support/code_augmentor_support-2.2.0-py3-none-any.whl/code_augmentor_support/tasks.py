import json
import math
import os
import os.path
import sys
import time
import traceback

from types import SimpleNamespace as Object

from .models import ProcessCodeContext, JsonDumpHelper

def jsonParse(str):
    return json.loads(str, object_hook=lambda d: Object(**d))

def compactJsonDump(obj):
    return json.dumps(obj, cls=JsonDumpHelper, separators=(',', ':'))

class ProcessCodeTask:
    def __init__(self):
        self._inputFile = None
        self._outputFile = None
        self._verbose = False
        self._beforeAllFilesHook = None
        self._afterAllFilesHook = None
        self._beforeFileHook = None
        self._afterFileHook = None
        self._allErrors = []
    
    def logVerbose(self, formatStr, *args, **kwargs):
        if self._verbose:
            print("[VERBOSE] " + formatStr.format(*args, **kwargs))
    
    def logInfo(self, formatStr, *args, **kwargs):
        print("[INFO] " + formatStr.format(*args, **kwargs))
    
    def logWarn(self, formatStr, *args, **kwargs):
        print("[WARN] " + formatStr.format(*args, **kwargs))
        
    def execute(self, evalFunction):
        # save properties before use.
        inputFile = self._inputFile
        outputFile = self._outputFile
        beforeFileHook = self._beforeFileHook
        afterFileHook = self._afterFileHook
        
        # validate
        assert inputFile, "inputFile property is not set"
        assert outputFile, "outputFile property is not set"
        assert evalFunction

        allErrors = []
        
        # ensure dir exists for outputFile
        outputDir = os.path.dirname(self._outputFile)
        if outputDir:
            os.makedirs(outputDir, exist_ok=True)
        
        context = ProcessCodeContext()
        context._errorAccumulator = lambda message, cause: allErrors.append(
            ProcessCodeTask._createOrWrapException(context, message, cause))
        
        with open(inputFile, 'r', encoding='utf-8') as codeGenRequest,\
                open(outputFile, 'w', encoding='utf-8') as codeGenResponse:
            # begin serialize by writing header to output    
            codeGenResponse.write("{}\n")
            
            headerSeen = False
            try:
                for line in codeGenRequest:
                    # begin deserialize by reading header from input
                    if not headerSeen:
                        context.header = jsonParse(line)
                        headerSeen = True

                        ProcessCodeTask._prepareContextForHookCall(context, True, None, None, None, -1)
                        ProcessCodeTask._callHook(self._beforeAllFilesHook, context)                    
                        continue

                    fileAugCodes = jsonParse(line)                
                    srcFile = os.path.join(fileAugCodes.dir,
                        fileAugCodes.relativePath)
                    self.logVerbose("Processing {0}", srcFile)
                    startInstant = time.perf_counter();
                    
                    beginErrorCount  = len(allErrors)
                    fileGenCodes = None
                    try:
                        fileGenCodes = ProcessCodeTask._processFileOfAugCodes(context, evalFunction,  
                            beforeFileHook, afterFileHook, srcFile,
                            fileAugCodes, allErrors)
                    except BaseException as e:
                        allErrors.append(ProcessCodeTask._createOrWrapException(context, "processing error", e))
                        
                    if len(allErrors) > beginErrorCount:
                        self.logWarn("{0} error(s) encountered in {1}",
                            len(allErrors) - beginErrorCount, srcFile)
                    
                    # don't waste time serializing if there are errors from previous
                    # iterations or this current one.
                    if not allErrors:
                        codeGenResponse.write(compactJsonDump(fileGenCodes) + "\n")

                    endInstant = time.perf_counter()
                    timeElapsed = math.ceil((endInstant - startInstant) * 1000)
                    self.logInfo("Done processing {0} in {1} ms", srcFile, timeElapsed)
 
                ProcessCodeTask._prepareContextForHookCall(context, False, None, None, None, -1)
                ProcessCodeTask._callHook(self._afterAllFilesHook, context)
            finally:
                self._allErrors = allErrors
        
    @staticmethod
    def _callHook(hook, context):
        if hook:
            return hook(context)

    @staticmethod
    def _prepareContextForHookCall(context,
            clearFileScope, srcFile, fileAugCodes, fileGenCodes, augCodeIndex):
        if clearFileScope:
            context.fileScope.clear()
        context.srcFile = srcFile
        context.fileAugCodes = fileAugCodes
        context.fileGenCodes = fileGenCodes
        context.augCodeIndex = augCodeIndex

    @staticmethod
    def _processFileOfAugCodes(context, evalFunction,
            beforeFileHook, afterFileHook, srcFile, fileAugCodes,
            errors):
        fileGenCodes = None
        try:
            ProcessCodeTask._prepareContextForHookCall(context, True, srcFile,
                fileAugCodes, None, -1);
            fileGenCodes = ProcessCodeTask._callHook(beforeFileHook, context)
        except BaseException as e:
            errors.append(ProcessCodeTask._createOrWrapException(context,
                "beforeFileHook error", e))
            return
        if fileGenCodes is None:
            # fetch arguments and parse any json arguments found
            fileAugCodesList = fileAugCodes.augmentingCodes
            for augCode in fileAugCodesList:
                augCode.processed = False
                augCode.args = []
                for block in augCode.blocks:
                    if block.jsonify:
                        parsedArg = jsonParse(block.content)
                        augCode.args.append(parsedArg)
                    elif block.stringify:
                        augCode.args.append(block.content)
            
            # process aug codes            
            fileGenCodeList = []
            fileGenCodes = Object(
                fileId = 0,  # declare here so as to provide deterministic position during tests
                generatedCodes = fileGenCodeList
            )
            for i in range(len(fileAugCodesList)):
                augCode = fileAugCodesList[i]
                if augCode.processed:
                    continue
 
                functionName = ProcessCodeTask._retrieveFunctionName(augCode)
                ProcessCodeTask._prepareContextForHookCall(context, False, srcFile, fileAugCodes, fileGenCodes, i)
                genCodes = ProcessCodeTask._processAugCode(evalFunction, functionName,
                    augCode, context, errors)
                fileGenCodeList.extend(genCodes)

        try:
            fileGenCodes.fileId = fileAugCodes.fileId
            if hasattr(fileGenCodes, "generatedCodes"):
                ProcessCodeTask._validateGeneratedCodeIds(fileGenCodes.generatedCodes, context, errors)
        except BaseException as e:
            errors.append(ProcessCodeTask._createOrWrapException(context, "validation error", e))
            return

        try:
            ProcessCodeTask._prepareContextForHookCall(context, False, srcFile, fileAugCodes, fileGenCodes, -1)
            ProcessCodeTask._callHook(afterFileHook, context)
        except BaseException as e:
            errors.append(ProcessCodeTask._createOrWrapException(context, "afterFileHook error", e))
            return
        
        return fileGenCodes

    @staticmethod
    def _retrieveFunctionName(augCode):
        functionName = augCode.blocks[0].content.strip()
        return functionName

    @staticmethod
    def _processAugCode(evalFunction, functionName, augCode, context, errors):
        try:
            result = evalFunction(functionName, augCode, context)
            
            if result == None:
                return [ ProcessCodeTask._convertGenCodeItem(None) ]
            converted = []
            if isinstance(result, (list, tuple, set)):
                for item in result:
                    genCode = ProcessCodeTask._convertGenCodeItem(item)
                    converted.append(genCode)
                    # try and mark corresponding aug code as processed.
                    if genCode.id > 0:
                        correspondingAugCodes = [x for x in
                            context.fileAugCodes.augmentingCodes
                                if x.id == genCode.id]
                        if correspondingAugCodes:
                            correspondingAugCodes[0].processed = True
            else:
                genCode = ProcessCodeTask._convertGenCodeItem(result)
                genCode.id = augCode.id
                converted.append(genCode)
            return converted
        except BaseException as e:
            errors.append(ProcessCodeTask._createOrWrapException(context, "", e))
            return []

    @staticmethod
    def _convertGenCodeItem(item):
        if item == None:
            return Object(id = 0)
        elif hasattr(item, 'skipped') or hasattr(item, 'contentParts'):
            if not hasattr(item, 'id'):
                item.id = 0
            return item
        elif hasattr(item, 'content'):
            return Object(id = 0, contentParts = [ item ])
        else:
            content = str(item)
            contentPart = Object(content = content, exactMatch = False)
            return Object(id = 0, contentParts = [ contentPart ])

    @staticmethod
    def _validateGeneratedCodeIds(genCodes, context, errors):
        if not genCodes:
            return
        ids = [x.id for x in genCodes]
        # Interpret use of -1 or negatives as intentional and skip
        # validating negative ids.
        if [x for x in ids if not x]:
            errors.append(ProcessCodeTask._createOrWrapException(context,
                'At least one generated code id was not set. Found: ' + str(ids)))        

    @staticmethod
    def _createOrWrapException(context, message, cause=None):
        wrapperMessage = ''
        srcFileSnippet = None
        try:
            if context.srcFile:
                wrapperMessage = F"in {context.srcFile}"
                if context.fileAugCodes.augmentingCodes and context.augCodeIndex >= 0 \
                        and context.augCodeIndex < len(context.fileAugCodes.augmentingCodes):
                    augCode = context.fileAugCodes.augmentingCodes[context.augCodeIndex]
                    srcFileSnippet = augCode.blocks[0].content
                    wrapperMessage += F" at line {augCode.lineNumber}"
        except:
            pass # ignore
        if wrapperMessage:
            wrapperMessage += ": "
        if wrapperMessage != None:
            wrapperMessage += str(message)
        if srcFileSnippet:
            wrapperMessage += "\n\n" + srcFileSnippet        
        wrapperException = Exception(wrapperMessage)
        wrapperException.__cause__ = cause
        return wrapperException

    def generateStackTrace(self, error):
        if sys.version_info >= (3, 10):
            return "".join(traceback.format_exception(error))
        else:
            return "".join(traceback.format_exception(
                type(error), error, error.__traceback__ ))

    @property
    def inputFile(self):
        return self._inputFile
        
    @inputFile.setter
    def inputFile(self, value):
        self._inputFile = value
        
    @property
    def outputFile(self):
        return self._outputFile
        
    @outputFile.setter
    def outputFile(self, value):
        self._outputFile = value
        
    @property
    def verbose(self):
        return self._verbose
        
    @verbose.setter
    def verbose(self, value):
        self._verbose = value
        
    @property
    def beforeAllFilesHook(self):
        return self._beforeAllFilesHook
        
    @beforeAllFilesHook.setter
    def beforeAllFilesHook(self, value):
        self._beforeAllFilesHook = value
        
    @property
    def afterAllFilesHook(self):
        return self._afterAllFilesHook
        
    @afterAllFilesHook.setter
    def afterAllFilesHook(self, value):
        self._afterAllFilesHook = value
        
    @property
    def beforeFileHook(self):
        return self._beforeFileHook
        
    @beforeFileHook.setter
    def beforeFileHook(self, value):
        self._beforeFileHook = value
        
    @property
    def afterFileHook(self):
        return self._afterFileHook
        
    @afterFileHook.setter
    def afterFileHook(self, value):
        self._afterFileHook = value

    #readonly
    @property
    def allErrors(self):
        return self._allErrors