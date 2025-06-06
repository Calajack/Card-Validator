from StringHex import *

try:
    from Crypto.Cipher import DES3
    from Crypto.Cipher import DES
    from Crypto.Cipher import AES
    from Crypto.Cipher import XOR
    from Crypto.Hash import SHA
except ImportError:
    print("Package Crypto not found.")
    import sys
    sys.exit(1)


def tdesEcbEncrypt(key, message, icv="0000000000000000"):
    keyB = StringHex(key).getBin()
    messageB = StringHex(message).getBin()
    icvB = StringHex(icv).getBin()    
    algo = DES3.new(keyB, DES3.MODE_ECB, icvB)
    return StringHex.fromBin(algo.encrypt(messageB))


def tdesEcbDecrypt(key, message, icv="0000000000000000"):
    keyB = StringHex(key).getBin()
    messageB = StringHex(message).getBin()
    icvB = StringHex(icv).getBin()
    algo = DES3.new(keyB, DES3.MODE_ECB, icvB)
    return StringHex.fromBin(algo.decrypt(messageB))


def tdesCbcEncrypt(key, message, icv="0000000000000000"):
    keyB = StringHex(key).getBin()
    messageB = StringHex(message).getBin()
    icvB = StringHex(icv).getBin()
    algo = DES3.new(keyB, DES3.MODE_CBC, icvB)
    return StringHex.fromBin(algo.encrypt(messageB))


def tdesCbcDecrypt(key, message, icv="0000000000000000"):
    keyB = StringHex(key).getBin()
    messageB = StringHex(message).getBin()
    icvB = StringHex(icv).getBin()
    algo = DES3.new(keyB, DES3.MODE_CBC, icvB)
    return StringHex.fromBin(algo.decrypt(messageB))

def desEcbEncrypt(key, message, icv="0000000000000000"):
    keyB = StringHex(key).getBin()
    messageB = StringHex(message).getBin()
    icvB = StringHex(icv).getBin()    
    algo = DES.new(keyB, DES.MODE_ECB, icvB)
    return StringHex.fromBin(algo.encrypt(messageB))


def desEcbDecrypt(key, message, icv="0000000000000000"):
    keyB = StringHex(key).getBin()
    messageB = StringHex(message).getBin()
    icvB = StringHex(icv).getBin()
    algo = DES.new(keyB, DES.MODE_ECB, icvB)
    return StringHex.fromBin(algo.decrypt(messageB))


def desCbcEncrypt(key, message, icv="0000000000000000"):
    keyB = StringHex(key).getBin()
    messageB = StringHex(message).getBin()
    icvB = StringHex(icv).getBin()
    algo = DES.new(keyB, DES.MODE_CBC, icvB)
    return StringHex.fromBin(algo.encrypt(messageB))


def desCbcDecrypt(key, message, icv="0000000000000000"):
    keyB = StringHex(key).getBin()
    messageB = StringHex(message).getBin()
    icvB = StringHex(icv).getBin()
    algo = DES.new(keyB, DES.MODE_CBC, icvB)
    return StringHex.fromBin(algo.decrypt(messageB))


def aesEcbEncrypt(key, message, icv="00000000000000000000000000000000"):
    keyB = StringHex(key).getBin()
    messageB = StringHex(message).getBin()
    icvB = StringHex(icv).getBin()
    algo = AES.new(keyB, AES.MODE_ECB, icvB)
    return StringHex.fromBin(algo.encrypt(messageB))


def aesEcbDecrypt(key, message, icv="00000000000000000000000000000000"):
    keyB = StringHex(key).getBin()
    messageB = StringHex(message).getBin()
    icvB = StringHex(icv).getBin()
    algo = AES.new(keyB, AES.MODE_ECB, icvB)
    return StringHex.fromBin(algo.decrypt(messageB))


def aesCbcEncrypt(key, message, icv="00000000000000000000000000000000"):
    keyB = StringHex(key).getBin()
    messageB = StringHex(message).getBin()
    icvB = StringHex(icv).getBin()
    algo = AES.new(keyB, AES.MODE_CBC, icvB)
    return StringHex.fromBin(algo.encrypt(messageB))


def aesCbcDecrypt(key, message, icv="00000000000000000000000000000000"):
    keyB = StringHex(key).getBin()
    messageB = StringHex(message).getBin()
    icvB = StringHex(icv).getBin()
    algo = AES.new(keyB, AES.MODE_CBC, icvB)
    return StringHex.fromBin(algo.decrypt(messageB))


