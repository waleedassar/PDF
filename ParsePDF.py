import os,sys,time,struct


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





if len(sys.argv)!=2:
    print "Usage: ParsePDF.py input.pdf\r\n"
    sys.exit(-1)

inF = sys.argv[1]

if os.path.exists(inF)==False or \
   os.path.getsize(inF)==0:
    print "Input file does not exist or is empty\r\n"
    sys.exit(-2)

InFLen = os.path.getsize(inF)

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
#print len(Lines)

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
                

Header = Lines[0]
Version = Header[5:]
print "PDF Version: " + Version
if Version[0]!="1" or Version.find(".")==-1:
    print "PDF version is not in the form of 1.N"




    
#Check for test Binary Data
BinaryData = ""
LineAfterHeader = Lines[1]
if LineAfterHeader[0]=="%":
    BinaryData = LineAfterHeader[1:]
    try:
        #Print HexDump Here
    except:
        print "hexdump is needed to print hexdump"







