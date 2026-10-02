# dependencies-finder

Encuentra la versión mínima de un paquete de npm que declara una dependencia compatible con
una versión dada.

Sirve para resolver una vulnerabilidad transitiva: si `cross-spawn` tiene que estar en
`7.0.5` o más, dice desde qué versión de `eslint` el rango declarado ya la acepta, y entonces
alcanza con actualizar el paquete padre.

## Uso

```bash
pip install requests semantic_version
python main.py <paquete-padre> <paquete-hijo> <versión-del-hijo>
```

```console
$ python main.py eslint cross-spawn 7.0.5
La versión mínima de 'eslint' que declara 'cross-spawn' compatible con '7.0.5' es: …
```

Recorre las versiones publicadas del padre en el registry de npm, de la más vieja a la más
nueva, y devuelve la primera cuyo rango de `dependencies` acepta la versión del hijo.
