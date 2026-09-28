from content.categories import F, E, M, H, I

MODULES = [
{
 "id": "crypto-classical", "cat": "crypto", "title": "Classical Ciphers",
 "tier": F, "points": 50,
 "summary": "Caesar, Vigenere, substitution and transposition, and how frequency analysis breaks them.",
 "theory": [
  ("Substitution Ciphers", "Caesar shifts every letter by a fixed amount, so there are only twenty-five keys and brute force takes a second. A general substitution maps each letter to any other consistently, which multiplies the keyspace enormously but changes nothing about the underlying statistics: the most common ciphertext letter is very probably the most common plaintext letter, and short common words give themselves away by shape. This is why frequency analysis has been sufficient for a thousand years."),
  ("Vigenere And Repeated Keys", "Vigenere applies a different Caesar shift per position, using a repeating keyword, which flattens single-letter frequencies and defeats naive analysis. The weakness is the repetition. If the key length is guessed, the ciphertext splits into that many independent Caesar problems. The length is recoverable from the distance between repeated sequences, since a repeated plaintext stretch encrypted with the same key phase produces a repeated ciphertext stretch, and their spacing is a multiple of the key length."),
  ("Transposition And Modern Echoes", "Transposition does not change any letter, only their order, so letter frequencies survive untouched and anagram solving recovers the text. Columnar transposition writes plaintext in rows and reads out by columns in a keyed order. These are historical, but the lesson generalises: a cipher is broken by finding structure the design failed to destroy, and every real-world break since has followed the same logic."),
 ],
 "labs": ["game-caesar-crack", "game-vigenere-break"],
 "quiz": [
  {"q": "How many keys does a Caesar cipher have?", "a": ["26", "25", "52", "Infinitely many"], "c": 1, "why": "A shift of zero is no encryption, leaving twenty-five."},
  {"q": "What does frequency analysis exploit?", "a": ["Weak keys", "The letter distribution of the plaintext language surviving encryption", "Implementation bugs", "Short keys"], "c": 1, "why": "If letters substitute one for one, their relative frequencies are unchanged."},
  {"q": "Which cipher does frequency analysis fail against directly?", "a": ["Caesar", "General substitution", "Vigenere with a short repeating key", "Vigenere with a long random key"], "c": 3, "why": "A key as long as the message with no repetition flattens all statistics."},
  {"q": "Transposition ciphers change what?", "a": ["Letter values", "Letter positions only", "Both", "Neither"], "c": 1, "why": "Only ordering changes, so frequency analysis still applies."},
 ],
},
{
 "id": "crypto-hashing", "cat": "crypto", "title": "Hashing & Password Cracking",
 "tier": E, "points": 100,
 "summary": "Hash functions, salting, why MD5 is dead, and how wordlists and rules actually work.",
 "theory": [
  ("What A Hash Is For", "A cryptographic hash maps arbitrary input to fixed-length output, deterministically, quickly, and one-way. It must resist preimage (find input from output), second preimage (find a different input with the same output), and collision (find any two inputs with the same output). MD5 and SHA-1 fail collision resistance and are suitable only for non-security checksums, if at all."),
  ("Passwords Specifically", "Passwords must never be hashed with a fast general-purpose function. Speed is the enemy, because it helps the attacker as much as the application. Purpose-built password functions, bcrypt, scrypt and Argon2, are deliberately slow and tunable, with a cost parameter you raise as hardware improves, and they take a salt so identical passwords do not produce identical hashes and cannot be attacked jointly."),
  ("Cracking In Practice", "Dictionary attacks try each candidate from a wordlist. Rule-based attacks mutate them, appending digits, capitalising, substituting characters, because humans reuse patterns across every password they have ever set. Masks and brute force cover short or known-format keys, and are used for things like WPA handshakes or numeric PINs. Rainbow tables precompute chains for unsalted hashes, and also store the plaintext, which is why they are keyed to a specific algorithm and defeated entirely by a per-password salt."),
  ("Choosing And Judging Tools", "Hashcat exploits GPUs and is the right choice for volume; John the Ripper is more flexible about formats and mangling rules. Identify the hash from its length and prefix before running anything: thirty-two hex characters is likely MD5, forty is SHA-1, sixty-four is SHA-256, a dollar-two-a prefix is bcrypt. Getting the format right matters more than raw speed, because the wrong mode wastes every GPU cycle you have."),
 ],
 "labs": ["game-hash-crack", "lab-hashcat-basics"],
 "quiz": [
  {"q": "Why is a salt used?", "a": ["To make hashes shorter", "So identical passwords produce different hashes and cannot be attacked together", "To encrypt the hash", "To slow network transfer"], "c": 1, "why": "A unique per-user salt forces separate work for each hash and kills rainbow tables."},
  {"q": "Which is designed for passwords?", "a": ["MD5", "SHA-256", "bcrypt", "CRC32"], "c": 2, "why": "bcrypt is deliberately slow and salted by design."},
  {"q": "A 32-character hex string is most likely:", "a": ["SHA-256", "MD5", "bcrypt", "Base64"], "c": 1, "why": "128 bits as hex is thirty-two characters."},
  {"q": "What do rule-based attacks exploit?", "a": ["Weak algorithms", "Predictable human password patterns", "Network latency", "Salt reuse"], "c": 1, "why": "Adding digits, capitalising first letters and leet substitutions model what people actually do."},
  {"q": "What makes a hash function unsuitable for passwords?", "a": ["Being one-way", "Being fast and unsalted", "Producing fixed length", "Being well known"], "c": 1, "why": "Speed in the defender's favour is speed in the attacker's favour too."},
 ],
},
{
 "id": "crypto-symmetric", "cat": "crypto", "title": "Symmetric Encryption & Modes",
 "tier": M, "points": 125,
 "summary": "AES, block cipher modes, IVs, padding oracles and the mistakes that make encryption pointless.",
 "theory": [
  ("Block vs Stream", "A block cipher encrypts fixed-size blocks; a stream cipher produces a keystream that you XOR with plaintext, which is flexible but fatal if the keystream is ever reused, because XORing two ciphertexts cancels the keystream and leaves only the relationship between two plaintexts. WEP's infamous break was exactly this. Never reuse a nonce or IV in a stream construction."),
  ("Modes", "ECB encrypts each block independently, so identical plaintext blocks produce identical ciphertext blocks, and structure leaks through. It is a textbook error and it still ships. CBC chains blocks with a random IV but requires padding and is vulnerable to padding oracle attacks when the application leaks whether decryption failed. CTR turns a block cipher into a stream cipher. GCM provides authenticated encryption, giving integrity as well as confidentiality, and it is the default you should reach for."),
  ("Padding Oracles", "In CBC, decryption failure can be detected through a different error message, a different status code, or even a consistent timing difference. Each guess about plaintext bytes can be tested against that signal, and a few thousand requests recover the plaintext one byte at a time while leaking nothing else. The lesson generalises: any observable difference in failure behaviour is an oracle, and oracles leak."),
  ("Nonce And IV Rules", "An IV must be unpredictable where the mode requires it and unique always. Reuse in CBC with a predictable IV enables chosen-plaintext attacks; reuse in CTR or GCM breaks confidentiality immediately and, for GCM, authentication too. This is not a subtle design point, it is the most commonly botched part of using crypto correctly."),
 ],
 "labs": ["game-ecb-detect", "lab-padding-oracle"],
 "quiz": [
  {"q": "What does ECB leak?", "a": ["The key", "Structure, via identical plaintext blocks giving identical ciphertext", "The IV", "Nothing"], "c": 1, "why": "No chaining means patterns survive encryption."},
  {"q": "Which AES mode provides authenticity as well as confidentiality?", "a": ["CBC", "ECB", "GCM", "CTR"], "c": 2, "why": "GCM is an authenticated encryption mode with an authentication tag."},
  {"q": "A padding oracle attack relies on what?", "a": ["Key weakness", "An observable difference when decryption and padding validation fail", "Short keys", "Weak IVs"], "c": 1, "why": "The side channel turns decryption into a byte-by-byte guessing game."},
  {"q": "Is it acceptable to reuse an IV in CTR mode?", "a": ["Yes", "No, it destroys confidentiality", "Only with a strong key", "Only for small messages"], "c": 1, "why": "Reusing the keystream allows XORing ciphertexts to cancel it out."},
 ],
},
{
 "id": "crypto-asymmetric", "cat": "crypto", "title": "Public Key Crypto & TLS",
 "tier": M, "points": 125,
 "summary": "RSA and Diffie-Hellman, key sizes, signature verification and certificate chain abuse.",
 "theory": [
  ("Key Exchange And The Hard Problems", "RSA security rests on factoring large integers; Diffie-Hellman on the discrete logarithm problem, in a group where it is believed hard. A modern TLS handshake uses ephemeral Diffie-Hellman to derive a session key that is discarded afterwards, giving forward secrecy: an attacker who steals the private key later cannot decrypt traffic captured earlier. Static RSA key exchange lacks this, which is why it is deprecated."),
  ("RSA Pitfalls", "Small moduli fall to factoring with public tools, so anything below 2048 bits is a finding. Textbook RSA without padding is malleable, so an attacker can multiply a ciphertext by a known value and predictably alter the plaintext. Sharing a modulus between two keypairs, using two different exponents on the same message, or a common factor between two moduli recoverable with the greatest common divisor, all destroy it. Randomness failures have produced real shared-prime breaks in the wild."),
  ("Signatures And The Verify Order", "A signature proves integrity and origin. Failures are usually not mathematical but procedural: verifying the signature after processing the content, accepting the alg field from the token when the server should enforce it, or treating an unsigned message as valid. Sign-then-encrypt versus encrypt-then-sign confusion also yields practical attacks. Read the verification code, not the maths."),
  ("Certificates And Trust", "A certificate binds a public key to an identity, signed by a certificate authority. Browsers check the chain to a trusted root, the validity dates, the hostname and revocation status. Common weaknesses: a private key that is weak or shared, a certificate generated on a system with poor entropy, an internal CA that will sign anything you ask, and hostname validation that is skipped in some library default. Misissuance has happened at every major CA."),
 ],
 "labs": ["game-rsa-recover", "lab-cert-inspect"],
 "quiz": [
  {"q": "What provides forward secrecy?", "a": ["Static RSA", "Ephemeral Diffie-Hellman", "AES-128", "SHA-256"], "c": 1, "why": "Ephemeral keys discarded after the session mean past traffic stays safe if the long-term key leaks."},
  {"q": "Two RSA moduli sharing a prime factor can be broken how?", "a": ["Brute force", "Computing the greatest common divisor", "Rainbow table", "Timing analysis"], "c": 1, "why": "The shared factor falls out of a GCD computation between the two moduli."},
  {"q": "Why is textbook RSA without padding unsafe?", "a": ["Too slow", "It is malleable: multiplying the ciphertext multiplies the plaintext", "Weak keys", "Large output"], "c": 1, "why": "The multiplicative property lets an attacker transform a ciphertext predictably."},
  {"q": "What does a certificate chain prove?", "a": ["The server is fast", "That a trusted CA vouched for the binding of key to identity", "The server is patched", "Encryption is enabled"], "c": 1, "why": "Trust anchors the identity, not the security of the implementation."},
 ],
},
]
