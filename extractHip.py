import os,struct,glob,gzip,zlib, StringIO
from PIL import Image
for filename in glob.glob("output/*img.pac.extracted/*.hip"):
    outfile = "img/"+os.path.split(filename)[1].replace(".hip",".png")
    if os.path.isfile(outfile) or "dmy_camera.hip" in filename:
        continue
    print filename
    f = open(filename,"rb")
    if f.read(4) != "HIP\x00":
        continue
    DATA = struct.unpack(">3I4I4I4I",f.read(0x3C))
    #print DATA
    #print hex(DATA[6]&0xFFFF)
    #DATA2 = TOTAL_SIZE,PALLETE SIZE
    tmp = f.tell()
    f.seek(1,2)
    end = f.tell()
    f.seek(tmp)
    if DATA[2] == 0:
        f.seek(0x50)
        f.read(4)
        SEGS_UNK,SEGS_ENTRY_COUNT,SEGS_ORIGINAL_LENGTH,SEGS_LENGTH = struct.unpack(">2H2I",f.read(12))
        tmp = f.tell()
        dataref = 0x80
        RAW_DATA = ""
        for i in range(0,SEGS_ENTRY_COUNT):
            f.seek(tmp+i*0x8)
            entry_data = struct.unpack(">2HI",f.read(8))
            f.seek(0x50+(entry_data[2] & ~1))
            data = f.read(entry_data[0])

            data = zlib.decompress(data,-15)
  
            RAW_DATA += data
        f = StringIO.StringIO(RAW_DATA)
        #Get pallete
        tmp = os.path.split(filename.replace("_img","_pal"))
  
        
        palfile = os.path.join(tmp[0],tmp[1][0:2]+"00_00.hpl")
        if not os.path.isfile(palfile):
           continue
        pal = open(palfile, "rb")
        pal.seek(0x20)
        PALLETE = []
        for i in range(0, 256):
            tmp = struct.unpack("4B",pal.read(4))
            PALLETE.extend((tmp[1],tmp[2],tmp[3]))
        
        img = Image.fromstring("P",(DATA[3],DATA[4]),RAW_DATA)
        img.putpalette(PALLETE)
        transparencycolor = (PALLETE[0],PALLETE[1],PALLETE[2])
        img = img.convert("RGB")
        img = img.crop((0,0,DATA[7],DATA[8]))
    else:
        PALLETE = []
        for i in range(0, 256):
            PALLETE.append(struct.unpack("4B",f.read(4)))
        
        RAW_DATA = ""
        while f.tell() < end:
            color = PALLETE[struct.unpack("B",f.read(1))[0]]
            counter = ord(f.read(1))
            #print color,counter
            while counter > 0:
                counter = counter -1
                RAW_DATA += struct.pack("4B",*color)
        print len(RAW_DATA)
        img = Image.fromstring("RGBA",(DATA[7],DATA[8]),RAW_DATA,"raw","ARGB")
    
    img.save(outfile,"png",transparency=(transparencycolor))
    
