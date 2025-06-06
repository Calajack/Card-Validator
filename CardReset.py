from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes
from CardCommands import CardCommands
import time, sys



Known_AIDs = [
    ["Visa Credit/Debit", "A0000000250000"], 
    ["Visa Electron", "A0000000032010"],
    ["Visa V PAY", "A0000000032020"],
    ["MasterCard Credit/Debit", "A0000000041010"],
    ["Maestro", "A0000000043060"],
    ["Discover/Diners club", "A0000001523010"]
    ]

Terminal_Data = {}
Terminal_Data["9F02"] = "000000000001"
Terminal_Data["9F1A"] = "0840"
Terminal_Data["5F2A"] = "0840"
Terminal_Data["9F35"] = "22"
Terminal_Data["95"] = "0000008000"


class AuditClass():
    
    def write(self, msg):
        print msg

        

def ExitProgram(audit):
    audit.write("")
    audit.write("Press Enter to exit")
    raw_input()
    sys.exit()
    return


def ResetCard(auditTo = None, bExitMsg = True, nextFunction = None):

    audit = AuditClass()
    if auditTo != None:
        audit = auditTo
    

    cardtype = AnyCardType()
    
    cardrequest = CardRequest( timeout=5, cardType=cardtype )
    readers = cardrequest.getReaders()
    if len(readers) == 0:
        audit.write("Please connect a PC/SC smartcard reader, and try again")
        ExitProgram(audit)
    else:
        audit.write("Found PC/SC smartcard reader(s):")
        for r in readers: audit.write(" - " + str(r))
        audit.write("")
    
    try:        
        cardservice = cardrequest.waitforcard()
        cardservice.connection.connect()
    except:
        audit.write("")
        audit.write("No card found")
        audit.write("")
        audit.write("Please insert a chip card in one of the readers listed above, and try again")    
        ExitProgram(audit)
        
        
    
    
    cc = CardCommands(cardservice, Terminal_Data, audit, bExitMsg, nextFunction)
    
    
    "ATR"
    cc.printATR()
    
    "Application Selection"
    cc.SelectFromList(Known_AIDs)
        
    
    "Get Processing Options"
    cc.GetProcessingOptions()
    
    
    "Read records"
    cc.ReadRecords()
    
    
    "First Generate AC - ARQC"
    cc.FirstGenerateAC_ARQC()
    
    
    "Validate Cryptography"
    cc.cp.ValidateCryptography()
    
    
    "External authenticate"
    cc.ExternalAuthenticate()
    
    
    "Second Generate AC - TC"
    cc.SecondGenerateAC_TC()
    
    "Unblock PIN"
    cc.UnblockPIN()
    
    
    
    audit.write("")
    audit.write("Online transaction successful: counters and PIN are reset")
    

    cc.cp.ExitProgram()
    if bExitMsg == True:
        raw_input()
    

if __name__ == '__main__':
    ResetCard()
    