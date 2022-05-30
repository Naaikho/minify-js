import string

def minify(src:str):
    src = list(src)
    i = 0
    inBracket = False
    inDBracket = False
    multiLine = False
    IGNORED = list(string.ascii_letters + string.digits + "_$")

    while(i<len(src)):
        if(multiLine):
            if(src[i] == "*" and src[i+1] == "/"):
                multiLine = False
                src[i+1] = " "
            src[i] = ""
            i+=1
            continue

        if(src[i] in "\"" and src[i-1] != "\\" and not inBracket):
            inDBracket = not inDBracket
            i+=1
            continue

        if(src[i] in "\'" and src[i-1] != "\\" and not inDBracket):
            inBracket = not inBracket
            i+=1
            continue

        if(inDBracket or inBracket):
            i+=1
            continue

        if(src[i] == "/" and src[i+1] == "*"):
            multiLine = True
            continue

        if(src[i] == "/" and src[i+1] == "/"):
            while(src[i] != "\n"):
                src[i] = ""
                i+=1
            continue


        # --------------------------------------------------- #

        if(src[i] in "}]):\"'" and src[i+1] in "\n\t\r"):
            if(src[i+1] in "\n\t\r"):
                i+=1
                while i < len(src)-1 and src[i] in "\n\t\r":
                    src[i] = ""
                    i+=1
                if(src[i] not in "}]):\"'"):
                    src[i-1] += ";"
            # print(src[i])

        if(src[i] in "+-" and src[i+1] in "+-"):
            if(src[i+2] not in IGNORED):
                src[i+1] += ")"
                l=i
                while l > 0 and src[l-1] in IGNORED:
                    l -= 1
                src[l] = "(" + src[l]
            elif(src[i-1] not in IGNORED):
                src[i] = "(" + src[i]
                i+=1
                l=i
                while l < len(src) and src[l+1] in IGNORED:
                    l += 1
                src[l] += ")"

        if(src[i] in "\n\t\r"):
            while(src[i] in "\n\t\r"):
                src[i] = ""
                i+=1

        if(src[i] == " " and (src[i-1] not in IGNORED or src[i+1] not in IGNORED)):
            src[i] = ""

        i+=1
    return "".join(src)





if __name__ == "__main__":

    import os, sys

    def path(src:str, *arg):
        for p in arg:
            src += os.path.sep + p
        return src

    GLOBAL_PATH = sys.path[0]
    IMPORT_PATH = path(GLOBAL_PATH, "import_js")
    EXPORT_PATH = path(GLOBAL_PATH, "export_js")

    files = os.listdir(IMPORT_PATH)
    if(files != []):
        for f in files:
            jsLine = open(path(IMPORT_PATH, f), "r").readlines()
            jsFile = ""
            for line in jsLine:
                jsFile += line
            tmpRes = minify(jsFile)
            with open(path(EXPORT_PATH, "min."+f), "w") as data:
                data.write(tmpRes)

