def sacar():
    saldo = 500
    saque = 550
    status = "Sucesso" if saldo >= saque else "Erro"
    print(f"{status} ao realizar o saque")
    # if saldo >= valor:
    #     print("valor foi retirado com sucesso")
    # elif saldo <= valor:
    #     print("saldo insuficiente")


# saque = float(input("Por favor insira o vlaor que deseja retirar: "))
sacar()
