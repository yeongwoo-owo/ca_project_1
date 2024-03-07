class Instruction:
    deciData=[]
    binaryData=""
    hexaData=""
    asemData=" "
    nInst=0

    def __init__(self, deci, n):
        self.deciData=deci
        self.nInst=n

    def getHexaData(self):
        for i in self.deciData:
            if i//16<10:
                self.hexaData+=str(i//16)
            else:
                self.hexaData+=str(chr((i//16)-10+ord('a')))
            
            if i%16<10:
                self.hexaData+=str(i%16)
            else:
                self.hexaData+=str(chr((i%16)-10+ord('a')))

    def getBinaryData(self):
        for i in self.hexaData:
            temp=0
            if i>='0' and i<='9':
                temp=ord(i)-ord('0')
            else:
                temp=ord(i)-ord('a')+10

            digit=8
            for j in range(4):
                self.binaryData+=str(temp//digit)
                temp%=digit
                digit//=2

    def getDecimal(self, string):
        num=0
        for i in string:
            num*=2
            num+=int(i)
        return str(num)

    def getUnsignedDecimal(self, string):
        comp1=""
        for i in string:
            if i=='0':
                comp1+='1'
            else:
                comp1+='0'

        comp2=int(self.getDecimal(comp1))+1

        return "-"+str(comp2)

    def getOpcode(self):
        return self.binaryData[0:6]

    def getRS(self):
        return self.getDecimal(self.binaryData[6:11])

    def getRT(self):
        return self.getDecimal(self.binaryData[11:16])
    
    def getRD(self):
        return self.getDecimal(self.binaryData[16:21])
    
    def getSA(self):
        return self.getDecimal(self.binaryData[21:26])
    
    def getFuncT(self):
        return self.binaryData[26:]

    def getOffset(self):
        if self.binaryData[16]=='0':
            return self.getDecimal(self.binaryData[17:])
        else:
            return self.getUnsignedDecimal(self.binaryData[17:])


    def getTarget(self):
        return self.getDecimal(self.binaryData[6:])

    def getAsemData(self):
        opcode=self.getOpcode()
        RS=self.getRS()
        RT=self.getRT()
        RD=self.getRD()
        SA=self.getSA()
        offset=self.getOffset()
        if opcode=="000000":                    #R-Format
            functype=self.getFuncT()
            if functype=="100000":
                self.asemData+="add $"+RD+", $"+RS+", $"+RT
            elif functype=="100001":
                self.asemData+="addu $"+RD+", $"+RS+", $"+RT
            elif functype=="100100":
                self.asemData+="and $"+RD+", $"+RS+", $"+RT
            elif functype=="011010":
                self.asemData+="div $"+RS+", $"+RT
            elif functype=="011011":
                self.asemData+="divu $"+RS+", $"+RT
            elif functype=="001001":
                self.asemData+="jalr $"+RD+", $"+RS
            elif functype=="001000":
                self.asemData+="jr $"+RS
            elif functype=="010000":
                self.asemData+="mfhi $"+RD
            elif functype=="010010":
                self.asemData+="mflo $"+RD
            elif functype=="010001":
                self.asemData+="mthi $"+RS
            elif functype=="010011":
                self.asemData+="mtlo $"+RS
            elif functype=="011000":
                self.asemData+="mult $"+RS+", $"+RT
            elif functype=="011001":
                self.asemData+="multu $"+RS+", $"+RT
            elif functype=="100111":
                self.asemData+="nor $"+RD+", $"+RS+", $"+RT
            elif functype=="100101":
                self.asemData+="or $"+RD+", $"+RS+", $"+RT
            elif functype=="000000":
                self.asemData+="sll $"+RD+", $"+RT+", "+SA
            elif functype=="000100":
                self.asemData+="sllv $"+RD+", $"+RT+", $"+RS
            elif functype=="101010":
                self.asemData+="slt $"+RD+", $"+RS+", $"+RT
            elif functype=="101011":
                self.asemData+="sltu $"+RD+", $"+RS+", $"+RT
            elif functype=="000011":
                self.asemData+="sra $"+RD+", $"+RT+", "+SA
            elif functype=="000111":
                self.asemData+="srav $"+RD+", $"+RT+", $"+RS
            elif functype=="000010":
                self.asemData+="srl $"+RD+", $"+RT+", "+SA
            elif functype=="000110":
                self.asemData+="srlv $"+RD+", $"+RT+", $"+RS
            elif functype=="100010":
                self.asemData+="sub $"+RD+", $"+RS+", $"+RT
            elif functype=="100011":
                self.asemData+="subu $"+RD+", $"+RS+", $"+RT
            elif functype=="001100":
                self.asemData+="syscall"
            elif functype=="100110":
                self.asemData+="xor $"+RD+", $"+RS+", $"+RT
            else:
                self.asemData+="unknown instruction"
        
        elif opcode=="000010":                #F-Format
            self.asemData+="j "+self.getTarget()
        elif opcode=="000011":
            self.asemData+="jal "+self.getTarget()

        elif opcode=="001000":
            self.asemData+="addi $"+RT+", $"+RS+", "+offset
        elif opcode=="001001":
            self.asemData+="addiu $"+RT+", $"+RS+", "+offset
        elif opcode=="001100":
            self.asemData+="andi $"+RT+", $"+RS+", "+offset
        elif opcode=="000100":
            self.asemData+="beq $"+RS+", $"+RT+", "+offset
        elif opcode=="000101":
            self.asemData+="bne $"+RS+", $"+RT+", "+offset
        elif opcode=="100000":
            self.asemData+="lb $"+RT+", "+offset+"($"+RS+")"
        elif opcode=="100100":
            self.asemData+="lbu $"+RT+", "+offset+"($"+RS+")"            
        elif opcode=="100001":
            self.asemData+="lh $"+RT+", "+offset+"($"+RS+")"
        elif opcode=="100101":
            self.asemData+="lhu $"+RT+", "+offset+"($"+RS+")"
        elif opcode=="001111":
            self.asemData+="lui $"+RT+", "+offset
        elif opcode=="100011":
            self.asemData+="lw $"+RT+", "+offset+"($"+RS+")"
        elif opcode=="001101":
            self.asemData+="ori $"+RT+", $"+RS+", "+offset
        elif opcode=="101000":
            self.asemData+="sb $"+RT+", "+offset+"($"+RS+")"
        elif opcode=="001010":
            self.asemData+="slti $"+RT+", $"+RS+", "+offset
        elif opcode=="001011":
            self.asemData+="sltiu $"+RT+", $"+RS+", "+offset
        elif opcode=="101001":
            self.asemData+="sh $"+RT+", "+offset+"($"+RS+")"
        elif opcode=="101011":
            self.asemData+="sw $"+RT+", "+offset+"($"+RS+")"
        elif opcode=="001110":
            self.asemData+="xori $"+RT+", $"+RS+", "+offset
        else:
            self.asemData+="unknown instruction"
        
    def printInst(self):
        self.getHexaData()
        self.getBinaryData()
        self.getAsemData()
        print("inst "+str(self.nInst)+": "+self.hexaData+self.asemData)

