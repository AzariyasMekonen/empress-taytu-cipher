# Empress Taytu's Royal Cipher (Crypto / Dynamic Generator, Easy)

**Story:**
Empress Taytu Betul was not only the empress consort of Ethiopia but also one of its foremost military strategists. During the campaign of 1895–1896, she commanded a contingent of 5,000 soldiers and personally oversaw the artillery batteries and logistical supply. Her secret courier dispatches used an affine substitution cipher.

## Mechanics
- This challenge supports the platform's **On-Demand Dynamic File Generator** to generate personalized challenge files with participants' unique dynamic flags.
- Players examine `output/taytu_dispatch.txt` and `output/cipher_rules.txt`.
- Alphabet: `ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}` (size $M = 39$).
- Cipher function: $C \equiv (a \cdot P + b) \pmod{39}$, with $\gcd(a, 39) = 1$.
- Decryption function: $P \equiv a^{-1} \cdot (C - b) \pmod{39}$.
- Crib: First 12 characters are `TAYTU_BETUL_`.

## Dynamic File Generator Settings
- **Type**: `dynamic`
- **Output Filename**: `taytu_dispatch.txt`
- **Environment Variables**:
  - `FLAG`: Dynamic participant flag (e.g. `AdwaCTF{...}`)
  - `USER_ID`: Unique participant or team identifier
  - `OUTPUT_DIR`: Target directory (defaults to `/output`)
  - `OUTPUT_FILENAME`: Name of output file inside `/output/` (defaults to `taytu_dispatch.txt`)

## Solution Walkthrough
1. Using crib letters:
   - For character 0: plaintext 'T' (index 19) -> ciphertext character $C_0$.
   - For character 1: plaintext 'A' (index 0) -> ciphertext character $C_1$.
   From $P = 0$, $b = C_1$.
   From $19a + b \equiv C_0 \pmod{39}$, solve for $a$.
2. Compute $a^{-1} \pmod{39}$.
3. Decrypt the entire ciphertext:
   $P_i = (a^{-1} \times (C_i - b)) \pmod{39}$.
4. Flag is revealed: `AdwaCTF{74y7u_b37ul_qu33n_0f_l10n5}`.

Run `solve/solve.py` to solve automatically.
