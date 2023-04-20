def ProcessModules(filepath):
    Modules = []
    Instances=[]
    with open(filepath, "r") as fp:
        lines = fp.readlines()
        instInModule = []
        for i in range(len(lines)):
            if not (lines[i].startswith("//") or len(lines[i].rstrip()) == 0):
                line = lines[i].strip()
                if not (line.startswith("input") or line.startswith("output") or line.startswith("wire") ):
                    # print(line)
                    if line.startswith("module"):
                        # instInModule = []
                        moudleLine = line.split(" ")
                        Modules.append(moudleLine[1])
                    elif not line.startswith("endmodule"):
                            inst = line.split(" ")
                            if len(inst) != 0:
                                instInModule.append(inst[0])
                    else:
                        if len(instInModule) != 0:
                            Instances.append(instInModule)
                            instInModule=[]
    fp.close()
    return Instances,Modules

def InstancesInHierarchy(Instances,Modules):
    PrimitiveModules = {}
    ModulePairs = {}
    while 1:
        Flag = 0
        for i in range(len(Instances)):
            if len(set(Instances[i]) & set(Modules)) == 0:
                PrimitiveModules[Modules[i]] = Instances[i]
                # Flag = 1
            else:
                Flag = 1
        for i in range(len(Instances)):
            index = []
            for j in range(len(Instances[i])):
                if Instances[i][j] in PrimitiveModules:
                    Instances[i].extend(PrimitiveModules[Instances[i][j]])
                    index.append(j)
            Instances[i]=Instances[i][len(index):]
        if Flag == 0:
            break
    for i in range(len(Instances)):
        count = {}
        for j in range(len(Instances[i])):
            comp = Instances[i][j]
            if comp not in count:
                count[comp] = 1
            else:
                count[comp] = count[comp] + 1
        ModulePairs[Modules[i]] = count
    return ModulePairs

def ShowNum(ModulePairs):
    for key in ModulePairs:
        print("Counting all of the instances in " + key + " hierarchy:")
        for subkey in ModulePairs[key]:
            print(f"{subkey:<15}: {ModulePairs[key][subkey]} placements")
        print("\n")


