import os,sys,time,struct,string,re

#-------------------- Start of func definitions here ----------------
def GetMyPrintables():
    Printables = string.printable
    NewPrintables = ""
    lenPrintables = len(Printables)
    for i in range(0,lenPrintables):
        if ord(Printables[i]) >= 9 and ord(Printables[i]) <= 13:
            pass
        else:
            NewPrintables += Printables[i]
    return NewPrintables

def GetHexDumpStr(XXX):
    Printables = GetMyPrintables()
    if XXX == "":
        return ""
    lenX = len(XXX)
    if lenX == 0:
        return ""
    NewConn = ""
    i = 0
    while i < lenX:
        XX = XXX[i]
        if Printables.find(XX)==-1:
            NewConn += "."
        else:
            NewConn += XX
        i = i + 1
    return NewConn

def HexDump(Binary,Size=2,Sep=" "):
    if Binary == "":
        return ""
    lenX = len(Binary)
    if lenX == 0:
        return ""
    i = 0
    FinalCon = ""
    RawCon = ""
    HexCon = ""
    StrCon = ""
    c = 0
    d = 0
    while i < lenX:
        X = Binary[i]
        RawCon += X
        XX = struct.unpack("B",X)[0]
        XXX = (hex(XX))[2:]
        if len(XXX)==1:
            XXX = "0" + XXX
        HexCon += XXX
        c = c + 1
        HexCon += Sep
        if c == 8:
            HexCon += Sep
            c = 0
        d = d + 1
        if d == 16 or i == lenX-1:
            StrCon = GetHexDumpStr(RawCon)
            if len(StrCon) < 16:
                ToAdd = 16 - len(StrCon)
                StrCon += (" "*ToAdd)
            RawCon = ""
            if len(HexCon) < 51:
                ToAdd = 51-len(HexCon)
                HexCon += (" "*ToAdd)
            FinalCon += HexCon
            HexCon = ""
            FinalCon += " "
            FinalCon += StrCon
            StrCon = ""
            FinalCon += "\r\n"
            d = 0
        i = i + 1
    return FinalCon

#Removes double spaces and tabs, every tab will be replaced with space 
def RemoveDoubleSpacesAndTabs(StrXX):
    if StrXX == 0 or len(StrXX)==0:
        return ""
    lenXX = len(StrXX)
    iu = 0
    NewStrX = ""
    while iu < lenXX:
        if StrXX[iu] == "\t" or StrXX[iu] == " ":
            while iu < lenXX and (StrXX[iu]=="\t" or StrXX[iu]==" "):
                iu = iu + 1
            NewStrX += " "
            continue
        else:
            NewStrX += StrXX[iu]
        iu = iu + 1
    return NewStrX



#returns 0 on error
def ExtractPrevOffsetFromTrailerDictionary(Trailer):
    if Trailer == "" or len(Trailer)==0:
        return 0
    Segments = Trailer.split("/")
    NumSegments = len(Segments)
    if NumSegments == 0:
        return 0
    for i in range(0,NumSegments):
        SegX = Segments[i].rstrip().lstrip()
        SegXX = SegX[0:4]
        if SegXX.upper()=="PREV":
            SegY = SegX[4:].rstrip().lstrip()
            if SegY != "":
                if SegY.isdigit()==True:
                    return int(SegY)
    return 0

def ExtractInfoDictionaryFromTrailerDictionary(Trailer):
    if Trailer == "" or len(Trailer)==0:
        return ""
    Segments = Trailer.split("/")
    NumSegments = len(Segments)
    if NumSegments == 0:
        return ""
    for i in range(0,NumSegments):
        SegX = Segments[i].rstrip().lstrip()
        SegXX = SegX[0:4]
        if SegXX.upper()=="INFO":
            SegY = SegX[4:].rstrip().lstrip()
            if SegY != "":
                return SegY
    return ""


def ExtractCatalogDictionaryFromTrailerDictionary(Trailer):
    if Trailer == "" or len(Trailer)==0:
        return ""
    Segments = Trailer.split("/")
    NumSegments = len(Segments)
    if NumSegments == 0:
        return ""
    for i in range(0,NumSegments):
        SegX = Segments[i].rstrip().lstrip()
        SegXX = SegX[0:4]
        if SegXX.upper()=="ROOT":
            SegY = SegX[4:].rstrip().lstrip()
            if SegY != "":
                return SegY
    return ""


