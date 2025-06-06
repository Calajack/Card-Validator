from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes
from datetime import datetime
import CardCrypto
import sys





class CardCommands():
    
    Present_AIDs = []
    Terminal_Data = {}
    
    list_APDUs = []
    

    
    
    def __init__ (self, cardservice, Terminal_Data, audit, bExitMsg, nextFunction = None, T1 = False):
        self.cardservice = cardservice
        self.cp = CardProcess(audit, bExitMsg, nextFunction)
        self.T1 = T1
        self.Terminal_Data = Terminal_Data
        self.audit = audit
        self.bExitMsg = bExitMsg
        self.nextFunction = nextFunction


    def printATR(self):
        self.audit.write("Connected to " + str(self.cardservice.connection.getReader()))
        self.audit.write("")
        self.audit.write("ATR")
        self.audit.write(toHexString( self.cardservice.connection.getATR()))
        self.audit.write("")
        pass 

    
    def SendRaw(self, cmd, bStopOnError = True):
        cmd = cmd.replace(" ", "")
        if self.T1: cmd = cmd + "00"
        apdu = toBytes(cmd)
        response, sw1, sw2 = self.cardservice.connection.transmit( apdu )
        self.audit.write( toHexString(apdu) )
                        
        if (sw1 != 0x90 and sw1 != 0x61 and sw1 != 0x6C): 
            if bStopOnError == True:
                self.audit.write("%02X %02X" % (sw1, sw2)) 
                self.cp.ExitProgram()
        
        data = self.GetResponse(apdu, response, sw1, sw2)
        return data


    def Select(self, AID):
        self.cp.tags_dict = {}
        AID = AID.replace(" ", "")
        SELECT = "00A40400 %02x" %(len(AID)/2) + AID
        if self.T1: SELECT = SELECT + "00"
        apdu = toBytes(SELECT)
        response, sw1, sw2 = self.cardservice.connection.transmit( apdu )
        self.audit.write(toHexString(apdu))

        data, rsp = self.GetResponse(apdu, response, sw1, sw2)
        
        self.list_APDUs.append([toHexString(apdu), data])
        
        return data, rsp
    
    
    def SelectFromList(self, Known_AIDs):
        self.Present_AIDs = []
        self.audit.write("--- Listing card applications")
        self.audit.write("")
        for AID in Known_AIDs:
            self.audit.write("Select " + AID[0])
            data, response = self.Select(AID[1])
            
            if (response[-2] == 0x90 and response[-1] == 0x00) or (response[-2] == 0x62 and response[-1] == 0x83):
                self.Present_AIDs.append(AID)
            
            self.audit.write("")
            
        if len(self.Present_AIDs) < 1:
            self.audit.write("Found no compatible application - exiting")
            self.cp.ExitProgram()
            
        self.audit.write("Found application(s):")
        for AID in self.Present_AIDs:
            self.audit.write(" -%s (%s)" % (AID[0], AID[1]))
        
        self.audit.write("")
        self.audit.write("")
        AID = self.Present_AIDs[0]
        self.audit.write("--- Running transaction with " + AID[0])
        self.audit.write("")
        
        self.audit.write("Select " + AID[0])
        data, response = self.Select(AID[1])
        self.audit.write("")
        if (response[-2] == 0x62 and response[-1] == 0x83):
            self.audit.write("Application is blocked - no need for a reset - exiting")
            self.cp.ExitProgram()
        
        self.cp.ParseAndExtract(response)
        self.audit.write("")
        self.audit.write("")
        

             

        
    def GetProcessingOptions(self):
        self.audit.write("Get Processing Options")
        
        self.cp.record_list = []
        
        if "9F38" in self.cp.tags_dict.keys():
            dol = self.cp.BuildDOL("9F38", self.Terminal_Data)
            data = "83 %02x" %(len(dol)/2) + dol
        else:
            data = "8300"
            
        GPO = "80A80000 %02x" %(len(data)/2) + data
        if self.T1: GPO = GPO + "00"
        apdu = toBytes(GPO)
        response, sw1, sw2 = self.cardservice.connection.transmit( apdu )
        self.audit.write(toHexString(apdu))
        
        data, rsp = self.GetResponse(apdu, response, sw1, sw2)
        self.audit.write("")

        if rsp[0] == 0x80:
            rsp = rsp[1:-2]
            if rsp[0] < 0x80:
                rsp = rsp[1:]
            else:
                rsp = rsp[2:]
            
            self.cp.tags_dict["82"] = rsp [:2]
            self.cp.tags_dict["94"] = rsp [2:]
            
            self.audit.write("Found tag %s with value \"%s\"" %("82", toHexString(self.cp.tags_dict["82"]).replace(' ', '')))
            self.audit.write("Found tag %s with value \"%s\"" %("94", toHexString(self.cp.tags_dict["94"]).replace(' ', '')))
            
        else:        
            self.cp.ParseAndExtract(rsp)
        self.audit.write("")
        self.cp.BuildRecordList()
        
        self.list_APDUs.append([toHexString(apdu), data])
       
        return data
        

    def FirstGenerateAC_ARQC(self):
        data = self.cp.BuildDOL("8C", self.Terminal_Data)
        
        self.audit.write("")
        self.audit.write("First Generate AC - ARQC") 
        GENERATE_AC = "80AE8000 %02x" %(len(data)/2) + data
        if self.T1: GENERATE_AC = GENERATE_AC + "00"
        apdu = toBytes(GENERATE_AC)
        response, sw1, sw2 = self.cardservice.connection.transmit( apdu )
        self.audit.write(toHexString(apdu))
                

        data, rsp = self.GetResponse(apdu, response, sw1, sw2)
        self.audit.write("")

        if rsp[0] == 0x80:
            rsp = rsp[1:-2]
            if rsp[0] < 0x80:
                rsp = rsp[1:]
            else:
                rsp = rsp[2:]
            
            self.cp.tags_dict["9F27"] = rsp [:1]
            self.cp.tags_dict["9F36"] = rsp [1:3]
            self.cp.tags_dict["9F26"] = rsp [3:11]
            self.cp.tags_dict["9F10"] = rsp [11:]
            
            self.audit.write( "Found tag %s with value \"%s\"" %("9F27", toHexString(self.cp.tags_dict["9F27"]).replace(' ', '')))
            self.audit.write( "Found tag %s with value \"%s\"" %("9F36", toHexString(self.cp.tags_dict["9F36"]).replace(' ', '')))
            self.audit.write( "Found tag %s with value \"%s\"" %("9F26", toHexString(self.cp.tags_dict["9F26"]).replace(' ', '')))
            self.audit.write( "Found tag %s with value \"%s\"" %("9F10", toHexString(self.cp.tags_dict["9F10"]).replace(' ', '')))
            
        else:        
            self.cp.ParseAndExtract(rsp)
        self.audit.write("")

        if self.cp.tags_dict["9F27"][0] == 0x80:
            self.audit.write( "Generate AC returned ARQC")
        else:
            self.audit.write( "Generate AC failed to return ARQC, returned %d instead - exiting" % self.cp.tags_dict["9F27"][0])
            self.cp.ExitProgram()

        self.audit.write("")
        return response


    def FirstGenerateAC_TC(self):
        data = self.cp.BuildDOL("8C", self.Terminal_Data)
        
        self.audit.write("")
        self.audit.write("First Generate AC - TC") 
        GENERATE_AC = "80AE4000 %02x" %(len(data)/2) + data
        if self.T1: GENERATE_AC = GENERATE_AC + "00"
        apdu = toBytes(GENERATE_AC)
        response, sw1, sw2 = self.cardservice.connection.transmit( apdu )
        self.audit.write(toHexString(apdu))
                

        data, rsp = self.GetResponse(apdu, response, sw1, sw2)
        self.audit.write("")

        if rsp[0] == 0x80:
            rsp = rsp[1:-2]
            if rsp[0] < 0x80:
                rsp = rsp[1:]
            else:
                rsp = rsp[2:]
            
            self.cp.tags_dict["9F27"] = rsp [:1]
            self.cp.tags_dict["9F36"] = rsp [1:3]
            self.cp.tags_dict["9F26"] = rsp [3:11]
            self.cp.tags_dict["9F10"] = rsp [11:]
            
            self.audit.write( "Found tag %s with value \"%s\"" %("9F27", toHexString(self.cp.tags_dict["9F27"]).replace(' ', '')))
            self.audit.write( "Found tag %s with value \"%s\"" %("9F36", toHexString(self.cp.tags_dict["9F36"]).replace(' ', '')))
            self.audit.write( "Found tag %s with value \"%s\"" %("9F26", toHexString(self.cp.tags_dict["9F26"]).replace(' ', '')))
            self.audit.write( "Found tag %s with value \"%s\"" %("9F10", toHexString(self.cp.tags_dict["9F10"]).replace(' ', '')))
            
        else:        
            self.cp.ParseAndExtract(rsp)
        self.audit.write("")

        CID = self.cp.tags_dict["9F27"][0]
        if CID == 0x40:
            self.audit.write( "Generate AC returned TC")
        else:
            self.audit.write( "Generate AC failed to return TQC, returned %d instead - exiting" % self.cp.tags_dict["9F27"][0])

        self.audit.write("")
        return response, CID


    def ExternalAuthenticate(self):
        
        # skip if bit not set in AIP
        if self.cp.tags_dict["82"][0] & 0x04 != 0x04: return
        
        self.audit.write("")
        self.audit.write("")
        self.audit.write( "External Authenticate")
        if "91" not in self.cp.tags_dict.keys():
            self.audit.write("No value for tag 91 - exiting")
            self.cp.ExitProgram()
        
        data = toHexString(self.cp.tags_dict["91"]).replace(' ', '')
        EXTERNAL_AUTHENTICATE = "00820000 %02x" %(len(data)/2) + data
        
        apdu = toBytes(EXTERNAL_AUTHENTICATE)
        response, sw1, sw2 = self.cardservice.connection.transmit( apdu )
        self.audit.write(toHexString(apdu))
                
        data = self.GetResponse(apdu, response, sw1, sw2)
        self.audit.write("")
        
        return 

    def SecondGenerateAC_TC(self):
        
        self.audit.write("")
        self.audit.write("--- Completing online transaction")
        self.audit.write("")
        data = self.cp.BuildDOL("8D", self.Terminal_Data)
        self.audit.write("")
        self.audit.write("Second Generate AC - TC" )
        GENERATE_AC = "80AE4000 %02x" %(len(data)/2) + data
        if self.T1: GENERATE_AC = GENERATE_AC + "00"
        apdu = toBytes(GENERATE_AC)
        response, sw1, sw2 = self.cardservice.connection.transmit( apdu )
        self.audit.write(toHexString(apdu))
                

        data, rsp = self.GetResponse(apdu, response, sw1, sw2)
        self.audit.write("")

        if rsp[0] == 0x80:
            rsp = rsp[1:-2]
            if rsp[0] < 0x80:
                rsp = rsp[1:]
            else:
                rsp = rsp[2:]
            
            self.cp.tags_dict["9F27"] = rsp [:1]
            self.cp.tags_dict["9F36"] = rsp [1:3]
            self.cp.tags_dict["9F26"] = rsp [3:11]
            self.cp.tags_dict["9F10"] = rsp [11:]
            
            self.audit.write("Found tag %s with value \"%s\"" %("9F27", toHexString(self.cp.tags_dict["9F27"]).replace(' ', '')))
            self.audit.write("Found tag %s with value \"%s\"" %("9F36", toHexString(self.cp.tags_dict["9F36"]).replace(' ', '')))
            self.audit.write("Found tag %s with value \"%s\"" %("9F26", toHexString(self.cp.tags_dict["9F26"]).replace(' ', '')))
            self.audit.write("Found tag %s with value \"%s\"" %("9F10", toHexString(self.cp.tags_dict["9F10"]).replace(' ', '')))
            
        else:        
            self.cp.ParseAndExtract(rsp)
        self.audit.write("")

        if self.cp.tags_dict["9F27"][0] == 0x40:
            self.audit.write("Generate AC returned TC")
        else:
            self.audit.write("Generate AC failed to return TC, returned %d instead - exiting" % self.cp.tags_dict["9F27"][0])
            self.cp.ExitProgram()

        self.audit.write("")
        return response

    
    def UnblockPIN(self):
        
        # skip if card is not VISA
        if self.cp.PAN[0] != "4":
            self.audit.write("PIN was unblocked during Second Generate AC, no need for a script")
            self.audit.write("")
            return
        
        # skip for CVN 18 (0x12)
        if self.cp.lastCVN == "12":
            self.audit.write("Not unblocking PIN with script on VISA CVN 18 card")
            self.audit.write("")
            return
        
        self.audit.write("")
        self.audit.write("Script: PIN Unblock")

        PIN_UNBLOCK = "8424000008"
        MAC = self.cp.ComputeMAC(PIN_UNBLOCK)
        PIN_UNBLOCK = PIN_UNBLOCK + MAC

        apdu = toBytes(PIN_UNBLOCK)
        response, sw1, sw2 = self.cardservice.connection.transmit( apdu )
        self.audit.write(toHexString(apdu))
                
        data = self.GetResponse(apdu, response, sw1, sw2)
        self.audit.write("")
        
        return 


    def BlockApplication(self):
        
        
        self.audit.write("")
        self.audit.write("Script: Application Block")

        APPLICATION_BLOCK = "841E000008"
        MAC = self.cp.ComputeMAC(APPLICATION_BLOCK)
        APPLICATION_BLOCK = APPLICATION_BLOCK + MAC

        apdu = toBytes(APPLICATION_BLOCK)
        response, sw1, sw2 = self.cardservice.connection.transmit( apdu )
        self.audit.write(toHexString(apdu))
                
        data = self.GetResponse(apdu, response, sw1, sw2)
        self.audit.write("")
        
        return 


        
    def GetChallenge(self):
        self.audit.write("Get challenge")
        
        GET_CHALLENGE = "0084000000"
        if self.T1: GET_CHALLENGE = GET_CHALLENGE + "00"
        apdu = toBytes(GET_CHALLENGE)
        response, sw1, sw2 = self.cardservice.connection.transmit( apdu )
        self.audit.write(toHexString(apdu))
                
        data = self.GetResponse(apdu, response, sw1, sw2)
        self.audit.write("")
        return data

                
    def GetData(self, tag, DataName = ""):
        self.audit.write("Get Data " + DataName)
        tag = tag.replace(" ", "")
        GET_DATA = "80CA" + tag + "00"
        if self.T1: GET_DATA = GET_DATA + "00"
        apdu = toBytes(GET_DATA)
        response, sw1, sw2 = self.cardservice.connection.transmit( apdu )
        self.audit.write(toHexString(apdu))
        
        data = self.GetResponse(apdu, response, sw1, sw2)
        self.audit.write("")
        return data

        
    def ReadRecord(self, sfi, rec):
        self.audit.write("Read Record %s in SFI %s" % (rec, sfi))
        P2 = "%02x" % ((sfi << 3) + 4) 
        P1 = "%02x" % rec
        
        READ_RECORD = "00B2" + P1 + P2 + "00"
        if self.T1: READ_RECORD = READ_RECORD + "00"
        apdu = toBytes(READ_RECORD)
        response, sw1, sw2 = self.cardservice.connection.transmit( apdu )
        self.audit.write(toHexString(apdu))
        
        data, resp = self.GetResponse(apdu, response, sw1, sw2)
        self.audit.write("")
        
        self.list_APDUs.append([toHexString(apdu), data])
        return data, resp


    def ReadRecords(self):
        
        list_responses = []
        
        for rec in self.cp.record_list:
            self.audit.write("")
            data, response = self.ReadRecord(rec[0], rec[1])
            self.cp.ParseAndExtract(response)
            self.audit.write("")
            
            list_responses.append(data)
        
        return list_responses

    
    "verifies the PIN"
    def Verify(self, PIN):
        self.audit.write("PIN Verify")
        
        VERIFY = "002000800824" + PIN + "FFFFFFFFFF"
        if self.T1: VERIFY = VERIFY + "00"
        apdu = toBytes(VERIFY)
        response, sw1, sw2 = self.cardservice.connection.transmit( apdu )
        self.audit.write(toHexString(apdu))
        
        data = self.GetResponse(apdu, response, sw1, sw2)
        self.audit.write("")
        return data
       
    "decides whether to set a get response command or re-send the command with different Lc"
    def GetResponse(self, apdu, response, sw1, sw2):
        if sw1 == 0x61:
            GET_RESPONSE = [0X00, 0XC0, 00, 00 ]
            apdu = GET_RESPONSE + [sw2]
            response, sw1, sw2 = self.cardservice.connection.transmit( apdu )
            
        elif sw1 == 0x6C:
            apdu = apdu[:4]
            apdu.append(sw2)
            response, sw1, sw2 = self.cardservice.connection.transmit( apdu )

        rsp = response 
        response.append(sw1)
        response.append(sw2)
        self.audit.write(toHexString(response))
        return toHexString(response), rsp


