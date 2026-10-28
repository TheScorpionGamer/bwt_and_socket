print("BURROWS WHEELER TRANSFORM")

bwt_phrase = input("Inserisci la frase da trasformare: ") + "$"

bwt_versions = []

for i in range(len(bwt_phrase)):
    bwt_versions.append(bwt_phrase[i:] + bwt_phrase[:i])

print("\nRotazioni:")

for version in bwt_versions:
    print(version)


# Confronta alfabeticamente due stringhe
def viene_prima(version, version2):
    c = 0

    while c < len(version):

        if version[c] < version2[c]:
            return True

        elif version[c] > version2[c]:
            return False

        else:
            c += 1

    return False


# Ordinamento manuale
bwt_order = bwt_versions

for i in range(len(bwt_order)):

    minimo = i

    for j in range(i + 1, len(bwt_order)):

        if viene_prima(bwt_order[j], bwt_order[minimo]):
            minimo = j

    tmp = bwt_order[i]
    bwt_order[i] = bwt_order[minimo]
    bwt_order[minimo] = tmp


print("\nRotazioni ordinate:")

for version in bwt_order:
    print(version)


# Ultima colonna
bwt_result = ""

for version in bwt_order:
    bwt_result += version[-1]


print(f"\nRisultato della Burrows Wheeler Transform: {bwt_result}")