def ExtractFileIdentifierFromTrailerDictionary(Trailer):
    if Trailer == "" or len(Trailer)==0:
        return []
    Segments = Trailer.split("/")
    NumSegments = len(Segments)
    if NumSegments == 0:
        return []
    for i in range(0,NumSegments):
        SegX = Segments[i].rstrip().lstrip()
        SegXX = SegX[0:2]
        if SegXX.upper()=="ID":
            SegY = SegX[2:]
            IdHashes = re.findall("([0-9a-fA-F]{32})",SegY)
            NumIdHashes = len(IdHashes)
            if NumIdHashes == 2:
                FileId = []
                FileId.append(IdHashes[0])
                FileId.append(IdHashes[1])
                return FileId
    return []
            
def ExtractSizeFromTrailerDictionary(Trailer):
    if Trailer == "" or len(Trailer) == 0:
        return 0
    Segments = Trailer.split("/")
    NumSegments = len(Segments)
    if NumSegments == 0:
        return 0
    for i in range(0,NumSegments):
        SegX = Segments[i].rstrip().lstrip()
        SegXX = SegX[0:4]
        if SegXX.lower()=="size":
            Size = SegX[4:].lstrip().rstrip()
            try:
                Size_i = int(Size)
            except:
                Size_i = 0
            return Size_i
    
#Converts the SubPDF from List into string stripped from leading and
#trailing whitespace characters
def CompactSubPDF(subPDF):
    if subPDF == "" or len(subPDF) == 0:
        return ""
    newSubPDF = ""
    NumLines = len(subPDF)
    for i in range(0,NumLines):
        Line = subPDF[i]
        Line = Line.lstrip().rstrip()
        if Line != "":
            newSubPDF += Line
    return newSubPDF

def SplitPDFIntoLines(PDFCon):
    NewList = []
    if PDFCon == "" or len(PDFCon)==0:
        return []
    lenPDFCon = len(PDFCon)
    i = 0
    CurrLine = ""
    while i < lenPDFCon:
        if i == lenPDFCon - 1:
            if PDFCon[i]!="\r" and PDFCon[i]!="\n":
                CurrLine += PDFCon[i]
            NewList.append(CurrLine)
        if PDFCon[i] == "\r":
            NewList.append(CurrLine)
            CurrLine = ""
            if i + 1 < lenPDFCon and PDFCon[i+1]=="\n":
                i = i + 2
                continue
        elif PDFCon[i]=="\n":
            NewList.append(CurrLine)
            CurrLine = ""
        else:
            CurrLine += PDFCon[i]
        i = i + 1
    return NewList


def IsValidBinaryData(BinaryData):
    if BinaryData == "":
        return False
    lenBin = len(BinaryData)
    if lenBin == 0:
        return False
    for i in range(0,lenBin):
        xBinx = struct.unpack("B", BinaryData[i])[0]
        if xBinx < 128:
            return False
    return True

def SplitPDFLinesIntoSubPDFs(AllPDFLines):
    NewList = []
    if AllPDFLines == "" or len(AllPDFLines)==0:
        return []
    NumLines = len(AllPDFLines)
    if NumLines == 0:
        return []
    FirstFound = False
    i = 0
    while i < NumLines:
        N = []
        if Lines[i].startswith("%PDF-") == True or FirstFound == True:
            N.append(Lines[i])
            c = i + 1
            while c < NumLines:
                if Lines[c] == "%%EOF":
                    N.append(Lines[c])
                    break
                N.append(Lines[c])
                c = c + 1
            if Lines[i].startswith("%PDF-") == True:
                FirstFound = True
            NewList.append(N)
            i = c + 1
    return NewList
            

    
#-------------------- End of func definitions here -----------------

if len(sys.argv)!=2:
    print "Usage: ParsePDF.py input.pdf\r\n"
    sys.exit(-1)

inF = sys.argv[1]

if os.path.exists(inF)==False or \
   os.path.getsize(inF)==0:
    print "Input file does not exist or is empty\r\n"
    sys.exit(-2)

