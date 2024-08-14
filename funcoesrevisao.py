# Variável para marcar uma alteração na agenda
agenda = []
alterada = False

# Função para solicitar o nome do contato ao usuário, com opção de valor padrão
def pede_nome(padrao=""):
    nome = input("Nome: ")
    if nome == "":
        nome = padrao
    return nome

# Função para solicitar o telefone do contato ao usuário, com opção de valor padrão
def pede_telefone(padrao=""):
    telefone = input("Telefone: ")
    if telefone == "":
        telefone = padrao
    return telefone

# Função para solicitar o endereço do contato ao usuário, com opção de valor padrão
def pede_endereco(padrao=""):
    endereco = input("Endereço: ")
    if endereco == "":
        endereco = padrao
    return endereco

# Função para solicitar a cidade do contato ao usuário, com opção de valor padrão
def pede_cidade(padrao=""):
    cidade = input("Cidade: ")
    if cidade == "":
        cidade = padrao
    return cidade

# Função para solicitar a UF do contato ao usuário, com opção de valor padrão
def pede_uf(padrao=""):
    uf = input("UF: ")
    if uf == "":
        uf = padrao
    return uf

# Função para exibir os dados de um contato
def mostra_dados(nome, telefone, endereco, cidade, uf):
    print(f"Nome: {nome} | Telefone: {telefone} | Endereço: {endereco} | Cidade: {cidade} | UF: {uf}")

# Função para solicitar o nome do arquivo ao usuário
def pede_nome_arquivo():
    return input("Nome do arquivo: ")

# Função para pesquisar um contato pelo nome na agenda
def pesquisa(nome):
    mnome = nome.lower()
    for p, e in enumerate(agenda):
        if e[0].lower() == mnome:
            return p
    return None

# Função para verificar se um nome já existe na agenda
def nome_existe(nome):
    for contato in agenda:
        if contato[0].lower() == nome.lower():
            return True
    return False

# Função para adicionar um novo contato na agenda
def novo():
    global agenda, alterada
    nome = pede_nome()
    if nome_existe(nome):
        print("Erro: Este nome já está na agenda.")
        return
    telefone = pede_telefone()
    endereco = pede_endereco()
    cidade = pede_cidade()
    uf = pede_uf()
    agenda.append([nome, telefone, endereco, cidade, uf])
    alterada = True

# Função para confirmar uma operação (como apagar ou alterar um contato)
def confirma(operacao):
    while True:
        opcao = input(f"Confirma {operacao} (S/N)? ").upper()
        if opcao in "SN":
            return opcao
        else:
            print("Resposta inválida. Escolha S ou N.")

# Função para apagar um contato da agenda
def apaga():
    global agenda, alterada
    nome = pede_nome()
    p = pesquisa(nome)
    if p is not None:
        if confirma("apagamento") == "S":
            del agenda[p]
            alterada = True
    else:
        print("Nome não encontrado.")

# Função para alterar os dados de um contato existente
def altera():
    global alterada
    p = pesquisa(pede_nome())
    if p is not None:
        nome, telefone, endereco, cidade, uf = agenda[p]
        print("Encontrado:")
        mostra_dados(nome, telefone, endereco, cidade, uf)
        nome = pede_nome(nome)  # Se nada for digitado, mantém o valor
        telefone = pede_telefone(telefone)
        endereco = pede_endereco(endereco)
        cidade = pede_cidade(cidade)
        uf = pede_uf(uf)
        if confirma("alteração") == "S":
            agenda[p] = [nome, telefone, endereco, cidade, uf]
            alterada = True
    else:
        print("Nome não encontrado.")

# Função para listar todos os contatos da agenda
def lista():
    print("\nAgenda\n------")
    for posicao, e in enumerate(agenda):
        print(f"Posição: {posicao} ", end="")
        mostra_dados(e[0], e[1], e[2], e[3], e[4])
    print("------\n")

# Função para ler a última agenda gravada
def le_ultima_agenda_gravada():
    ultima = ultima_agenda()
    if ultima is not None:
        leia_arquivo(ultima)

# Função para obter o nome do último arquivo de agenda gravado
def ultima_agenda():
    try:
        with open("ultima_agenda.dat", "r", encoding="utf-8") as arquivo:
            ultima = arquivo.readline().strip()
    except FileNotFoundError:
        return None
    return ultima

# Função para atualizar o nome do último arquivo de agenda gravado
def atualiza_ultima(nome):
    with open("ultima_agenda.dat", "w", encoding="utf-8") as arquivo:
        arquivo.write(f"{nome}\n")

# Função para ler os dados da agenda a partir de um arquivo
def leia_arquivo(nome_arquivo):
    global agenda, alterada
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        agenda = []
        for linha in arquivo.readlines():
            nome, telefone, endereco, cidade, uf = linha.strip().split("#")
            agenda.append([nome, telefone, endereco, cidade, uf])
    alterada = False

# Função para ler uma agenda do arquivo, com opção de salvar alterações pendentes
def le():
    global alterada
    if alterada:
        print("Você não salvou a lista desde a última alteração. Deseja gravá-la agora?")
        if confirma("gravação") == "S":
            grava()
    print("Ler\n---")
    nome_arquivo = pede_nome_arquivo()
    leia_arquivo(nome_arquivo)
    atualiza_ultima(nome_arquivo)

# Função para ordenar os contatos da agenda pelo nome
def ordena():
    global alterada
    agenda.sort()
    alterada = True

# Função para gravar os contatos da agenda em um arquivo
def grava():
    global alterada
    if not alterada:
        print("Você não alterou a lista. Deseja gravá-la mesmo assim?")
        if confirma("gravação") == "N":
            return
    print("Gravar\n------")
    nome_arquivo = pede_nome_arquivo()
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        for e in agenda:
            arquivo.write(f"{e[0]}#{e[1]}#{e[2]}#{e[3]}#{e[4]}\n")
    atualiza_ultima(nome_arquivo)
    alterada = False

# Função para validar a entrada de um número inteiro dentro de uma faixa
def valida_faixa_inteiro(pergunta, inicio, fim):
    while True:
        try:
            valor = int(input(pergunta))
            if inicio <= valor <= fim:
                return valor
        except ValueError:

            print(f"Valor inválido, favor digitar entre {inicio} e {fim}")

# Função para exibir o menu e retornar a opção escolhida pelo usuário
def menu():
    print("""
1 - Novo
2 - Altera
3 - Apaga
4 - Lista
5 - Grava
6 - Lê
7 - Ordena por nome
0 - Sai
""")
    print(f"\nNomes na agenda: {len(agenda)} | Alterada: {alterada}\n")
    return valida_faixa_inteiro("Escolha uma opção: ", 0, 7)

# Leitura da última agenda gravada ao iniciar o programa
le_ultima_agenda_gravada()

# Loop principal do programa, exibindo o menu e executando as funções conforme a escolha do usuário
while True:
    opcao = menu()
    if opcao == 0:
        break
    elif opcao == 1:
        novo()
    elif opcao == 2:
        altera()
    elif opcao == 3:
        apaga()
    elif opcao == 4:
        lista()
    elif opcao == 5:
        grava()
    elif opcao == 6:
        le()
    elif opcao == 7:
        ordena()