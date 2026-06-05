# Skill: NullPointerException

## Qué es
Se lanza cuando el código intenta usar una referencia que apunta a `null` — acceder a un campo, invocar un método o acceder a un índice de array sobre un objeto no inicializado.

## Causas frecuentes en nivel intermedio

- Retorno de método que puede ser `null` usado sin verificar:
  ```java
  String nombre = mapa.get("clave"); // puede ser null
  int len = nombre.length();         // NPE si la clave no existe
  ```

- Objeto declarado pero no instanciado:
  ```java
  List<String> lista;
  lista.add("item"); // NPE — falta new ArrayList<>()
  ```

- Encadenamiento de llamadas sin guardia:
  ```java
  usuario.getDireccion().getCiudad(); // NPE si getDireccion() retorna null
  ```

## Cómo corregirlo

Verificar antes de usar:
```java
if (nombre != null) {
    int len = nombre.length();
}
```

Usar `Optional` para retornos que pueden ser nulos:
```java
Optional<String> nombre = Optional.ofNullable(mapa.get("clave"));
nombre.ifPresent(n -> System.out.println(n.length()));
```

Para encadenamiento, romper en pasos y verificar cada eslabón.

## Cómo prevenirlo
- Inicializar siempre las colecciones en la declaración.
- Documentar qué métodos pueden retornar `null` y verificar en el caller.
- Preferir `Optional<T>` sobre retorno de `null` en métodos propios.
