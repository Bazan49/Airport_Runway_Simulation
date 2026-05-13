import random
import math

def generate_exponential(lam):
    """Generates a random variable exponentially distributed with rate lam."""
    if(lam <= 0):
        raise ValueError("Rate parameter lam must be positive.")
    u = random.random()
    return - math.log(1-u) / lam

def generate_normal(mean=0.0, std=1.0):
    """Generates a normally distributed random variable using the Box‑Müller method."""
    if std <= 0:
        raise ValueError("Standard deviation must be positive.")
    # Generate two independent uniform (0,1) values
    u1 = random.random()
    u2 = random.random()
    # Box-Müller transformation
    z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    return mean + std * z
