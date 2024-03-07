import sys
import instruction

if __name__=='__main__':
    filePath=sys.argv[1]

    if len(sys.argv)!=2:
        print("Input Error\n")
        sys.exit()

    inputFile=open(filePath, 'rb')
    data=inputFile.read()
    inputFile.close()

    nInst=0
    deciData=[]

    for i in data:
        deciData.append(i)
        if(len(deciData)==4):
            inst=instruction.Instruction(deciData, nInst)
            inst.printInst()
            deciData.clear()
            nInst+=1
