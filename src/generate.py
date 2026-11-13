#!/usr/bin/env python3
"""
On-Demand Dynamic Challenge File Generator for Empress Taytu's Royal Cipher (AdwaCTF).

Environment variables:
  - FLAG: Dynamic participant-specific flag (e.g. 'AdwaCTF{...}')
  - USER_ID: Optional participant or team identifier
  - OUTPUT_FILENAME: Output file name (default: 'taytu_dispatch.txt')
  - OUTPUT_DIR: Target directory to write to (default: 'output' or '/output')
"""

import os
import sys
import math
import secrets
from pathlib import Path

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}"
M = len(ALPHABET)  # 39

# Candidate coprimes to 39
COPRIMES = [x for x in range(1, M) if math.gcd(x, M) == 1]

def encrypt_char(c, a, b):
    if c not in ALPHABET:
        return c
    idx = ALPHABET.index(c)
    enc_idx = (a * idx + b) % M
    return ALPHABET[enc_idx]

def encrypt_text(text, a, b):
    return "".join(encrypt_char(c, a, b) for c in text.upper())

def get_flag():
    flag = os.environ.get("FLAG", "").strip()
    if flag:
        return flag

    candidates = ["flag.txt", "/app/flag.txt", "../flag.txt"]
    for c in candidates:
        if os.path.isfile(c):
            try:
                with open(c, "r", encoding="utf-8") as f:
                    val = f.read().strip()
                    if val:
                        return val
            except OSError:
                pass

    return "AdwaCTF{74y7u_b37ul_qu33n_0f_l10n5}"

def main():
    flag = get_flag()
    user_id = os.environ.get("USER_ID", "operative_taytu").strip()
    here = Path(__file__).resolve().parent.parent

    # Determine primary output target directory
    output_path = os.environ.get("OUTPUT_PATH", "").strip()
    if output_path:
        target_file = Path(output_path).resolve()
        target_dir = target_file.parent
        target_dispatch_name = target_file.name
    elif len(sys.argv) > 1 and sys.argv[1].strip():
        arg_path = Path(sys.argv[1].strip()).resolve()
        if arg_path.is_dir() or sys.argv[1].endswith("/"):
            target_dir = arg_path
            target_dispatch_name = "taytu_dispatch.txt"
        else:
            target_dir = arg_path.parent
            target_dispatch_name = arg_path.name
    else:
        env_dir = os.environ.get("OUTPUT_DIR", "").strip()
        if env_dir:
            target_dir = Path(env_dir).resolve()
        elif Path("/output").is_dir():
            target_dir = Path("/output")
        else:
            target_dir = here / "output"
        target_dispatch_name = os.environ.get("OUTPUT_FILENAME", "taytu_dispatch.txt").strip()

    target_dir.mkdir(parents=True, exist_ok=True)

    # Cryptographic parameter selection: random coprime 'a' and shift 'b'
    a = secrets.choice(COPRIMES)
    b = secrets.randbelow(M)

    plaintext = (
        f"TAYTU_BETUL_IMPERIAL_DECREE_"
        f"MEKELLE_WATER_SPRINGS_CUT_OFF_"
        f"ADVANCE_TO_ADWA_AND_SEIZE_THE_CRESTS_"
        f"FLAG_IS_{flag}"
    )

    ciphertext = encrypt_text(plaintext, a, b)

    rules_content = (
        "IMPERIAL CIPHER CODEX:\n"
        f"Alphabet space ({M} characters): {ALPHABET}\n"
        "Each character C at index P is enciphered via affine mapping:\n"
        "C = (a * P + b) mod 39\n"
        "Known crib: The dispatch begins with the Empress's royal title 'TAYTU_BETUL_'\n"
    )

    dirs_to_write = {target_dir}
    if Path("/output").is_dir():
        dirs_to_write.add(Path("/output"))

    if (here / "output").is_dir() and not env_dir and not output_path and len(sys.argv) <= 1:
        dirs_to_write.add(here / "output")

    for d in dirs_to_write:
        try:
            d.mkdir(parents=True, exist_ok=True)
            dispatch_file = d / target_dispatch_name
            with open(dispatch_file, "w", encoding="utf-8") as f:
                f.write(ciphertext + "\n")
            try:
                os.chmod(dispatch_file, 0o666)
            except OSError:
                pass

            rules_file = d / "cipher_rules.txt"
            with open(rules_file, "w", encoding="utf-8") as f:
                f.write(rules_content)
            try:
                os.chmod(rules_file, 0o666)
            except OSError:
                pass
        except OSError:
            pass

    # Also keep dist/ updated if present and no custom target was forced
    if (here / "dist").is_dir() and not env_dir and not output_path and len(sys.argv) <= 1:
        try:
            with open(here / "dist" / "taytu_dispatch.txt", "w", encoding="utf-8") as f:
                f.write(ciphertext + "\n")
            with open(here / "dist" / "cipher_rules.txt", "w", encoding="utf-8") as f:
                f.write(rules_content)
        except OSError:
            pass

    print(f"[generator] user_id={user_id}")
    print(f"[generator] a={a}, b={b}")
    print(f"[generator] target_dir={target_dir}")
    print(f"[generator] generated output files: taytu_dispatch.txt, cipher_rules.txt")

if __name__ == "__main__":
    main()
