import os,struct,glob,zlib
MODE = ">"
def dump_pac(f,basename,filename,filesize):
    if not os.path.isdir("output/"+basename+".extracted"):
        os.makedirs("output/"+basename+".extracted")
    else:
        pass
    outFilename = os.path.join("output/"+basename+".extracted",filename)
    if os.path.isfile(outFilename):
            return
    out = open(outFilename,"wb")
    out.write(f.read(filesize))
    out.close()
def iterpac(filename,func):
    global MODE
    basename = os.path.split(filename)[1]
    f = open(filename,"rb")
    zlib.decompress(f.read(),-15)
    if f.read(4) != "FPAC":
        print "\t","Not a valid .pac file"
        return
    DATA_START,TOTAL_SIZE,FILE_COUNT = struct.unpack(">3I",f.read(12))
    if FILE_COUNT == 0:
        return
    UNK01,STRING_SIZE,UNK03,UNK04 = struct.unpack(">4I",f.read(16))
    ENTRY_SIZE = (DATA_START-0x20)/FILE_COUNT
    #STRING_SIZE = (STRING_SIZE + 15) & ~15

    for i in range(0,FILE_COUNT):
        f.seek(0x20+i*(ENTRY_SIZE))
        FILE_NAME,FILE_ID,FILE_OFFSET,FILE_SIZE,UNK = struct.unpack(">"+str(STRING_SIZE)+"s4I",f.read(0x10+STRING_SIZE))
        FILE_NAME = FILE_NAME.split("\x00")[0]
        f.seek(DATA_START+FILE_OFFSET)
        func(f,basename,FILE_NAME,FILE_SIZE)
        
        
#for filename in glob.glob("disc/P4AU/char/char_ka_*.pac"):
        
for filename in glob.glob("X:/Games/BlazBlue Continuum Shift Extend/Data/Char/char_rg*"):
    iterpac(filename,dump_pac)

        
        
