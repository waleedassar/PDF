import os,sys,time,struct

#-------------------- Start of func definitions here ----------------
def SplitPDFIntoLines(PDFCon):
    NewList = []
    if PDFCon == "" or len(PDFCon)==0:
        return []
    lenPDFCon = len(PDFCon)
    i = 0
    CurrLine = ""
    while i < lenPDFCon:
        if PDFCon[i]=="\r":
            if i + 1 <= lenPDFCon:
                if PDFCon[i+1]=="\n":
                    i = i + 1
            NewList.append(CurrLine)
            CurrLine = ""
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

# Quick validity check
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
    #Print HexDump Here



#find xref tables, all sections of all updates
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

xref_offsets = []
for iiii in range(0,len(startxrefs)):
    offsetX = int(Lines[startxrefs[iiii]+1])
    if offsetX >= InFLen:
        print "Warning: An xref Section was found to be out of file boundaries"
    xref_offsets.append(offsetX)

print "xref section(s) were found at offset(s) " + str(xref_offsets)

        
#find "Trailer"s



