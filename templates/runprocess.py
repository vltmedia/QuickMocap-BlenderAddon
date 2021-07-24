import subprocess


def TestProcess():
    textexe = "C:/Users/Justin Jaro/source/repos/DebugProcess/DebugProcess/bin/Release/DebugProcess.exe"


    args = [textexe, 'Check 1', 'Cheeeeck 2', "THREE"]
    subprocess.run(args) 

def OpenUSDFile(filepath):
    args = ["cmd.exe", "/c","usdview", filepath ]
    subprocess.run(args) 
if __name__ == '__main__':
    OpenUSDFile("C:/temp/usd/BuildingB_Window_Cartoon2.usda")