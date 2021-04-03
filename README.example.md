**Nume**: Sandu Ilie-Cristian  
**Grupă**: 334CC

# Tema 1 ACS

## Organizare

1. Explicație pentru soluția aleasă:  
   Am folosit clasele definite în skelet, nu am considerat necesar nimic suplimentar. Am ales o implementare mai minimalistă protejând anumite zone pe care le-am considerat critice în: **register_producer**, **new_cart**, **add_to_cart** și **place_order**.
   Ca si structuri de date pentru păstrarea informațiilor în **Marketplace** am utilizat:

- o listă pentru stocarea id_producers
- o listă pentru produsele din Maketplace
- dicționar pentru asocierea dintre id_producător (key) si nr de produse pe care acesta le-a produs (value)
- dicționar pentru asocierea dintre produs (Key) si id_producator (value)
- dicționar pentru asocierea id_cart (key) si o listă (value) cu produse care sunt in coșul asociat cu id_cart

  **Am folosit dicționare din punctul de vedere al faptului ca introducerea si scoaterea este in O(1).**

2. Consideri că tema este utilă?  
   A fost din prisma utilizării python si modului de programare, dar modele similare am facut si la APD semestrul trecut ( apreciez că nu e tot JAVA ;) )
3. Consideri implementarea naivă, eficientă, se putea mai bine?  
   Implementare este putin naivă din prisma faptului că protejez doar anumite zone, dar totuși este eficientă.  
   Aș fi putut stoca diferit id_utile producătorilor in marketplace.

## Implementare

- **De specificat dacă întregul enunț al temei e implementat**  
  Întregul enunț al temei a fost implementat în totalitate
- **Dacă există funcționalități extra, pe lângă cele din enunț - descriere succintă + motivarea lor**  
   Nu exista funcții extra
- **De specificat funcționalitățile lipsă din enunț (dacă există) și menționat dacă testele reflectă sau nu acest lucru**  
  Nu exista funcționalităti lipsă

- **Lucruri interesante descoperite pe parcurs si Dificultăți întâmpinate**  
  Modul de afișarea, se întelege că afișarea soluției trebuia să se facă autoamta cand trimiteam lista, dar in schimb trebuia sa îl afișăm noi la stdout. Aveam anumite zone pe care le-am considerat neimportante si a trebuit să le protejez și pe acestea cu câte un lock.
  Checker-ul local nu îmi trecea din cauza termiantoarelor de șir din fișierul de referință.  
  Rezolvare: `sed -i -e 's/\r$//' fisiere de out.ref`

## Resurse utilizate

- Laboratorul 01 - Introducere în limbajul Python
- Laboratorul 02 - Fire de execuție în Python
- Laboratorul 03 - Programare concurentă în Python (continuare)

## Git

1. [Link Repo GitHub](https://github.com/CristiSandu/Marketplace-H1-ASC.git)
