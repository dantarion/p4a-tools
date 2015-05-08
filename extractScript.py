import os,struct,glob,json
from PIL import Image
COMMAND_NAMES = {}
COMMAND_NAMES[0x0000] = "EventHead"
COMMAND_NAMES[0x0001] = "EventEnd"
COMMAND_NAMES[0x0002] = "SetSprite"
COMMAND_NAMES[0x0003] = "LoopWait"
COMMAND_NAMES[0x0006] = "Label"
COMMAND_NAMES[0x0007] = "Goto"
COMMAND_NAMES[0x0313] = "AttackLevel"
COMMAND_NAMES[0x0314] = "Damage"
COMMAND_NAMES[0x720] = "WhiffCancel"
COMMAND_NAMES[0x721] = "OnHitCancel"
COMMAND_NAMES[0x729] = "HitCancel"
COMMAND_NAMES[0x72D] = "HitCancel+"
for filename in glob.glob("char_*_scr.pac.extracted/*.bbsbin"):
    print filename
    f = open(filename,"rb")
    COUNT = struct.unpack(">I",f.read(4))[0]
    for i in range(0,COUNT):
        f.seek(4+i*36)
        ScriptName,ScriptOffset = struct.unpack(">32sI",f.read(36))
        ScriptName = ScriptName.split("\x00")[0]
        ScriptOffset = COUNT*36+ScriptOffset+4
        if i < COUNT-1:
            f.seek(32,1)
            ScriptEndOffset = COUNT*36+struct.unpack(">I",f.read(4))[0]+4
        else:
            f.seek(0,2)
            ScriptEndOffset = f.tell()
            
        print i,ScriptName,ScriptOffset,ScriptEndOffset
        
        f.seek(ScriptOffset)
        commands = []
        
        while True:
            cmd = struct.unpack(">I",f.read(4))[0]
            params = []
            #
            # 0x0000
            #
            if cmd == 0x0000:
                params.append(f.read(0x20).split("\x00")[0])
                
            elif cmd == 0x0002:
                params.append(f.read(0x20).split("\x00")[0])
                params.append(struct.unpack(">I",f.read(4))[0])
            
            elif cmd == 0x0003:
                pass
            elif cmd == 0x0004:
                params = struct.unpack(">II",f.read(8))
            elif cmd == 0x0005:
                pass
            elif cmd == 0x0006:
                params.append(struct.unpack(">I",f.read(4))[0])
            elif cmd == 0x0007:
                params.append(struct.unpack(">I",f.read(4))[0])
            elif cmd == 0x000A:
                params.append(f.read(0x20).split("\x00")[0])
            elif cmd == 0x000F:
                params.append(struct.unpack(">I",f.read(4))[0])
            elif cmd == 0x0010:
                pass
            elif cmd == 0x12:
                params = struct.unpack(">3I",f.read(3*4))
            elif cmd == 0x0015:
                params.append(f.read(0x20).split("\x00")[0])
            elif cmd == 0x001D:
                params = struct.unpack(">II",f.read(8))    
            elif cmd == 0x27:
                params = struct.unpack(">3I",f.read(3*4))
            elif cmd == 0x28:
                params = struct.unpack(">5I",f.read(4*5))
            elif cmd == 0x29:
                params = struct.unpack(">4I",f.read(4*4))
            elif cmd == 0x2A:
                params.append(f.read(0x10).split("\x00")[0])
            elif cmd == 0x32:
                params = struct.unpack(">III",f.read(12))
            elif cmd == 0x36:
                params = struct.unpack(">II",f.read(8))
            elif cmd in (0x37,0x38,0x39):
                pass
            elif cmd == 0x64:
                params.append(f.read(0x10).split("\x00")[0])
            elif cmd in (0x67,0x74,0x76,0x79,0x7A,0x7B,0x7C,0x7F):
                params = struct.unpack(">i",f.read(4))
            elif cmd in (0x78,0x7A):
                params = struct.unpack(">I",f.read(4))
            elif cmd == 0x8A:
                params = struct.unpack(">I",f.read(4))
            elif cmd == 0x8C:
                params = struct.unpack(">II",f.read(8))
            elif cmd == 0x8D:
                pass
            elif cmd in (0x8E,0x94,0x96,0x9A,0x9F,0xBB):
                params = struct.unpack(">I",f.read(4))
            elif cmd == 0xFE:
                pass
            #
            # 0x0100
            #
            elif cmd in (0x122,0x12a,0x172,0x175,0x1f1,0x1f2,0x1EF):
                params.append(struct.unpack(">i",f.read(4))[0])
            elif cmd in (0x100,0x104,0x109,0x1f7):
                pass
            elif cmd in (0x0103,):
                params = struct.unpack(">ii",f.read(8))
            elif cmd in (0x18d,0x0191,):
                params = struct.unpack(">ii",f.read(8))
            elif cmd in (0x1E8,0x1E9,0x1EA,0x1EC):
                params.append(f.read(0x20).split("\x00")[0])
                params.append(struct.unpack(">I",f.read(4))[0])
            elif cmd in (0x1EB,):
                params.append(f.read(0x40).split("\x00")[0])
            #
            # 0x0200
            #
            elif cmd in (0x2A6,):
                params.append(f.read(0x20).split("\x00")[0])
            elif cmd in (0x2A7,0x2AA):
                params.append(f.read(0x10).split("\x00")[0])

            elif cmd in (0x2A9,):
                params.append(f.read(0x20).split("\x00")[0])
            elif cmd in (0x2AD,):
                params.append(f.read(0x10).split("\x00")[0])
                params.append(struct.unpack(">I",f.read(4))[0])
                params.append(f.read(0x10).split("\x00")[0])
                params.append(struct.unpack(">I",f.read(4))[0])
                params.append(f.read(0x10).split("\x00")[0])
                params.append(struct.unpack(">I",f.read(4))[0])
                params.append(f.read(0x10).split("\x00")[0])
                params.append(struct.unpack(">I",f.read(4))[0])
            elif cmd in (0x2AF,):
                params.append(struct.unpack(">I",f.read(4))[0])
            elif cmd in (0x02e3,0x2E4,0x02e7,0x02e8,):
                params = struct.unpack(">iii",f.read(12))
            elif cmd in (0x02ea,):
                params = struct.unpack(">ii",f.read(8))
            
            #
            # 0x0300
            #
            elif cmd in (0x313,0x314,0x356,0x362,0x3E6,0x36e,0x37a):
                params.append(struct.unpack(">i",f.read(4))[0])
            #
            # 0x0400
            #
            elif cmd in (0x422,0x424,0x42E,0x43A,0x452,0x476,0x46A,0x4D4,0x4ED,0x4F7,0x4F8,0x4F9,0x4FA,0x4FB):
                params.append( struct.unpack(">I",f.read(4))[0])
            #
            # 0x0500
            #
            elif cmd in (0x561,):
                params = struct.unpack(">ii",f.read(8))
            elif cmd in (0x506,):
                params = struct.unpack(">iii",f.read(12))
            elif cmd in (0x50F,0x514,0x516,0x51A,0x53A,0x53B,0x53F,0x53d,0x53E,0x55b,0x55E,0x55F,0x556):
                params.append(struct.unpack(">i",f.read(4))[0])
            #
            # 0x0600
            #
            elif cmd in (0x653,0x654,0x68A,0x68d,0x68e,0x690,0x691,0x6a1):
                params.append(struct.unpack(">i",f.read(4))[0])
            #
            # 0x0700
            #
            elif cmd in (0x720,0x721,0x728,0x729,0x738):
                params.append(f.read(0x20).split("\x00")[0])
            elif cmd in (0x72D,0x72e):
                params.append(f.read(0x20).split("\x00")[0])
                params.append(struct.unpack(">i",f.read(4)))
            elif cmd in (0x722,):
                params.append(f.read(0x20).split("\x00")[0])
                params.append(struct.unpack(">ii",f.read(8)))
            elif cmd in (0x723,0x72B):
                params.append(struct.unpack(">II",f.read(8)))
            elif cmd in (0x72A,0x72C,0x730,0x732,0x733,0x735):
                params.append(struct.unpack(">i",f.read(4))[0])
            elif cmd in (0x71E,0x726):
                pass
            #
            # 0x0800
            #
            elif cmd in (0x83E,):
                params.append(f.read(0x20).split("\x00")[0])
                params.append(struct.unpack(">II",f.read(8)))
            elif cmd in (0x87e,0x886):
                params.append(struct.unpack(">I",f.read(4)))
            elif cmd in (0x83F,):
                params.append(struct.unpack(">II",f.read(8)))
            #
            # 0x0900
            #
            elif cmd in (0x91A,0x922,0x955):
                params.append(struct.unpack(">ii",f.read(8)))
            elif cmd in (0x953,0x95B,0x9B1,0x9B9,):
                pass
            elif cmd in (0x950,0x0951,0x958,0x959,0x963):
                params.append(struct.unpack(">I",f.read(4))[0])
            elif cmd in (0x91F,):
                params.append(f.read(0x20).split("\x00")[0])
            #
            # 0x0A00
            #
            elif cmd in (0xa5D,):
                params.append(struct.unpack(">I",f.read(4))[0])
            elif cmd in (0xA6a,0xa81,0xA69,0xa8a):
                params.append(struct.unpack(">I",f.read(4))[0])
            elif cmd in (0xA8b,0xa96,0xa97):
                pass
            elif cmd in (0x0A8C,0xA98):
                params.append(f.read(0x20).split("\x00")[0])
                params.extend(struct.unpack(">2i",f.read(8)))
            elif cmd in (0xac2,0xAD0 ):
                params.append(f.read(0x20).split("\x00")[0])
            else:
                print f.tell(),
                if cmd == 1 and f.tell() == ScriptEndOffset:
                    print "------------END"
                else:
                    print
                    #print "\t",commands[-2:]
                    print "\tCommand",hex(cmd),
                    print "\tUnknown:",
                    while f.tell() < ScriptEndOffset:
                        print hex(struct.unpack(">i",f.read(4))[0]),
                    print
                print
                break
            rawcmd = cmd
            if cmd in COMMAND_NAMES.keys():
                cmd = COMMAND_NAMES[cmd]
            else:
                cmd = hex(cmd)
            commands.append((cmd,params))
            print "\t",(cmd,params)
        if not os.path.isdir("out/"+os.path.split(filename)[1]):
            os.makedirs("out/"+os.path.split(filename)[1])
        out = open("{1}/{0}.json".format(ScriptName,"out/"+os.path.split(filename)[1]),"w")
        out.write(json.dumps(commands, indent=4, sort_keys=True))
        out.close()
