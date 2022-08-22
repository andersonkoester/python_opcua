import os
from time import sleep
from opcua import Client, ua

servers = ["10.0.8.14", "10.0.8.20"]

def clear_screen():
  os.system('cls' if os.name == 'nt' else 'clear')
  print("================ OPC UA CONNECTION ================")

def opc_menus(node = None):
  clear_screen()
  print("--- SERVER [{}] ---".format(selected_server))
  print("--- NODE [{}] ---".format(node.get_path()[-1]))
  node_children = node.get_children();
  if len(node_children) > 0:
    global last_parent
    last_parent = node
    for idx, item in enumerate(node_children):
      print("OPT[{}] ==> ".format(idx), item.get_browse_name().to_string())

    index_opt = int(input("Selecione a opção (-1: Sair): "))
    try:
      if index_opt >= 0:
        selected_node = node_children[index_opt]
        opc_menus(selected_node)
      else:
        try:
          opc_menus(node.get_parent())
        except:
          print("--- DESCONECTANDO ---")
    except:
      print("OPÇÃO NÃO EXISTE, LEVE ISTO A SÉRIO")
      sleep(3)
      opc_menus(node)
  else:
    print("VALOR DO NODE: {}".format(node.get_value()))
    parent = last_parent if node.get_parent() == None else node.get_parent()
    input("\n\nPressione qualquer tecla para voltar")
    opc_menus(parent)

def connect_opcua():
  client = Client("opc.tcp://{}:4840".format(selected_server))
  try:
    client.connect()

    root = client.get_root_node()
    opc_menus(root)
  finally:
    client.disconnect()

def main_menu():
  global selected_server
  clear_screen()
  for idx, server in enumerate(servers):
    print("SRV[{}] ==> ".format(idx),server)

  index_srv = int(input("Selecione o servidor (-1: Sair): "))

  try:
    if index_srv >= 0:
      selected_server = servers[index_srv]
      connect_opcua()
      sleep(3)
      main_menu()
  except:
    print("\nSERVIDOR NÃO EXISTE, LEVE ISTO A SERIO")
    sleep(3)
    main_menu()

if __name__ == "__main__":
  main_menu()