def xor(block1, block2):
    block1 = StringHex(block1).getBin()
    block2 = StringHex(block2).getBin()
    obj = XOR.new(block1)
    xored = obj.encrypt(block2)
    return StringHex.fromBin(xored)
    


def rsa(keyExp, keyMod, msg):
    keyExpL = int(StringHex(keyExp).string, 16)
    keyModL = int(StringHex(keyMod).string, 16)
    msgL = int(StringHex(msg).string, 16)
    result = pow(msgL, keyExpL, keyModL)
    return  StringHex.fromNumber(result, len(keyMod))

def rsaCrt(p, q, dp, dq, pq, msg, length):
    pL = int(StringHex(p).string, 16)
    qL = int(StringHex(q).string, 16)
    dpL = int(StringHex(dp).string, 16)
    dqL = int(StringHex(dq).string, 16)
    pqL = int(StringHex(pq).string, 16)
    msgL = int(StringHex(msg).string, 16)

    sp = pow(msgL, dpL, pL)
    sq = pow(msgL, dqL, qL)
    result = sq + ((pqL * (sp - sq)) % pL ) * qL

    return  StringHex.fromNumber(result, length)


def macDes(key, message, icv="0000000000000000"):
    k1 = StringHex(key)[:8]
    k2 = StringHex(key)[8:]
    tmpResult = macTdes(k1+k1, message, icv)
    tmpResult = tdesEcbDecrypt(k2+k2, tmpResult, "0000000000000000")
    return tdesEcbEncrypt(k1+k1, tmpResult, "0000000000000000")


def macDes2(key, message, icv="0000000000000000"):
    k2 = StringHex(key)[:8]
    k1 = StringHex(key)[8:]
    des = desCbcEncrypt(k1, message, icv)
    mac = des[-8:]
    tmpResult = desCbcDecrypt(k2, mac, "0000000000000000")
    return desCbcEncrypt(k1, tmpResult, "0000000000000000")


def macTdes(key, message, icv="0000000000000000"):
    des = tdesCbcEncrypt(key, message, icv)
    return des[-8:]




def pad0(plainData):
    newData = StringHex(plainData)
    while len(newData)%8:
        newData = newData + "00"
    return newData


def pad1(plainData):
    newData = StringHex(plainData) + "80"
    while len(newData)%8:
        newData = newData + "00"
    return newData
    

def luhn10(PAN):
    
    luhn_digit = "X"
    s = reversed(list(PAN))
    i = 0
    total = 0
    for digit in s:
        i = i + 1
        d = int(digit) * (1 + i % 2)
        if d > 9: d = 1 + (d % 10)
        total = total + d

    luhn_digit = "%d" % ((10-(total % 10)) % 10)
    
    return luhn_digit  


def DeriveUDK(IMK, PAN, PSN):
    UDK = ""
    PAN = PAN.replace('F', '')
    
    while len(PSN) < 2: PSN = "0" + PSN
    PSN = PSN[:2]
    
    # built input buffer
    msg = PAN + PSN
    while len(msg) < 16: msg = "0" + msg
    msg = msg[-16:]
    
    UDK_L = macTdes(IMK, msg).string.upper()
    msg = xor(msg, "FFFFFFFFFFFFFFFF").string.upper()
    UDK_R = macTdes(IMK, msg).string.upper()

    UDK = UDK_L + UDK_R
    
    return UDK


def ComputeARQC_CVN10(CDOL1, AIP, ATC, IAD, UDK_AC):
    ARQC = ""
    
    CVR = IAD[6:14]
    msg = CDOL1[:58] + AIP + ATC + CVR
    while len(msg) % 16 != 0: msg = msg + "0"
    
    ARQC =  macDes(UDK_AC, msg).string.upper()
    
    return ARQC


def ComputeARQC_CVN18(CDOL1, AIP, ATC, IAD, UDK_AC):
    ARQC, SDK = ComputeARQC_DPAS(CDOL1, AIP, ATC, IAD, UDK_AC)
    
    return ARQC, SDK

def ComputeARQC_MCHIP4(CDOL1, AIP, ATC, IAD, UDK_AC):
    ARQC = ""
    
    div_A = ATC + "F00000000000"
    div_B = ATC + "0F0000000000"
    
    SDK_A = macDes(UDK_AC, div_A).string.upper()
    SDK_B = macDes(UDK_AC, div_B).string.upper()
    
    SDK = SDK_A + SDK_B
    
    CVR = IAD[4:16]
    msg = CDOL1[:58] + AIP + ATC + CVR + "80"
    while len(msg) % 16 != 0: msg = msg + "0"
    
    ARQC =  macDes(SDK, msg).string.upper()
    
    return ARQC


