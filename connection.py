import sys
import re

#sys.path.insert(0, "..")

from opcua import Client, ua

def normalize_name(name):
  return re.sub(r"\)", "", re.sub(r"\(", "", re.sub("QualifiedName", "", str(name))))

def recursive(children, node):
  for item in children:
    name = node, item.get_browse_name()
    if len(item.get_children()) > 0:
      recursive(item.get_children(), name)
    else:
      try:
        print(item.get_path())
      except:
        None

if __name__ == "__main__":

    client = Client("opc.tcp://10.0.8.20:4840")
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
    try:
        client.connect()

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        #print("root node is: ", root)

        objects = client.get_objects_node()
        #print("Objects node is: ", objects)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        #print("Children of root are: ", root.get_children())

        #print("Children of objects are: ", objects.get_children())

        for item in objects.get_children():
          print(item.get_browse_name(), item.get_path()[-1])

        node = client.get_node("ns=2;i=5001")

        for item in node.get_children():
          print(item.get_browse_name(), item.get_path()[-1])

        #recursive(objects.get_children(), objects.get_browse_name())
          #node = client.get_node(ua.NodeId(iterator))


        # get a specific node knowing its node id
        #var = client.get_node(ua.NodeId(1002, 2))
        #var = client.get_node("ns=3;i=2002")
        #print(var)
        #var.get_data_value() # get value of node as a DataValue object
        #var.get_value() # get value of node as a python builtin
        #var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        #var.set_value(3.9) # set node value using implicit data type

        # Now getting a variable node using its browse path
        # myvar = root.get_child(["TwoByteNodeId", "TwoByteNodeId", "TwoByteNodeId"])
        # obj = root.get_child(["0:Objects", "2:MyObject"])
        # print("myvar is: ", myvar)
        # print("myobj is: ", obj)

        # Stacked myvar access
        # print("myvar is: ", root.get_children()[0].get_children()[1].get_variables()[0].get_value())

    finally:
        client.disconnect()
