import random
import math

def generate_uniform(a, b):
    """Generates a random variable uniformly distributed between a and b."""
    u = random.random()
    return (b - a) * u + a

def generate_exponential(lam):
    """Generates a random variable exponentially distributed with rate lam."""
    if(lam <= 0):
        raise ValueError("Rate parameter lam must be positive.")
    u = random.random()
    return - math.log(1-u) / lam

def generate_normal(mu, sigma):
    """Generates a random variable normally distributed with mean mu and standard deviation sigma."""
    return random.gauss(mu, sigma)
