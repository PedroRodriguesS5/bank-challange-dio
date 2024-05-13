palavra = "50"
VOGAIS = "AEIOU"

for letra in palavra:
    if letra.upper() in VOGAIS:
        print(letra, end="")

print()

# for com built-in-range
for numero in range(0, 51, 5):
    print(numero, end=" ")


for numero in range(50000):
    if numero == int(palavra):
            break
    print(numero)