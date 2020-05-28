import re

'''
可根据自定义的base64表，来编解码
'''

def base64_encode(s, dictionary=None):
    if dictionary == None:
        dictionary = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    r = ""
    p = ""
    c = len(s) % 3

    if (c > 0):
        for i in range(c, 3):
            p += '='
            s += "\0"

    for c in range(0, len(s), 3):
        n = (ord(s[c]) << 16) + (ord(s[c+1]) << 8) + (ord(s[c+2]))
        n = [(n >> 18) & 0x3F, (n >> 12) & 0x3F, (n >> 6) & 0x3F, n & 0x3F]
        r += dictionary[n[0]] + dictionary[n[1]] + dictionary[n[2]] + dictionary[n[3]]
    return r[0:len(r) - len(p)]  + p

def base64_decode(s, dictionary=None):
    if dictionary == None:
        dictionary = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    base64inv = {}
    for i in range(len(dictionary)):
        base64inv[dictionary[i]] = i

    s = s.replace("\n", "")
    if not re.match(r"^([{alphabet}]{{4}})*([{alphabet}]{{3}}=|[{alphabet}]{{2}}==)?$".format(alphabet = dictionary), s):
        raise ValueError("Invalid input: {}".format(s))

    if len(s) == 0:
        return ""
    p = "" if (s[-1] != "=") else "AA" if (len(s) > 1 and s[-2] == "=") else "A"
    r = ""
    s = s[0:len(s) - len(p)] + p
    for c in range(0, len(s), 4):
        n = (base64inv[s[c]] << 18) + (base64inv[s[c+1]] << 12) + (base64inv[s[c+2]] << 6) + base64inv[s[c+3]]
        r += chr((n >> 16) & 255) + chr((n >> 8) & 255) + chr(n & 255)
    return r[0:len(r) - len(p)]


def decodeText_From_KownTeam(crp,know_text,kown_crp):
    temp_dict = {}
    old_kown_crp = base64_encode(know_text)
    old_crp = list('*'*len(crp))
    for i in range(0, len(kown_crp)):
        # print('{}==>{}'.format(old_kown_crp[i], kown_crp[i]))
        temp_dict[kown_crp[i]] = old_kown_crp[i]
    for j in range(0, len(crp)):
        if crp[j] in temp_dict.keys():
            print('{}==>{}'.format(crp[j], temp_dict[crp[j]]))
            old_crp[j] = temp_dict[crp[j]]
        else:
            print('{}==>{}'.format(crp[j],'*'))
            pass
    old_crp = ''.join(old_crp)
    print(temp_dict)
    print(old_crp)
    # print(base64_decode(old_crp))


crp = "uLdAuO8duojAFLEKjIgdpfGeZoELjJp9kSieuIsAjJ/LpSXDuCGduouz"
know_text = "ashlkj!@sj1223%^&*Sd4564sd879s5d12f231a46qwjkd12J;DJjl;LjL;KJ8729128713"
kown_crp = "pTjMwJ9WiQHfvC+eFCFKTBpWQtmgjopgqtmPjfKfjSmdFLpeFf/Aj2ud3tN7u2+enC9+nLN8kgdWo29ZnCrOFCDdFCrOFoF="
decodeText_From_KownTeam(crp,know_text,kown_crp)


# dictionary =  "XYZFGHI2+/Jhi345jklmEnopuvwqrABCDKL6789abMNWcdefgstOPQRSTUVxyz01"
# print(base64_decode("nRKKAHzMrQzaqQzKpPHClX==", dictionary))