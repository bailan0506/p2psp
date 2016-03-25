"""
A Simple Demo of Naranjo et al's key distribution scheme
"""
import gmpy2
from gmpy2 import mpz
from Crypto.Random import random

def generate_large_prime(bits):
    """ 
        Generate large pseudo prime .
        Args:
            bits: int, the number of bits of the prime you want to generate.
    """
    rand_prime=random.getrandbits(bits)
    if (rand_prime%2)==0 :
        rand_prime=rand_prime-1

    while not gmpy2.is_prime(rand_prime):
        rand_prime=rand_prime+2
    return rand_prime
    
def generate_m(p):
    """ Generate large pseudo prime m, which satisfy p|(m-1) .
    """
    q=1
    m=p*2*q+1
    while not gmpy2.is_prime(m):
        q=q+1
        m= p*2*q+1
    return m,q

def get_key(g,m,u,x_i):
    """Members calculate keys.
    """
    delta=gmpy2.invert(u,x_i)
    r=gmpy2.powmod(g,delta,m)
    return r
    

def generate_key_r(bits,x):
    """ Generate the key r. All the variables' name are the same as those used in the paper.
        Args:
            bits: int, the number of bits of p, which can be set to be larger than the length of r.
            x: list, includes x_i which has been distributed members.         
    """

    p=generate_large_prime(bits)
    (m,q)=generate_m(p)
    
    delta= generate_large_prime(len(bin(min(x)))-2)
    k=delta-p
    
    a=generate_large_prime(bits)
    g=gmpy2.powmod(a,q,m)
    
        
    r=gmpy2.powmod(g,k,m)
    
    L=1
    for x_i in x :
       L=gmpy2.mul(L,x_i)
       
    u=gmpy2.invert(delta,L)
    
    """ Because the primes generated are pseudo primes that has passed probable 
        prime test, it is possible that the member cannot calculat the right key.
        Verify the members can calculate the key rightly.
    """
    
    while get_key(g,m,u,x[0])!=r:
        p=generate_large_prime(bits)
        (m,q)=generate_m(p)
        
        delta= generate_large_prime(len(bin(min(x)))-2)
        k=delta-p
        
        a=generate_large_prime(bits)
        g=gmpy2.powmod(a,q,m)
            
        r=gmpy2.powmod(g,k,m)
        
        L=1
        for x_i in x :
           L=gmpy2.mul(L,x_i)
           
        u=gmpy2.invert(delta,L)
        
        
    return (g,m,u,L,r)

    
def regenerate_key(bits,x,x_i,L,leave):
    """ Regenerate the key r when some peer join or leave the team. All the variables' name are the same as those used in the paper.
        Args:
            bits: int, the number of bits of p, which can be set to be larger than the length of r.
            x: list, x_i which has been distributed members.
            x_i: int, the x_i of a member who wants to join or leave the team.
            L: int, the value of product of x_is before the member join or leave.
            leave: bool. True if the x_i is leaving the team. False if the x_i is join the team.
    """  

    p=generate_large_prime(bits)
    (m,q)=generate_m(p)
    
    delta= generate_large_prime(len(bin(min(x)))-2)
    k=delta-p
    
    a=generate_large_prime(bits)
    g=gmpy2.powmod(a,q,m)
    
        
    r=gmpy2.powmod(g,k,m)
    
    if leave :
       L=gmpy2.div(L,x_i)
    else:
       L=gmpy2.mul(L,x_i)
       
    u=gmpy2.invert(delta,L)
    
    while get_key(g,m,u,x[0])!=r:
        p=generate_large_prime(bits)
        (m,q)=generate_m(p)
        
        delta= generate_large_prime(len(bin(min(x)))-2)
        k=delta-p
        
        a=generate_large_prime(bits)
        g=gmpy2.powmod(a,q,m)
            
        r=gmpy2.powmod(g,k,m)
        
        if leave :
           L=gmpy2.div(L,x_i)
        else:
           L=gmpy2.mul(L,x_i)
           
        u=gmpy2.invert(delta,L)
        
        
    return (g,m,u,L,r)



    
    
if __name__ == '__main__':
    # Test functions.
    x=list()
    x_bits=60
    for i in range(0,4):
        x.append(generate_large_prime(60))
    bits=128
    (g,m,u,L,r)=generate_key_r(bits,x)
    print r #If the length of r is greater than needed, truncate.
    r_member=get_key(g,m,u,x[1])
    print r_member
    x.append(generate_large_prime(60))
    (g,m,u,L,r)=regenerate_key(bits,x,x[3],L,False)
    print r
    r_member=get_key(g,m,u,x[3])
    print r_member
    


