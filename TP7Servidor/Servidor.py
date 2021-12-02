import socket, pickle, psutil, time, os, nmap,platform,subprocess
from tabulate import tabulate
from datetime import datetime
import time

def retorna_codigo_ping(hostname):
  """Usa o utilitario ping do sistema operacional para encontrar   o host. ('-c 5') indica, em sistemas linux, que deve mandar 5   pacotes. ('-W 3') indica, em sistemas linux, que deve esperar 3   milisegundos por uma resposta. Esta funcao retorna o codigo de   resposta do ping """

  plataforma = platform.system()
  args = []
  if plataforma == "Windows":
    args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]

  else:
    args = ['ping', '-c', '1', '-W', '1', hostname]
    
  ret_cod = subprocess.call(args,
    stdout=open(os.devnull, 'w'),
    stderr=open(os.devnull, 'w'))
  return ret_cod
def verifica_hosts(base_ip):
  print("Carregando...")
  host_validos = []
  return_codes = dict()
  for i in range(1, 255):
    return_codes[base_ip + '{0}'.format(i)] =   retorna_codigo_ping(base_ip + '{0}'.format(i))
    if i %20 ==0:
      print(".", end = "")
    if return_codes[base_ip + '{0}'.format(i)] == 0:
      host_validos.append(base_ip + '{0}'.format(i))

  return host_validos
def obter_hostnames(host_validos):
  nm = nmap.PortScanner()
  for i in host_validos:
    try:
      nm.scan(i)
    except:
      pass
def scan_host(host):
  nm = nmap.PortScanner()
  nm.scan(host)
  print(nm[host].hostname())
  for proto in nm[host].all_protocols():
    print('----------')
    print('Protocolo : %s' % proto)

    lport = nm[host][proto].keys()
    #lport.sort()
    for port in lport:
      print ('Porta: %s\t Estado: %s' % (port, nm[host][proto][port]['state']))
def enviar_TP4():
  lista = os.listdir()
  dic = {}
  for i in lista:
    if os.path.isfile(i):
      dic[i] = []
      dic[i].append(os.stat(i).st_size)
      dic[i].append(os.stat(i).st_atime)
      dic[i].append(os.stat(i).st_mtime)
  tabela = [["Nome", "Tamanho", "Data criação", "Data modificação", "Tipo"]]
  for arq in dic:
    linha = [arq]
    linha.append(dic[arq][0])
    linha.append(time.ctime(dic[arq][1]))
    linha.append(time.ctime(dic[arq][2]))
    linha.append(os.path.splitext(arq)[1])
    tabela.append(linha)  
  listaPid = psutil.pids()
  tabelaPid = [["Pid", "Nome do executável", "CPU", "Memória"]]
  for pidIndex in range(1,9):
    pid = listaPid[pidIndex]
    dicProcesso = [pid, psutil.Process(pid).exe(),str(psutil.Process(pid).cpu_percent()*100) + '%',str(round(psutil.Process(pid).memory_percent()*100)) + '%']
    tabelaPid.append(dicProcesso)
  return [tabulate(tabela, headers='firstrow'), tabulate(tabelaPid, headers='firstrow')]
def enviar_TP5():
  instanteInicial = datetime.now()
  enviar_TP4()
  enviar_TP7()
  instanteFinal = datetime.now()
  return str(instanteFinal - instanteInicial)[8:11]+'ms'
def enviar_TP6():
  ip_string = '192.168.0.0'
  ip_lista = ip_string.split('.')
  base_ip = ".".join(ip_lista[0:3]) + '.'
  hosts_validos = verifica_hosts(base_ip)

  lista = []

  for host in hosts_validos:

    print(host)

    nm = nmap.PortScanner()

    info_host = {
      "endereco": host,
      "nome" : "",
      "portas" : []
    }
    try:
      nm.scan(host)
      info_host["nome"] = nm[host].hostname()
      for proto in nm[host].all_protocols():
        lport = nm[host][proto].keys()
        for port in lport:
          info_host["portas"].append({"numero":port,"estado":nm[host][proto][port]['state']})
    except:
      pass
    lista.append(info_host)

  return lista
def enviar_TP7():
  ip = psutil.net_if_addrs().get('Wi-Fi 2')[1].address
  gateway = ip[0:11]
  mascaradesubrede = psutil.net_if_addrs().get('Wi-Fi 2')[1].netmask
  rede = {
    "ip":ip,
    "gateway":gateway,
    "mascaradesubrede":mascaradesubrede
  }
  return rede
# Cria o socket
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname() # Nome do servidor
porta = 9999 # Porta do servidor
# Realiza o bind do IP e porta com o servidor
socket_servidor.bind((host, porta))
# Escutando...
socket_servidor.listen()
print("Servidor", host.upper(), "esperando conexão na porta", porta)
# Aceita a conexão do cliente
(socket_cliente, addr) = socket_servidor.accept()
print("Conectado a ", str(addr))
while True:
  msg = socket_cliente.recv(4096) # Recebe a mensagem do cliente
  if (msg.decode("UTF-8") == "1"):
    socket_cliente.send(pickle.dumps(enviar_TP4()))
  elif (msg.decode("UTF-8") == "2"):
    socket_cliente.send(pickle.dumps(enviar_TP5()))
  elif (msg.decode("UTF-8") == "3"):
    socket_cliente.send(pickle.dumps(enviar_TP6()))
  elif (msg.decode("UTF-8") == "4"):
    socket_cliente.send(pickle.dumps(enviar_TP7()))
  elif (msg.decode("UTF-8") == "5"):
    print("Términa da conexão")
    socket_cliente.close()
    break