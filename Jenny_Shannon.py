import math
import sys
import time
from collections import Counter

sys.set_int_max_str_digits(0)

def shannon_entropy(s):
    freq = Counter(s)
    length = len(s)
    return -sum((c / length) * math.log2(c / length) for c in freq.values())

def get_sequence_value(seed, iterations):
    current = seed
    for _ in range(iterations):
        current = str(int(current, 16))
    return current

def xor_with_key(text, key):
    key_bytes = key.encode()
    text_bytes = text.encode()
    return bytes(t ^ key_bytes[i % len(key_bytes)] for i, t in enumerate(text_bytes))

def encrypt(plaintext, seed, iterations):
    key = get_sequence_value(seed, iterations)
    return xor_with_key(plaintext, key).hex()

def decrypt(ciphertext, seed, iterations):
    key = get_sequence_value(seed, iterations)
    return xor_with_key(bytes.fromhex(ciphertext), key).decode()

def run_sequence(seed):
    current = seed
    seen = {}
    iteration = 0
    try:
        while True:
            current = str(int(current, 16))
            entropy = shannon_entropy(current)
            digit_count = f"{len(current):,}"
            print(f"{iteration:>4}  {current:<30}  {digit_count:>15} digits  H = {entropy:.4f} bits/digit")
            if current in seen:
                print(f"\nCycle detected: iteration {iteration} repeats iteration {seen[current]}.")
                break
            seen[current] = iteration
            iteration += 1
            time.sleep(1.5)
    except KeyboardInterrupt:
        print(f"\nStopped at iteration {iteration}.")

print("Jenny's Number")
print("Seed: any hex string, e.g. 867 (0x867 = 2151 decimal)\n")

mode = input("Mode — (r)un sequence ").strip().lower()
seed = input("Seed (hex): ").strip()

if mode == "r":
    run_sequence(seed)
elif mode == "e":
    iterations = int(input("Iterations: "))
    plaintext = input("Message: ")
    print(f"\nCiphertext: {encrypt(plaintext, seed, iterations)}")
elif mode == "d":
    iterations = int(input("Iterations: "))
    ciphertext = input("Ciphertext (hex): ")
    print(f"\nPlaintext: {decrypt(ciphertext, seed, iterations)}")
