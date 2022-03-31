import subprocess
def runJavaCode(data,key):
    val = str(subprocess.check_output("java call "+data+" "+key))

    return val[2:len(val)-5]
    
    # print(str(subprocess.check_output("dir",shell=True))[2:])
# runJavaCode("vdsvsdv","MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDXOsNnHqH+gHozdSZIFgx2EDvEqNB/6dGHKzK5S4+aJtjtIeVWRlsMuq4Hle3hngPEBPFMrr7tgqRivPg9qm0XOO0niMphlxzZL3p49hZB3IDt0NC+O/4uiRYF6fU+SmTYGCwRFMAMutLrHCiRfFahRMBy7g1UWm0GHsh+uRKg9QIDAQAB")