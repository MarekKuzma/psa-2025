from datetime import datetime
aktualny_rok = datetime.now().year
meno = input("Zadaj svoje meno: ")
rok_narodenia = int(input("Zadaj rok narodenia: "))
vek = aktualny_rok - rok_narodenia
print(f"Ahoj, {meno}!")
print(f"Máš {vek} rokov.")