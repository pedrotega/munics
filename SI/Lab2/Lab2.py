import random
import paho.mqtt.client as mqtt
from threading import Thread

# MQTT broker address and port
mqttBroker = '18.101.47.122'
password = 'HkxNtvLB3GC5GQRUWfsA'
mqtt_id = 'sinf'
port = 1883

'''
    The messages are going to be send with an id that 
    are going to be used to know the content of the 
    message.
'''

# We need two dictionaries to don't cheat.
# Threads share the memory space.
info_bob = {
    'seed': None,
    'r': None,
    'msg': None,
    'b': None
}

info_alice = {
    'seed': None,
    'c': None
}

def string_to_bits_array(msg):
    bits_array = []

    for char in msg:
        binary_rep = bin(ord(char))[2:]
        padded_binary_rep = binary_rep.zfill(8)

        for bit in padded_binary_rep:
            bits_array.append(int(bit))

    return bits_array

def bits_array_to_string(b):
    msg = ''
    for i in range(0,int(len(b)/8)):
        bits_ltr = b[i*8:(i*8)+8]
        ascii_ltr = 0
        for p,j in enumerate(bits_ltr[::-1]):
            ascii_ltr += j * 2 ** p
        msg += chr(ascii_ltr)

    return msg

def generate_r_vector(q):
    bit_vector = [0] * (2*q)

    one_indices = random.sample(range(2*q), q)

    for i in one_indices:
        bit_vector[i] = 1

    return bit_vector

def prg_Gs(l,seed):
    bit_vector = [0]*l
    random.seed(seed)
    n_1s = random.randint(0,l)
    one_indices = random.sample(range(l), n_1s)
    for i in one_indices:
        bit_vector[i] = 1

    return bit_vector

def getGrGz(r,gs):
    gr = []
    gz = []
    for i,j in zip(r,gs):
        if(i==1):
            gr.append(j)
        else:
            gz.append(j)

    return gr,gz

def parseCTX(ctx: str):
    return ctx.encode().rjust(5, b'\x00')

def on_message_bob(client, userdata, message):
    ctx = message.payload[:5].replace(b'\x00', b'').decode()
    pref = '\n[BOB] - ' 
    if(ctx=='b'):
        b = list(message.payload[5:])
        print(pref+'Vector b recived.')
        m = len(b)
        q = 3*m
        r = generate_r_vector(q)
        msg = bits_array_to_string(b)
        info_bob['b']=b
        info_bob['r']=r
        info_bob['msg']=msg
        ctx = parseCTX('r')
        client.publish('Alice', ctx+bytes(r))
    elif(ctx=='e'):
        e = list(message.payload[5:])
        print(pref+'Vector b recived.')
        info_bob['e']=e
    elif(ctx=='gz'):
        gz_alice = list(message.payload[5:])  
        info_bob['gz']=gz_alice
        print(pref+'Vector gz recived.')
        r = info_bob['r']
        b = info_bob['b']
        c_prime = b+b+b
        gs = prg_Gs(len(r), seed=info_bob['seed'])
        gr,gz = getGrGz(r,gs)
        e = info_bob['e']
        e_prime = []
        for i,j in zip(c_prime,gr):
            e_prime.append(i ^ j)

        print(pref+'VERIFICATION:')
        print('\t> Meesage recived:',info_bob['msg'])
        if(e == e_prime and gz == gz_alice):
            print('\t> Verification succed.')
        else:
            print('\t> Error in verification.')
        
        seed = input(pref+'Give me a seed(int): ')
        info_bob['seed'] = int(seed)
        msg = parseCTX('seed')+str(seed).encode()
        client.publish('Alice', msg)

        

def Bob():
    client = mqtt.Client()
    client.username_pw_set(username=mqtt_id, password=password)
    client.connect(mqttBroker,port)

    pref = '\n[BOB] - ' 
    # Choosing and sending the seed.
    seed = input(pref+'Give me a seed(int): ')
    info_bob['seed'] = int(seed)
    msg = parseCTX('seed')+str(seed).encode()
    client.publish('Alice', msg)

    client.subscribe('Bob')
    client.on_message = on_message_bob
    client.loop_forever()
    # Computing and sending r vector.


def on_message_alice(client, userdata, message):
    client = mqtt.Client()
    client.username_pw_set(username=mqtt_id, password=password)
    client.connect(mqttBroker,port)
    ctx = message.payload[:5].replace(b'\x00', b'').decode()
    pref = '\n[ALICE] - '
    if(ctx=='seed'):
        # Reciving seed.
        seed = int(message.payload[5:])
        print(pref+'Seed recived:',seed)

        # Get message, compute b and send it.
        msg = input(pref+'Write a message: ')
        ctx = parseCTX('b')
        b = string_to_bits_array(msg)
        c = b+b+b
        info_alice['seed']=seed
        info_alice['c']=c
        client.publish('Bob',ctx+bytes(b))
    elif(ctx=='r'):
        r = list(message.payload[5:])
        print(pref+'Vector r recived.')
        c = info_alice['c']
        gs = prg_Gs(len(r), seed=info_alice['seed'])
        print(pref,gs)
        print(pref,len(gs))
        gr, gz = getGrGz(r, gs)
        e = []
        for i,j in zip(c,gr):
            e.append(i ^ j)
        ctx = parseCTX('e')
        client.publish('Bob', ctx+bytes(e))
        ctx = parseCTX('gz')
        client.publish('Bob', ctx+bytes(gz))

def Alice():
    client = mqtt.Client()
    client.username_pw_set(username=mqtt_id, password=password)
    client.connect(mqttBroker,port)

    client.subscribe('Alice')
    client.on_message = on_message_alice
    client.loop_forever()


t_bob = Thread(target=Bob)
t_alice = Thread(target=Alice)
t_bob.start()
t_alice.start()
