# Skill: Manejo de Excepciones

## Jerarquía relevante para nivel intermedio

```
Throwable
├── Error          (no manejar — JVM errors)
└── Exception
    ├── RuntimeException     (unchecked — no obliga try/catch)
    │   ├── NullPointerException
    │   ├── ArrayIndexOutOfBoundsException
    │   ├── ClassCastException
    │   └── IllegalArgumentException
    └── IOException          (checked — obliga try/catch o throws)
        └── FileNotFoundException
```

## Errores comunes

Capturar `Exception` genérica en lugar del tipo específico:
```java
// mal — oculta el tipo real del problema
try { ... } catch (Exception e) { e.printStackTrace(); }

// bien
try { ... } catch (FileNotFoundException e) {
    System.err.println("Archivo no encontrado: " + e.getMessage());
}
```

Bloque `catch` vacío — el error se silencia y el programa sigue con estado inválido:
```java
try { ... } catch (IOException e) {} // nunca hacer esto
```

Lanzar `Exception` genérica en lugar de un tipo adecuado:
```java
throw new Exception("valor inválido"); // mal
throw new IllegalArgumentException("valor inválido"); // bien
```

## Bloque finally y try-with-resources

Para recursos que deben cerrarse (streams, conexiones), usar try-with-resources:
```java
try (BufferedReader br = new BufferedReader(new FileReader("archivo.txt"))) {
    String linea = br.readLine();
} catch (IOException e) {
    e.printStackTrace();
}
// br se cierra automáticamente aunque haya excepción
```

## Crear excepciones personalizadas

```java
public class SaldoInsuficienteException extends RuntimeException {
    public SaldoInsuficienteException(double monto) {
        super("Saldo insuficiente para operar: " + monto);
    }
}
```
