from datetime import datetime
from abc import ABC, abstractmethod
import textwrap

class Conta:
    def __init__(self, numero, cliente) -> None:
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self) -> float:
        return self._saldo
    
    @property
    def numero(self)-> int:
        return self._numero
    
    @property
    def agencia(self)-> int:
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_cnta(cls, cliente, numero):
        return cls(numero, cliente)
    
    def sacar(self, valor):
        if self._saldo < valor:
             print("Saldo insuficiente")
             return False
        elif valor < 0:
             print("Por favor insira um valor válido para saque!")
             return False

        self._saldo -= valor
        print("Saque efetuado com sucesso")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Por favor insira um valor válido")
        
        
        self._saldo += valor
        print("Depóstio realizado com sucesso.")
        return True


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)


    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente): 
    def __init__(self, endereco, nome, data_nascimento, cpf):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3) -> None:
        super().__init__( numero, cliente)
        self._limite = limite
        self._limite_saques= limite_saques

    def sacar_valor(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques > self._limite_saques

        if excedeu_limite: 
            print("Limite insuficiente!")
        elif excedeu_saques:
            print("Limite se saques atingidos no dia")
        else:
            return super().sacar(valor)
        
    def __str__(self) -> str:
        return f"""\
            Agência:\t {self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}"""
    
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo" : transacao.__class__.__name__,
            "valor": transacao.valor,
        })

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_realizada = conta.sacar(self.valor)

        if transacao_realizada:
            conta.historico.adcionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_realizada = conta.depositar(self.valor)

        if transacao_realizada:
            conta.historico.adicionar_transacao(self)
    

def menu():
    menu = """
        [1] \tDepositar
        [2] \tSacar
        [3] \tExtrato
        [4] \tCriar Usuário
        [5] \tCriar Conta
        [6] \tListar contas
        [0] \tSair
        """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    cliente_filtrado = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_filtrado[0] if cliente_filtrado else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui nenhuma conta cadastrada!")
        return
    # FIXME: não permite o cliente escolher uma conta
    return cliente.contas[0]

def operacao(clientes, tipo_transacao):
    cpf = input("Informe seu cpf: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = tipo_transacao(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe seu cpf: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n========== EXTRATO ==========")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram encontradas nenhuma movimentação"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("===================================")

def criar_cliente(clientes):
    cpf = input("Informe seu cpf: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Cpf já existe!")
        return
    
    nome = input("Informe o nome completo!")
    data_nascimento = input("Informe a data de nascimento(dd-mm-aaaa): ")

    endereco = input("Informe seu endereço (logradouro, nro, bairro, cidade/UF): ")
    cliente = PessoaFisica(nome=nome, data_nascimento= data_nascimento, endereco= endereco, cpf = cpf)

    clientes.append(cliente)

    print("Cliente cadastrado com sucesso!")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe seu cpf: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado, fluxo de criação de conta encerrado!")
        return
    conta = ContaCorrente.nova_cnta(cliente=cliente, numero= numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n Conta criada com suecsso!")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            operacao(clientes, Deposito)
        elif opcao == "2":
            operacao(clientes, Saque)
        elif opcao == "3":
            exibir_extrato(clientes)
        elif opcao == "4":
            criar_cliente(clientes)
        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "6":
            listar_contas(contas)
        elif opcao == "7":
            break
        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

main()
