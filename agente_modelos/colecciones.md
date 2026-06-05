# Skill: Colecciones en Java

## Interfaces principales y sus implementaciones más usadas

| Interfaz | Implementación típica | Cuándo usarla |
|---|---|---|
| `List<E>` | `ArrayList` | Acceso por índice, orden importa |
| `Set<E>` | `HashSet` | Sin duplicados, orden no importa |
| `Map<K,V>` | `HashMap` | Pares clave-valor, búsqueda rápida |
| `Queue<E>` | `LinkedList` | Procesamiento FIFO |

## Errores frecuentes

Modificar una lista mientras se itera con for-each:
```java
for (String s : lista) {
    if (s.isEmpty()) lista.remove(s); // ConcurrentModificationException
}

// correcto: usar Iterator
Iterator<String> it = lista.iterator();
while (it.hasNext()) {
    if (it.next().isEmpty()) it.remove();
}
```

Usar `==` para comparar objetos en colecciones:
```java
// String en un Set se compara por equals(), no por ==
Set<String> set = new HashSet<>();
set.add("hola");
set.contains("hola"); // true — correcto
```

Olvidar implementar `equals()` y `hashCode()` en claves de `HashMap`:
```java
// Si Producto no sobreescribe equals/hashCode,
// dos objetos con los mismos datos son "distintos" para el mapa
Map<Producto, Integer> stock = new HashMap<>();
```

## Inicialización correcta

```java
// declarar con la interfaz, instanciar con la implementación
List<String> nombres = new ArrayList<>();
Map<String, Integer> edades = new HashMap<>();

// lista inmutable (Java 9+)
List<String> fijos = List.of("a", "b", "c");
```

## Recorrer un Map

```java
for (Map.Entry<String, Integer> entry : mapa.entrySet()) {
    System.out.println(entry.getKey() + " -> " + entry.getValue());
}
```
