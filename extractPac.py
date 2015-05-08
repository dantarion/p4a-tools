import os,struct,glob

for filename in glob.glob("disc/P4AU/char/*.pac"):
    print filename
    basename = os.path.split(filename)[1]
    f = open(filename,"rb")
    
    if f.read(4) != "FPAC":
        print "\t","Not a valid .pac file"
        continue
    DATA_START,TOTAL_SIZE,FILE_COUNT = struct.unpack(">3I",f.read(12))
    if FILE_COUNT == 0:
        continue
    UNK01,STRING_SIZE,UNK03,UNK04 = struct.unpack(">4I",f.read(16))
    print DATA_START,TOTAL_SIZE,FILE_COUNT,UNK01,STRING_SIZE,UNK03,UNK04
    ENTRY_SIZE = (DATA_START-0x20)/FILE_COUNT
    #STRING_SIZE = (STRING_SIZE + 15) & ~15
    print "Entry size",ENTRY_SIZE
    print "String size",STRING_SIZE
    if not os.path.isdir("output/"+basename+".extracted"):
        os.makedirs("output/"+basename+".extracted")
    else:
        continue
    for i in range(0,FILE_COUNT):
        f.seek(0x20+i*(ENTRY_SIZE))
        FILE_NAME,FILE_ID,FILE_OFFSET,FILE_SIZE,UNK = struct.unpack(">"+str(STRING_SIZE)+"s4I",f.read(0x10+STRING_SIZE))
        FILE_NAME = FILE_NAME.split("\x00")[0]
        print FILE_NAME,FILE_ID,FILE_OFFSET,FILE_SIZE,UNK
        f.seek(DATA_START+FILE_OFFSET)
        outFilename = os.path.join("output/"+basename+".extracted",FILE_NAME)
        if os.path.isfile(outFilename):
            continue
        out = open(outFilename,"wb")
        out.write(f.read(FILE_SIZE))
        out.close()
        
        