InFLen = os.path.getsize(inF)

#Quick validity check
fIn_t = open(inF,"rb")
fCon_t_h = fIn_t.read(5) #Read Header
fIn_t.close()
if fCon_t_h != "%PDF-":
    if fCon_t_h.upper() == "%PDF-":
        print "Warning: HEADER is " + fCon_t_h + " (It should be all caps \"%PDF-\")"
    else:
        print "Input file is not PDF"
        sys.exit(-3)

fIn = open(inF,"rb")
fCon = fIn.read()
fIn.close()



#Split PDF into lines here
Lines = SplitPDFIntoLines(fCon)

fCon_t_t = Lines[-1]

if fCon_t_t != "%%EOF":
    if fCon_t_t.upper() == "%%EOF":
        print "Warning: Trailer is " + fCon_t_t + " (It should be all caps \"%%EOF\")"
    else:
        if fCon_t_t[-1].isspace():
            fCon_t_t_ = fCon_t_t.rstrip()
            if Con_t_t_ == "%%EOF":
                print "Warning: Trailler is padded with whitespace character(s)"
            elif Con_t_t_.upper()=="%%EOF":
                print "Warning: Trailler is not all in Caps and is padded with whitespace character(s)"             

NumLines = len(Lines)
print Lines[NumLines-1]
Updates = 0
UpdateIndices = []
for ii in range(0,NumLines):
    if Lines[ii]=="%%EOF":
        Updates += 1
        UpdateIndices.append(ii)

print "This PDF has " + str(Updates) + " Update(s)"

Header = Lines[0]
Version = Header[5:]
print "PDF Version: " + Version
Vers = Version.split(".")
MajorVersion = 0
MinorVersion = 0
if len(Vers) > 1:
    MajorVersion = int(Vers[0])
    MinorVersion = int(Vers[1])
if MajorVersion != 1 or Version.find(".") == -1 or MinorVersion > 7:
    print "PDF version is not in the form of 1.N, where N is 0-7"


    
#Check for test Binary Data
BinaryData = ""
LineAfterHeader = Lines[1]
if LineAfterHeader[0]=="%":
    BinaryData = LineAfterHeader[1:]
    retB = IsValidBinaryData(BinaryData)
    if retB == False:
        print "Warning: Binary comment line contains invalid bytes ( each byte must be 128 or greater )"
    print "Test Binary Data ==> " + HexDump(BinaryData)



#find xref table, all sections of all updates
startxrefs = []
for iii in range(0,Updates):
    XXX = UpdateIndices[iii]
    if XXX - 2 > 0:
        STartXREF = Lines[XXX-2]
        if STartXREF == "startxref":
            startxrefs.append(XXX-2)
        else:
            if STartXREF.lower()=="startxref":
                print "Warning: startxref line is not all in small letters"
                startxrefs.append(XXX-2)
            else:
                del UpdateIndices[iii]
    else:
        del UpdateIndices[iii]

Updates_ = len(UpdateIndices)
if Updates_ != Updates:
    print "Warning: number of PDF updates decreased from " + str(Updates) + " to " + str(Updates_)
    Updates = Updates_

xref_offsets = []
for iiii in range(0,len(startxrefs)):
    offsetX = int(Lines[startxrefs[iiii]+1])
    if offsetX >= InFLen:
        print "Warning: An xref Section was found to be out of file boundaries"
    xref_offsets.append(offsetX)

NumXRefSections = len(xref_offsets)
print str(NumXRefSections) + " xref section(s) were found at offset(s) " + str(xref_offsets)


#Slice PDF into subPDFs i.e. main PDF + its update PDFs
subPDFs = SplitPDFLinesIntoSubPDFs(Lines)

TrailerDicts = []

#Process all PDF updates (subPDFs) to get all "Trailer Dictionaries"
for iii in range(0,Updates):
    SubPDF_str = CompactSubPDF(subPDFs[iii])
    re_trailer_lst = re.findall("trailer<<((.*?)+)>>",SubPDF_str,re.I)
    re_trailer_tpl = re_trailer_lst[0]
    if len(re_trailer_tpl) >= 2:
        trailer = re_trailer_tpl[len(re_trailer_tpl)-2]
        print trailer
        TrailerDicts.append(trailer)
    
