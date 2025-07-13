#!/usr/bin/env python3
import zipfile
import itertools
import pyfiglet
import time
from argparse import ArgumentParser
def banner():
    print(r"""
  T E C H   2 4   I N D I
  -------------------------
    """)
    print("  Premium Hacking Resources")
    print("  https://github.com/Tech24Indi\n")
    print("Zip Password Cracker - Termux Edition")
    print("-------------------------------------\n")
def color_text(text, color=None, bg_color=None, style=None):
    colors = {
        'black': '30', 'red': '31', 'green': '32', 'yellow': '33',
        'blue': '34', 'magenta': '35', 'cyan': '36', 'white': '37',
        'bright_black': '90', 'bright_red': '91', 'bright_green': '92',
        'bright_yellow': '93', 'bright_blue': '94', 'bright_magenta': '95',
        'bright_cyan': '96', 'bright_white': '97'
    }
    bg_colors = {
        'black': '40', 'red': '41', 'green': '42', 'yellow': '43',
        'blue': '44', 'magenta': '45', 'cyan': '46', 'white': '47',
        'bright_black': '100', 'bright_red': '101', 'bright_green': '102',
        'bright_yellow': '103', 'bright_blue': '104', 'bright_magenta': '105',
        'bright_cyan': '106', 'bright_white': '107'
    }
    styles = {
        'normal': '0', 'bold': '1', 'faint': '2', 'italic': '3',
        'underline': '4', 'blink': '5', 'reverse': '7', 'hidden': '8'
    }
    
    codes = []
    if color in colors:
        codes.append(colors[color])
    if bg_color in bg_colors:
        codes.append(bg_colors[bg_color])
    if style in styles:
        codes.append(styles[style])
    
    if codes:
        return f"\033[{';'.join(codes)}m{text}\033[0m"
    return text

# Usage
print(color_text("------>Crated By Tech24indi<-----", "red", style="bold"))

def try_password(zip_file, password):
    try:
        zip_file.extractall(pwd=password.encode())
        return True
    except (RuntimeError, zipfile.BadZipFile):
        return False

def brute_force(zip_path, min_len=1, max_len=6, charset=None):
    if charset is None:
        charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
    
    zip_file = zipfile.ZipFile(zip_path)
    start_time = time.time()
    attempts = 0
    
    print(f"\n[+] Starting brute-force attack (Length: {min_len}-{max_len})")
    print(f"[+] Character set: {charset[:20]}...")
    
    for length in range(min_len, max_len + 1):
        for guess in itertools.product(charset, repeat=length):
            attempts += 1
            guess = ''.join(guess)
            
            if attempts % 1000 == 0:
                print(f"\r[+] Attempts: {attempts} | Current: {guess.ljust(8)}", end='', flush=True)
            
            if try_password(zip_file, guess):
                print(f"\n\n[+] Password found: {guess}")
                print(f"[+] Time elapsed: {time.time() - start_time:.2f} seconds")
                print(f"[+] Total attempts: {attempts}")
                return guess
    
    print("\n[-] Password not found with current settings")
    return None

def dictionary_attack(zip_path, wordlist_path):
    zip_file = zipfile.ZipFile(zip_path)
    start_time = time.time()
    attempts = 0
    
    try:
        with open(wordlist_path, 'r', errors='ignore') as f:
            words = f.read().splitlines()
    except FileNotFoundError:
        print(f"[-] Error: Wordlist file '{wordlist_path}' not found")
        return None
    
    print(f"\n[+] Starting dictionary attack with {len(words)} words")
    
    for word in words:
        attempts += 1
        word = word.strip()
        
        if attempts % 100 == 0:
            print(f"\r[+] Attempts: {attempts} | Current: {word.ljust(20)}", end='', flush=True)
        
        if try_password(zip_file, word):
            print(f"\n\n[+] Password found: {word}")
            print(f"[+] Time elapsed: {time.time() - start_time:.2f} seconds")
            print(f"[+] Total attempts: {attempts}")
            return word
    
    print("\n[-] Password not found in dictionary")
    return None

def main():
    parser = ArgumentParser(description='Zip Password Cracker Tool for Termux')
    parser.add_argument('zipfile', help='Path to the password-protected ZIP file')
    parser.add_argument('-m', '--mode', choices=['brute', 'dict'], required=True,
                       help='Attack mode: brute-force or dictionary')
    parser.add_argument('-w', '--wordlist', help='Path to wordlist file (for dictionary attack)')
    parser.add_argument('--min', type=int, default=1, help='Minimum password length (brute-force)')
    parser.add_argument('--max', type=int, default=6, help='Maximum password length (brute-force)')
    parser.add_argument('--charset', help='Custom character set (brute-force)')
    
    args = parser.parse_args()
    
    banner()
    
    if args.mode == 'brute':
        brute_force(args.zipfile, args.min, args.max, args.charset)
    elif args.mode == 'dict':
        if not args.wordlist:
            print("[-] Error: Wordlist path required for dictionary attack")
            return
        dictionary_attack(args.zipfile, args.wordlist)

if __name__ == '__main__':
    main()
