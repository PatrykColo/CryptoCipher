# CryptoCypher

Projekt edukacyjny w pythonie mający na celu eksplorację różnych sposobów szyfrowania plików.

# Zasada Działania

## DES

Data Encryption Standard to algorytm szyfrowania symetrycznego opracowany we wczesnych latach 70. Bazowany jest na wcześniejszym algorytmie znanym jako Sieć Feistela. Obecnie jest powszechnie uznawany za 

### Szczegóły techniczne
DES w teorii używa 64-bitowego klucza, w praktyce jednak ostatnie 8 bitów nieużywane jest w procesie szyfrowania. W pierwszym kroku tekst jawny dzielony jest na 64-bitowe bloki. Jeśli rozmiar szyfrowanych danych nie jest wielokrotnością 64 to ostatni blok jest wypełniony aby był. Następnie dla każdego bloku wykonywany jest następujący algorytm:

1. Podziel blok wejściowy na lewą i prawą część $L_0$ i $P_0$
2. Przesuń bity klucza zgodnie z tabelą permutacji (po tym kroku klucz będzie miał 56 bitów).
3. Podziel klucz na dwie, 28-bitowe części $C_0$ i $D_0$
4. Wykonaj następne 3 kroki 16 razy

    1. Wykonaj przesunięcie cykliczne w lewo $C_i$ i $D_i$ o 1 w iteracji=1, 2 i 16, i o 2 w każdej innej, uzyskując podklucze $C_i$ i $D_i$
    2. Złącz ze sobą podklucze $C_i$ i $D_i$ uzyskując klucz $K_i$
    3. Stwórz lokalne dla iteracji $L_i = R_{i-1}$ i $R_i = f(R_{i-1}, K_i)$ gdzie f zdefiniujemy poniżej
5. Po wykonaniu tych iteracji otrzymujemy blok wyjściowy $O = R_{16} + L_{16}$
6. Blok wyjściowy permutujemy finalnie za pomocą tabeli permutacji.

Funkcja $f$ przyjmuje jako parametry 32-bitowy blok danych $D$ oraz 48-bitowy klucz $K$.
1. Rozszerz $D$ do 48 bitów używając tabeli permutacji, wynik tej opracji nazwijmy $E$
2. Wykonaj xor $E$ i $K$, nazwijmy wynik X.
3. Podziel X na 8 grup po 6 bitów od $B_1$ do $B_8$. Dokonaj konwersji X na 32-bitową liczbę w następujący sposób: z tych najstarszego i najmłodszego bitu złóż liczbę 2-bitową (0..3). Liczba ta wskazuje na rząd w tabeli dekodowania $S_i$. Na kolumnę w owej tableki wskazuję środkowe 4 bity. Z tabeli tej odczytaj liczbę która będzie z przedziału 0..15 (4-bity). Złóż wszystkie wyniki w kolejności, wynik nazwijmy $O$
4. Wykonaj permutację $O$ zgodnie z tablą permutacji, otrzymana permutacja to wynik funkcji.

## AES

### TODO

## Tryby szyfrowania

Zarówno DES jak i AES korzystają z trybów szyfrowania. Są to warianty algorytmu w które różnią się sposobem tworzenia bloków wejściowych lub wyjściowych. W projekcie zastosowano trzy rózne tryby szyfrowania.

### ECB
ECB - z ang. Electronic Codebook. Jest to tryb w którym każdy blok tekstu jawnego szyfrowany jest oddzielnie w jeden blok szyfrogramu.

### CBC

CBC - z ang. Cipher Blokck Chaining. W tym trybie pracy każdy blok wejściowy jest XORem poprzedniego bloku szyfrogramu i obecnego bloku tekstu jawnego. Pierwszy blok zamiast poprzedniego bloku szyfrogramu używa tzw. wektora inicjalizyjnego.

### CTR

Ctr - z ang. Counter. W tym unikalnym trybie pracy tekst jawny nie jest wejściem algorytmu szyfrowania blokowego. Zamiast tego używa się połączenia bajtów nonce wraz z licznikiem który inkrementowany jest co blok. Wyjście algorytmu szyfrującego XORuje się z blokiem tekstu jawnego.

# Funkcjonalności

### TODO

# Przykłady użycia

# Budowanie

## Windows

# Szczegóły techniczne aplikacji

Interfejs aplikacji napisany jest za pomocą biblioteki PySide6, funkcje kryptograficzne wzięte są z biblioteki pycryptodome.

# Referencje

Strona z obrazami testowymi: https://openclipart.org
Dobry opis DES: https://pl.wikipedia.org/wiki/Data_Encryption_Standard
Kolejny dobry opis DES: https://billstclair.com/grabbe/des.htm