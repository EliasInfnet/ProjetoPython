import socket, sys, pickle

host = socket.gethostname() # Endereço do servidor
porta = 9999 # Porta do servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria o socket no cliente
try:
  s.connect((host, porta)) # Tenta conexão com o servidor
except Exception as erro:
  print(str(erro))
  sys.exit(1) # Termina o programa
_menuAberto = True

def mostrar_menu():
  print()
  print('------------------------------')
  print('1 - Informações do TP4 (Diretórios, arquivos, processos)')
  print('2 - Informações do TP5 (Shed, Time)')
  print('3 - Informações do TP6 (Subrede)')
  print('4 - Informações do TP7 (Interfaces de rede)')
  print('5 - Sair')
  print('------------------------------')
  print()

def carregar_opcao_um():
  print()
  s.send(_valorMenu.encode("UTF-8"))
  _retorno = pickle.loads(s.recv(4096))
  print(_retorno[0])
  print()
  print(_retorno[1])

def carregar_opcao_dois():
  print()
  s.send(_valorMenu.encode("UTF-8"))
  _retorno = pickle.loads(s.recv(4096))
  print(_retorno)

def carregar_opcao_tres():
  print()
  s.send(_valorMenu.encode("UTF-8"))
  _retorno = pickle.loads(s.recv(4096))
  for host in _retorno:
    print('--------------')
    print('Endereço: ', host["endereco"])
    print('Nome: ', host["nome"])
    print('Portas: ')
    for portas in host["portas"]:
      print('---------')
      print('  Número: ' + str(portas["numero"]))
      print('  Estado: ' + str(portas["estado"]))

def carregar_opcao_quatro():
  s.send(_valorMenu.encode("UTF-8"))
  _retorno = pickle.loads(s.recv(4096))
  print('IP : ',_retorno["ip"])
  print('Gateway : ',_retorno["gateway"])
  print('Máscara de Subrede : ',_retorno["mascaradesubrede"])

while _menuAberto:
  mostrar_menu()
  _valorMenu = input("Entre com a opção do menu: ")
  if(_valorMenu == '1'):
    carregar_opcao_um()
  elif(_valorMenu == '2'):
    carregar_opcao_dois()
  elif(_valorMenu == '3'):
    carregar_opcao_tres()
  elif(_valorMenu == '4'):
    carregar_opcao_quatro()
  elif(_valorMenu == '5'):
    s.send(_valorMenu.encode("UTF-8"))
    _menuAberto = False
  else:
    print('Entre com o uma opção válida !!')