#Get total number of xref entries in all sections of the XREF table
TotalNumberOfXrefEntries = 0
if len(TrailerDicts) == 1:
    TotalNumberOfXrefEntries = ExtractSizeFromTrailerDictionary(TrailerDicts[0])
elif len(TrailerDicts) > 1:
    TotalNumberOfXrefEntries = ExtractSizeFromTrailerDictionary(TrailerDicts[-1])
           
print "Total number of XREF entries is " + str(TotalNumberOfXrefEntries)

#-------------------------------------
#All Sizes i.e. total number of entries in the whole xref table
Sizes = []
#All File Identifiers
FileIDs = []

#Locations of all "Catalog Dictionaries"
CatalogLocations = [] #38 0 R    ==> str
CatalogEntries = []   #38        ==> int

#Locations of all "Information Dictionaries"
InfoLocations = []
InfoEntries = []

#Previous
#First/Main PDF has no "Prev" in its Trailer Dictionary, so it is always zero
Prevs = []

#True or False
Encrypted = [] 

for iii in range(0,Updates):
    print "--------------------------------------------"
    SIze = ExtractSizeFromTrailerDictionary(TrailerDicts[iii])
    Sizes.append(SIze)
    print "Size: " + str(SIze)
    print "---------------------"
    FileId = ExtractFileIdentifierFromTrailerDictionary(TrailerDicts[iii])
    FileIDs.append(FileId)
    if FileId != []:
        print "MajorFileId: " + FileId[0]
        print "MinorFileId: " + FileId[1] + "\r\n"
    else:
        print "MajorFileId: N/A"
        print "MinorFileId: N/A\r\n"
    print "---------------------"
    CatalogDictLocation = ExtractCatalogDictionaryFromTrailerDictionary(TrailerDicts[iii])
    if CatalogDictLocation != "":
        CatalogLocations.append(CatalogDictLocation)
        CatalogEntries.append(int((CatalogDictLocation.split(" "))[0]))
        print "Catalog Dictionary: " + CatalogDictLocation
    else:
        print "Catalog Dictionary: N/A"
    print "---------------------"
    InfoDictLocation = ExtractInfoDictionaryFromTrailerDictionary(TrailerDicts[iii])
    if InfoDictLocation != "":
        InfoLocations.append(InfoDictLocation)
        InfoEntries.append(int((InfoDictLocation.split(" "))[0]))
        print "Information Dictionary: " + InfoDictLocation
    else:
        print "Information Dictionary: N/A"
    print "---------------------"
    Prev = ExtractPrevOffsetFromTrailerDictionary(TrailerDicts[iii])
    Prevs.append(Prev)
    print "Previous: " + str(Prev)
    print "--------------------------------------------"

#Some sanity checks

#Make sure last PDF Update has the highest "Size"
iii = Updates
if Updates != 0:
    iii = iii - 1
    LastSize = 0
    while iii >= 0:
        currSize = ExtractSizeFromTrailerDictionary(TrailerDicts[iii])
        if currSize < LastSize:
            print "Warning: \"Size\" found in current PDF Update Trailer Dictionary is less than that of the preceding PDF Update"
        iii = iii - 1

#Some sanity checks on File Identifiers
NumFileIDs = len(FileIDs)
OriginalFound = False
for iii in range(0,NumFileIDs):
    currFileId_l = FileIDs[iii]
    if currFileId_l != []:
        Major = currFileId_l[0]
        Minor = currFileId_l[1]
        if Major == Minor:
            OriginalFound = True
        if iii > 0 and FileIDs[iii-1] != []:
            if Major != FileIDs[iii-1][0]:
                print "Warning: Major File Identifier is not constant across all updates"
if OriginalFound == False:
    print "Warning: Original File Identifier was not found"




#[0-9]{10}\s[0-9]{5}\s[f|n]

#All xref sections
xrefs = []

for iii in range(0,NumXRefSections):
    curr_xref_offset = xref_offsets[iii]
    print curr_xref_offset
    XuX = fCon[curr_xref_offset:curr_xref_offset+4]
    print XuX
