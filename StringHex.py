import binascii
import string
import re


class StringHex:
    regexp = re.compile("[0-9a-fA-F]{2}")
    
    def __init__(self, s):
        for i in string.whitespace:
            s = str(s).replace(i,"")
        length = len(s) / 2 * 2
        self.string = s.lower()[:length]
        

    def getBin(self):
        return binascii.a2b_hex(self.removeWhite())

    def toBin(self):
        return binascii.a2b_hex(self.removeWhite())

    @staticmethod
    def fromBin(s):
        return StringHex(binascii.b2a_hex(s))
    
    @staticmethod
    def fromByte(i):
        return StringHex(binascii.b2a_hex(chr(i)))

    @staticmethod
    def fromShort(i):
        return StringHex(binascii.b2a_hex(chr(i/256))) + \
               StringHex(binascii.b2a_hex(chr(i%256)))

    @staticmethod
    def fromNumber(i, width = 0):
        s = hex(i)
        # Remove final "L"
        if s[-1] == "L":
            s = s[:-1]
            
        # Remove initial "0x"
        s = s[2:]
        
        # Add 0 if odd length
        if len(s) % 2 == 1:
            s = '0'+s
            
        if width == 0:
            return StringHex(s)
        else:
            return StringHex(s.rjust(2*width, "0"))


    def toNumber(self):
        return long(self.string, 16)

    def removeWhite(self):
        return self.string.replace(" ","")

    def addWhite(self):
        return " ".join(self.regexp.findall(self.string))


    def getData(self):
        return StringHex(self.string[:-4])

    def getSW(self):
        return StringHex(self.string[-4:])



    def setCLA(self, val):
        val = StringHex(val)
        self.string = val.string + self.string[2:]

    def setINS(self, val):
        val = StringHex(val)
        self.string = self.string[:2] + val.string + self.string[4:]

    def setP1(self, val):
        val = StringHex(val)
        self.string = self.string[:4] + val.string + self.string[6:]

    def setP2(self, val):
        val = StringHex(val)
        self.string = self.string[:6] + val.string + self.string[8:]

    def setP3(self, val):
        val = StringHex(val)
        self.string = self.string[:8] + val.string + self.string[10:]
        pass

    def setP1P2(self, val):
        val = StringHex(val)
        self.string = self.string[:4] + val.string + self.string[8:]
        #self.setP1(val[:2])
        #self.setP2(val[2:4])
        pass


    def inc(self, v="01"):
        x = self.toNumber()
        y = StringHex(v).toNumber()
        self.__init__(StringHex.fromNumber(x+y))

    def dec(self, v="01"):
        x = self.toNumber()
        y = StringHex(v).toNumber()
        self.__init__(StringHex.fromNumber(x-y))

    
    @staticmethod
    def xor(xHex, yHex):
        xHex = StringHex(xHex)
        yHex = StringHex(yHex)
        x = xHex.toNumber()
        y = yHex.toNumber()
        resultLen = max(len(xHex), len(yHex))
        return StringHex.fromNumber(x^y, resultLen)


    @staticmethod
    def add(xHex, yHex):
        xHex = StringHex(xHex)
        yHex = StringHex(yHex)
        x = xHex.toNumber()
        y = yHex.toNumber()
        resultLen = max(len(xHex), len(yHex))
        return StringHex.fromNumber(x+y)


    @staticmethod
    def sub(xHex, yHex):
        xHex = StringHex(xHex)
        yHex = StringHex(yHex)
        x = xHex.toNumber()
        y = yHex.toNumber()
        resultLen = max(len(xHex), len(yHex))
        return StringHex.fromNumber(x-y)


    @staticmethod
    def mul(xHex, yHex):
        xHex = StringHex(xHex)
        yHex = StringHex(yHex)
        x = xHex.toNumber()
        y = yHex.toNumber()
        resultLen = max(len(xHex), len(yHex))
        return StringHex.fromNumber(x*y)

    @staticmethod
    def div(xHex, yHex):
        xHex = StringHex(xHex)
        yHex = StringHex(yHex)
        x = xHex.toNumber()
        y = yHex.toNumber()
        resultLen = max(len(xHex), len(yHex))
        return StringHex.fromNumber(x/y)


    @staticmethod
    def arithmetic_or(xHex, yHex):
        xHex = StringHex(xHex)
        yHex = StringHex(yHex)
        x = xHex.toNumber()
        y = yHex.toNumber()
        resultLen = max(len(xHex), len(yHex))
        return StringHex.fromNumber(x|y, resultLen)


    @staticmethod
    def arithmetic_and(xHex, yHex):
        xHex = StringHex(xHex)
        yHex = StringHex(yHex)
        x = xHex.toNumber()
        y = yHex.toNumber()
        resultLen = max(len(xHex), len(yHex))
        return StringHex.fromNumber(x&y, resultLen)




    def display(self, head, blockLen=16):
        print head,

        nbBlocks = (len(self)+blockLen-1)/blockLen
        intend = len(head)

        for i in range(nbBlocks):
            if i != 0:
                print ' ' * intend,
            print StringHex(self[i*blockLen:i*blockLen+blockLen])

        print


    

    def len(self):
        return StringHex(binascii.b2a_hex(chr(len(self.string)/2)))

    def lenBER(self):
        l = self.__len__()
        if l<128:
            return self.len()
        else:
            return StringHex("81") + self.len()
        

    def __repr__(self):
        return self.addWhite()

    def __str__(self):
        return self.__repr__()


    def __getitem__(self, index):
        tmp = binascii.a2b_hex(self.string)
        fragment = tmp[index]
        return StringHex(binascii.b2a_hex(fragment))


    def __call__(self, *args):
        start = args[0]
        end = args[1]
        return self[start:start+end]


    def __len__(self):
        return len(self.string)/2

    def __add__(self, string):
        return StringHex(self.string + str(string))

    def __radd__(self, string):
        return StringHex(str(string) + self.string)

    def __mul__(self, int):
        return StringHex(self.string * int)

    def __cmp__(self, string):
        v = self.toNumber()-string.toNumber()
        if v<0:
            return -1
        elif v>0:
            return 1
        else:
            return 0

    def __eq__(self, string):
        return self.string.upper() == StringHex(string).string.upper()

    def __ne__(self, string):
        return self.string.upper() != StringHex(string).string.upper()


    def __hash__(self):
        return hash(self.string)
    
    



# ----------tests------

if __name__ == "__main__":
    a=StringHex("6162636465666768")
    print a

    print "getitem() test"
    print a[2]
    print a[2:4]
    print a[-3]
    print a[:3]
    print a[-4:]

    print a[2:4], a[2:4].toNumber()

    print "-------------------"
    a=StringHex("1f")
    b=StringHex("1F")
    print (a==b)

    a=StringHex("1f ca ")
    b=StringHex("1FcA")
    print (a==b)


    print "-------------------"
    a=StringHex("031f")
    b=StringHex("1020")
    print StringHex.xor(a,b)
    
    a=StringHex("06031f")
    b=StringHex("1020")
    print StringHex.xor(a,b)
    
    a=StringHex("06031f")
    b=StringHex("00121020")
    print StringHex.xor(a,b)
    
    print StringHex.xor("334455", "00214441")

    

    
