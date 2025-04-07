# Co je FlappyBird DX?
Remake Flappy Birda pomocí Pythonu a knihovny PyGame.
# V čem je to jiné oproti klasickému Flappy Birdovi?
Zatím ve 2 věcech:
- Existují i zlaté trubky. Je 10% šance že se vygenerují místo normálních trubek, dávají 3 body a mají menší díru než normální trubky.
- Skóre se může nahrávat do tabulek pro světové rekordy. Každý záznam obsahuje i čas, kdy byl rekord vytvořen.
# A jak to mám nainstalovat?
Nejdříve si stáhněte Python ze stránky https://www.python.org.
Při instalaci zaškrtněte "Add Python to PATH".
Poté otevřete příkazový řádek a napište následující:
```
cd C:\Cesta\K\Instalaci
```
```
pip install -r requirements.txt
```
To zaručí instalaci potřebných knihoven pro hru.
Následně přidejte informace o MySQL serveru do souboru `menu.py` - na začátku souboru je indikátor, kam údaje o serveru vepsat.
Pak už stačí jenom hru spustit v příkazovém řádku:
```
python menu.py
```
Hodně štěstí!
# Patch Notes
Viz stránka https://xeon.spskladno.cz/~slechtao/FlappyBirdDX/updates.php