def ComputeARQC_DPAS(CDOL1, AIP, ATC, IAD, UDK_AC):
    ARQC = ""
    
    div_A = ATC + "F00000000000"
    div_B = ATC + "0F0000000000"
    
    SDK_A = macDes(UDK_AC, div_A).string.upper()
    SDK_B = macDes(UDK_AC, div_B).string.upper()
    
    SDK = SDK_A + SDK_B
    
    msg = CDOL1[:58] + AIP + ATC + IAD + "80"
    if IAD[2:4] == "06": msg = CDOL1[:58] + AIP + ATC + IAD[4:16] + "80"
        
    while len(msg) % 16 != 0: msg = msg + "0"
    
    ARQC =  macDes(SDK, msg).string.upper()
    
    return ARQC, SDK


def ComputeARPC(ARQC, ARC, UDK_AC):
    ARPC = ""
    
    while len(ARC) < 16: ARC = ARC + "0"
    msg = xor(ARC, ARQC).string.upper()
    ARPC =  macDes(UDK_AC, msg).string.upper()
    
    return ARPC    


def ComputeARPC_CVN18(ARQC, CSU, SDK_AC):
    ARPC = ""
    
    Y = ARQC + CSU + "80"
    while len(Y) < 32: Y = Y + "0"
    ARPC =  macDes(SDK_AC, Y).string.upper()[:8]
    
    return ARPC       

def ComputeMAC(CMD, ARQC, ATC, UDK_SMI, bMC_SKD = False):
    MAC = ""
    
    SDK_A = ""
    SDK_B = ""
    
    if bMC_SKD == False:
        div_A = "000000000000" + ATC
        div_B = "000000000000%04X" % (0xFFFF - int(StringHex(ATC).string, 16))
        
        SDK_A = xor(div_A, UDK_SMI[:16]).string.upper()
        SDK_B = xor(div_B, UDK_SMI[16:]).string.upper()
    
    else:
        RND = ARQC    
 
        RND_A = RND[:4] + "F0" + RND[6:]
        RND_B = RND[:4] + "0F" + RND[6:]
        
        SDK_A = macDes(UDK_SMI, RND_A).string.upper()
        SDK_B = macDes(UDK_SMI, RND_B).string.upper()
    
    SDK = SDK_A + SDK_B
    
    msg = CMD + ATC + ARQC + "80"
    while len(msg) % 16 != 0: msg = msg + "0"
    
    MAC =  macDes(SDK, msg).string.upper()
    
    return MAC


def computeKCV(key, length):
    block = ""
    while len(block) < 16:
        block = block + "0"
        
    kcv = macDes(key, block).string.upper()
    return kcv[:length*2]
    
    
try:
    import hashlib

    def sha1(plainData):
        binData = StringHex(plainData).getBin()
        hash = hashlib.sha1(binData).hexdigest()
        return StringHex(hash)

    def sha224(plainData):
        binData = StringHex(plainData).getBin()
        hash = hashlib.sha224(binData).hexdigest()
        return StringHex(hash)

    def sha256(plainData):
        binData = StringHex(plainData).getBin()
        hash = hashlib.sha256(binData).hexdigest()
        return StringHex(hash)

    def ripemd160(plainData):
        binData = StringHex(plainData).getBin()
        hash = hashlib.new('ripemd160')
        hash.update(binData)
        return StringHex(hash.hexdigest())





    

except ImportError:
    print("Package hashlib (Python 2.5) not found.")

    def sha1(plainData):
        newData = StringHex(plainData)
        algo = SHA.new()
        algo.update(newData.getBin())
        result  = algo.digest()
        return  StringHex.fromBin(result)


# ----------tests------

if __name__ == "__main__":
    key="00112233445566770000111122223333"
    msg="0123012301230123 0011223344556677"
    
    CMD = "841E000008"
    ARQC = "E4112E5CB30E3D7D"
    ATC = "0006"
    UDK_SMI = "208A4CC2941C7C7A388554EC32B0AE54"

    MAC = ComputeMAC(CMD, ARQC, ATC, UDK_SMI, True)
    print MAC
    print
    print
    
    key = "52D0BAC246850B37E9FD234CDF29DFF1"
    kcv = computeKCV(key, 3)
    print kcv
    print "A5F1C6"


