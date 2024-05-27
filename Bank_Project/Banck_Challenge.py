menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Criar Usuário
[5] Criar Conta
[6] Listar contas
[0] Sair
"""

def realizar_deposito(saldo, valor_deposito, extract, /):
    if valor_deposito <= 0:
        return "Digite um valor válido por favor"

    print("Valor depositádo com sucesso com sucesso")
    extract += f"Depósito:\tR${valor_deposito:.2f}\n"
    print("Valor depósitado com suecsso")
    
    return saldo, extract

def saque(*, saldo, valor_saque, extract, limit, withdraw_count, withdraw_limit):
    excedeu_saldo = valor_saque > saldo
    excedeu_limite = valor_saque > limit
    excedeu_saque = withdraw_count > withdray_count

    if excedeu_saldo:
        print("Saldo insuficiente.")
    elif excedeu_limite:
        print("Limite indisponivel.")
    elif excedeu_saque:
        print("Limite de saques atingido.")

    saldo -= valor_saque
    extract += f"Saque:\t\tR$ {valor_saque:.2f}\n"
    withdraw_count += 1
    print("Saque realizado com sucesso!")

    return saldo, extract

def show_extract(saldo, /, *, extract):
    print("\n ================= Extrato =================")
    print("Não foram realizadas movimentações." if not extract else extract)
    print(f"\nSaldo:\t\tR$ {saldo:2f}")
    print("==================================")

def create_user(users):
    cpf = input("Informe o CPF (somente os números): ")
    user = filter_user(cpf, users)

    if user:
        print("\n CPF já cadastrado")
        return
    
    name = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-yyyy)")
    endereco = input("Informe o endeço (logradouro, nro, bairro, cidade/UF): ")

    users.append({"name": name, "data_nascimento": data_nascimento, "endereco": endereco, "cpf": cpf})
    print("Usuário criado com sucesso!!")

def create_account(agencia, account_number, users):
    cpf = input("Informe seu cpf: ")
    user = filter_user(cpf, users)

    if user:
        print("\n Conta criada com sucesso!")
        return {"agencia": agencia, "account_number": account_number, "user": user}

    print("Usuário não encotnrado, fluxo de criação de conta encerrado!")

def list_accounts(accounts):
    for conta in accounts:
        linha = f"""\
        Agência:\t{conta['agencia']}
        C/C:\t\t{conta['account_number']}
        Titular:\t{conta['user']['name']}
        """
        print("=" * 100)
        print(linha)

def filter_user(cpf, users):
    filter_users = [user for user in users if user["cpf"] == cpf]
    return filter_users[0] if filter_users else None

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 1000
    limite = 500
    extract = ""
    numero_saques = 0
    users = []
    accounts = []

    while True:
        option = input(menu)

        if option == '1':
            valor = float(input("Informe o valor do depósito: "))
            realizar_deposito(saldo, valor, extract)

        if option == '2':
            valor = float(input("Informe o valor do saque: "))
            saque(saldo =saldo, extract=extract, withdraw_count= numero_saques,limit=limite,
                   withdraw_limit=LIMITE_SAQUES)
            
        if option == '3':
            show_extract(saldo, extract= extract)

        if option == '4':
            create_user(users)

        if option == '5':
            account_number = len(accounts) + 1
            account = create_account(AGENCIA, account_number, users)

            if account:
                accounts.append(account)

        if option == '6':
            list_accounts(accounts)

        if option == '0':
            print("Obrigado pela preferência")
            break

main()