class CardProcess():
    tags_dict = {}
    record_list = []
    CDOL1 = ""
    ARQC = ""
    ARPC = ""
    ARC = ""
    PAN = ""
    lastCVN = ""
    
    def __init__(self, audit, bExitMsg, nextFunction):
        self.audit = audit
        self.bExitMsg = bExitMsg
        self.bPersoMode = False
        self.nextFunction = nextFunction
        pass
    

    def ExitProgram(self):
        self.audit.write("")
        if self.bExitMsg == True:
            self.audit.write("Press Enter to exit")
            raw_input()
        else:
            self.audit.write("Process finished")
            
        if self.nextFunction != None:
            self.nextFunction()
        
        sys.exit()
        
        return
    
    def ParseAndExtract(self, data, bRemoveSW = True):
        
        if bRemoveSW:
            data = data[:-2]
        
        # remove template tag
        if data[0] in [0x6F, 0x77, 0x70]:
            if data [1] < 0x80:
                data = data[2:]
            else:
                data = data[3:]
        
        while len(data) > 2:
            tag = ""
            if data[0] in [0x9F, 0x5F]:
                tag = "%02X%02X" % (data[0], data[1])
                data = data[2:]
            else:
                tag = "%02X" % data[0]
                data = data[1:]
            
            length = 0
            if data[0] < 0x80:
                length = data[0]
                data = data[1:]
            else:
                length = data[1]
                data = data[2:]
            
            value = data[:length]
            data = data[length:]
            
            if tag in ["A5"]:
                self.ParseAndExtract(value, False)
            else:
                self.tags_dict[tag] = value
                self.audit.write("Found tag %s with value \"%s\"" %(tag, toHexString(value).replace(' ', '')))
        
            if self.bPersoMode == False and tag == "5A" and "5413330089020011" in toHexString(value).replace(' ', ''):
                self.audit.write("")
                self.audit.write("")
                self.audit.write("Programmed not to run online transaction on card with PAN '%s' - exiting" % toHexString(value).replace(' ', ''))
                self.ExitProgram()
            
        return
        
    def BuildDOL(self, tag, Terminal_Data):

        TLV = self.tags_dict[tag]
        DOL = []
        data = ""       
        
        
        while len(TLV) > 0:
            t = ""
            if TLV[0] in [0x9F, 0x5F]:
                t = "%02X%02X" % (TLV[0], TLV[1])
                TLV = TLV[2:]
            else:
                t = "%02X" % TLV[0]
                TLV = TLV[1:]
        
            length = TLV[0]
            TLV = TLV[1:]
            
            DOL.append([t, length])

        self.audit.write("Building data object list from tag %s:" % tag)
        
        for d in DOL:
            v = ""
            if d[0] in Terminal_Data.keys():
                v = Terminal_Data[d[0]]
                
            elif d[0] in self.tags_dict.keys():
                v = toHexString(self.tags_dict[d[0]]).replace(' ', '')
            
            elif d[0] == "9A":
                dt = datetime.now()
                v = "%02d%02d%02d" % (dt.year-2000, dt.month, dt.day)
                
            while len(v) < d[1] * 2: v = v + "0"
            v = v[:d[1] * 2]
            
            self.audit.write(" %s-%s" % (d[0], v))
            
            data = data + v
        
        if tag == "8C": self.CDOL1 = data

        return data
   
    def BuildRecordList(self):
        AFL = self.tags_dict["94"]
        
        if len(AFL) == 0:
            self.audit.write("AFL list is empty - exiting")
            self.ExitProgram()
        
        if len(AFL) % 4 != 0:
            self.audit.write("AFL list \"%s\" is not a multiple of 4 bytes - exiting" % toHexString(AFL).replace(' ', ''))
            self.ExitProgram()
        
        while len(AFL) > 0:
            for i in range(0, AFL[2]-AFL[1]+1):
                self.record_list.append([AFL[0] >> 3, AFL[1] + i])
            
            AFL = AFL[4:]
                
        return
    
    def ValidateCryptography(self):
        
        self.audit.write("")
        self.audit.write("--- Validating cryptography")
        self.audit.write("")
        self.lastCVN = ""
        
        if "5A" in self.tags_dict.keys():
            self.PAN = toHexString(self.tags_dict["5A"]).replace(' ', '')
        else:
            self.PAN = toHexString(self.tags_dict["57"]).replace(' ', '')
            pos = self.PAN.find("=")
            if pos < 1: pos = self.PAN.find("D")
            if pos > 0: self.PAN = self.PAN[:pos]
            
        self.audit.write("Card has PAN " + self.PAN)
        if self.PAN[0] == "4" or self.PAN[0:3] == "994"  or self.PAN[0:3] == "997":
            self.audit.write("validating cryptography for VISA card")
            self.ValidateCrypto_VISA(self.PAN)
        elif self.PAN[0] == "5" or self.PAN[0:3] == "995"  or self.PAN[0:3] == "998":
            self.audit.write("validating cryptography for MasterCard card")
            self.ValidateCrypto_MC(self.PAN)
        elif self.PAN[0:3] == "679":
            self.audit.write("validating cryptography for Maestro card")
            self.ValidateCrypto_MC(self.PAN)
        elif self.PAN[0:2] in ["36", "65"]:
            self.audit.write("validating cryptography for DPAS card")
            self.ValidateCrypto_DPAS(self.PAN)
        else:
            self.audit.write("cryptography for PAN '%s' is not supported - exiting" % self.PAN)
            self.ExitProgram()
        
        
        return
    
    def ValidateCrypto_VISA(self, PAN):
        
        IMK = "11223300556677881122330055667788"
        self.audit.write("using IMK '%s'" % IMK)
        
        PSN = "00"
        if "5F34" in self.tags_dict.keys(): PSN = toHexString(self.tags_dict["5F34"]).replace(' ', '')
        UDK_AC = CardCrypto.DeriveUDK(IMK, PAN, PSN)
        self.audit.write("derived UDK_AC '%s' from PAN '%s' and PSN '%s'" % (UDK_AC, PAN, PSN))
        
        AIP = toHexString(self.tags_dict["82"]).replace(' ', '')
        ATC = toHexString(self.tags_dict["9F36"]).replace(' ', '')
        IAD = toHexString(self.tags_dict["9F10"]).replace(' ', '')
        card_ARQC = toHexString(self.tags_dict["9F26"]).replace(' ', '')
        self.ARQC = card_ARQC 
        self.lastCVN = IAD [4:6]
        
        if IAD [4:6] == "0A":
            computed_ARQC = CardCrypto.ComputeARQC_CVN10(self.CDOL1, AIP, ATC, IAD, UDK_AC)
            self.audit.write("computed ARQC '%s' for CVN 10 card" % (computed_ARQC))
            
            
            if computed_ARQC == card_ARQC:
                self.audit.write("ARQC matched")
            else:
                self.audit.write("ARQC mismatch, card returned '%s' - exiting" % card_ARQC)
                self.ExitProgram()
                
            self.audit.write("")
            self.ARC = "3030"
            self.ARPC = CardCrypto.ComputeARPC(computed_ARQC, self.ARC, UDK_AC)
            self.tags_dict["8A"] = toBytes(self.ARC)
            self.tags_dict["91"] = toBytes(self.ARPC + self.ARC)
            self.audit.write("computed ARPC '%s' using response code '%s'" % (self.ARPC, self.ARC))
            
         
        elif IAD [4:6] == "12":
            computed_ARQC, SDK = CardCrypto.ComputeARQC_CVN18(self.CDOL1, AIP, ATC, IAD, UDK_AC)
            self.audit.write("computed ARQC '%s' for CVN 18 card" % (computed_ARQC))
            
            
            if computed_ARQC == card_ARQC:
                self.audit.write("ARQC matched")
            else:
                self.audit.write("ARQC mismatch, card returned '%s' - exiting" % card_ARQC)
                self.ExitProgram() 
                
                
            self.audit.write("")
            CSU = "00800000"
            self.ARC = "3030"
            self.ARPC = CardCrypto.ComputeARPC_CVN18(computed_ARQC, CSU, SDK)
            self.tags_dict["8A"] = toBytes(self.ARC)
            self.tags_dict["91"] = toBytes(self.ARPC + CSU)
            self.audit.write("computed ARPC '%s' using CSU '%s'" % (self.ARPC, CSU))
            self.audit.write("")
            
            
        else:
            self.audit.write("found unsupported CVN '%s' in IAD '%s' - exiting" % (IAD [4:6], IAD))
            self.ExitProgram()
        
        return
    

    def ValidateCrypto_MC(self, PAN):
        
        IMK = "9E15204313F7318ACB79B90BD986AD29"
        self.audit.write("using IMK '%s'" % IMK)
        
        PSN = "00"
        if "5F34" in self.tags_dict.keys(): PSN = toHexString(self.tags_dict["5F34"]).replace(' ', '')
        UDK_AC = CardCrypto.DeriveUDK(IMK, PAN, PSN)
        self.audit.write("derived UDK_AC '%s' from PAN '%s' and PSN '%s'" % (UDK_AC, PAN, PSN))
        
        AIP = toHexString(self.tags_dict["82"]).replace(' ', '')
        ATC = toHexString(self.tags_dict["9F36"]).replace(' ', '')
        IAD = toHexString(self.tags_dict["9F10"]).replace(' ', '')
        card_ARQC = toHexString(self.tags_dict["9F26"]).replace(' ', '')
        self.ARQC = card_ARQC
        self.lastCVN = IAD [2:4]
        
        
        if IAD [2:4] == "10":
            computed_ARQC = CardCrypto.ComputeARQC_MCHIP4(self.CDOL1, AIP, ATC, IAD, UDK_AC)
            self.audit.write("computed ARQC '%s' for MasterCard card" % (computed_ARQC))
            
            
            if computed_ARQC == card_ARQC:
                self.audit.write("ARQC matched")
            else:
                self.audit.write("ARQC mismatch, card returned '%s' - exiting" % card_ARQC)
                self.ExitProgram()
                
            self.audit.write("")
            ARPC_ResponseCode = "031A"
            self.ARC = "3030"
            self.ARPC = CardCrypto.ComputeARPC(computed_ARQC, ARPC_ResponseCode, UDK_AC)
            self.tags_dict["8A"] = toBytes(self.ARC)
            self.tags_dict["91"] = toBytes(self.ARPC + ARPC_ResponseCode)
            self.audit.write("computed ARPC '%s' using ARPC response code '%s'" % (self.ARPC, ARPC_ResponseCode))
            self.audit.write("")
                
        else:
            self.audit.write("found unsupported CVN '%s' in IAD '%s' - exiting" % (IAD [2:4], IAD))
            self.ExitProgram()
        
        return
    
    
    def ValidateCrypto_DPAS(self, PAN):
        
        IMK = "11111111111111112222222222222222"
        self.audit.write("using IMK '%s'" % IMK)
        
        PSN = "00"
        if "5F34" in self.tags_dict.keys(): PSN = toHexString(self.tags_dict["5F34"]).replace(' ', '')
        UDK_AC = CardCrypto.DeriveUDK(IMK, PAN, PSN)
        self.audit.write("derived UDK_AC '%s' from PAN '%s' and PSN '%s'" % (UDK_AC, PAN, PSN))
        
        AIP = toHexString(self.tags_dict["82"]).replace(' ', '')
        ATC = toHexString(self.tags_dict["9F36"]).replace(' ', '')
        IAD = toHexString(self.tags_dict["9F10"]).replace(' ', '')
        card_ARQC = toHexString(self.tags_dict["9F26"]).replace(' ', '')
        self.ARQC = card_ARQC
        self.lastCVN = IAD [2:4]
        
        if IAD[2:4] in ["05", "06"]:
            computed_ARQC, SDK = CardCrypto.ComputeARQC_DPAS(self.CDOL1, AIP, ATC, IAD, UDK_AC)
            self.audit.write("computed ARQC '%s' for DPAS CVN %s card" % (computed_ARQC, IAD[2:4]))
            
            
            if computed_ARQC == card_ARQC:
                self.audit.write("ARQC matched")
            else:
                self.audit.write("ARQC mismatch, card returned '%s' - exiting" % card_ARQC)
                self.ExitProgram()
                
            self.audit.write("")
            ARPC_ResponseCode = "031A"
            self.ARC = "3030"
            self.ARPC = CardCrypto.ComputeARPC(computed_ARQC, ARPC_ResponseCode, SDK)
            self.tags_dict["8A"] = toBytes(self.ARC)
            self.tags_dict["91"] = toBytes(self.ARPC + ARPC_ResponseCode)
            self.audit.write("computed ARPC '%s' using ARPC response code '%s'" % (self.ARPC, ARPC_ResponseCode))
            self.audit.write("")
            
            
            
        else:
            self.audit.write("found unsupported CVN '%s' in IAD '%s' - exiting" % (IAD [2:4], IAD))
            self.ExitProgram()
        
        return
    
    def ComputeMAC(self, CMD):
        
        ATC = toHexString(self.tags_dict["9F36"]).replace(' ', '')
        bMC_SKD = False
        
        if self.PAN[0] == "4":
            IMK = "11220044556677881122330055667788" #Visa
        elif self.PAN[0] == "5":
            bMC_SKD = True
            IMK = "4664942FE615FB02E5D57F292AA2B3B6" #MasterCard
        elif self.PAN[0:3] == "679":
            bMC_SKD = True
            IMK = "4664942FE615FB02E5D57F292AA2B3B6" #Maestro
        elif self.PAN[0:2] in ["36", "65"]:
            IMK = "33333333333333334444444444444444" #DPAS
        else:
            self.audit.write("No IMK for PAN '%s' - exiting" % self.PAN)
            self.ExitProgram()
        
        
        PSN = "00"
        if "5F34" in self.tags_dict.keys(): PSN = toHexString(self.tags_dict["5F34"]).replace(' ', '')
        UDK_SMI = CardCrypto.DeriveUDK(IMK, self.PAN, PSN)

        MAC = CardCrypto.ComputeMAC(CMD, self.ARQC, ATC, UDK_SMI, bMC_SKD)



        return MAC
    
    
    
    
    
    
    
    
    