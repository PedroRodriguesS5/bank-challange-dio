extrato = {"saques": {"valor_do_saque": 0, "qtd_saque": 0},
           "saldo": 20000,
           "depositos": {"valor_deposito": 0, "qtd_deposito": 0}}

menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair
"""


def realizar_deposito():
    valor_depositado = float(input("Digite o valor do depósito"))

    if valor_depositado <= 0:
        return "Digite um valor válido por favor"

    print("Valor depositádo com sucesso com sucesso")
    extrato["depositos"]["qtd_deposito"] += 1
    extrato["depositos"]["valor_deposito"] += valor_depositado


def saque():
    valor_saque = float(input("Digite o valor do saque: "))

    if valor_saque > extrato["saldo"]:
        return print("Saldo insuficiente")

    if extrato["saques"]["qtd_saque"] > 3:
        return print("Não pode ser realizado mais que três saques por dia!")

    print("Valor retirado com sucesso!")
    extrato["saques"]["qtd_saque"] += 1
    extrato["saques"]["valor_do_saque"] += valor_saque


def extract():
    print(extrato)


while True:
    option = input(menu)

    if option == '1':
        realizar_deposito()

    if option == '2':
        saque()

    if option == '3':
        extract()

    if option == '0':
        print("Obrigado pela preferência")
        break
