# 🏦 Análisis de Malas Prácticas — Proyecto CA-Banco (Cajero Automático)

> **Proyecto:** Sistema de Cajero Automático — Banco JVAG  
> **Tecnología:** Java SE · Swing (NetBeans GUI Builder)  
> **Paquete principal:** `Sistema`  
> **Propósito de este documento:** Identificar y justificar las malas prácticas de desarrollo detectadas en cada clase del proyecto, evaluadas desde los principios de la **Programación Orientada a Objetos (POO)** y los **Patrones de Diseño** más relevantes.

---

## 📋 Índice de Clases

| # | Clase | Tipo | Descripción breve |
|---|-------|------|-------------------|
| 1 | [`CuentaBancaria`](#1-cuentabancaria) | Modelo | Gestión del estado de la cuenta |
| 2 | [`persona`](#2-persona) | Modelo | Representación de un solicitante de préstamo |
| 3 | [`prestamo`](#3-prestamo) | Modelo | Entidad base del préstamo |
| 4 | [`principal`](#4-principal) | Controlador | Flujo de registro de préstamos por consola |
| 5 | [`Styles`](#5-styles) | Utilidad | Estilización de componentes Swing |
| 6 | [`Bienvenida`](#6-bienvenida) | Vista | Pantalla de inicio del cajero |
| 7 | [`Acceso`](#7-acceso) | Vista | Pantalla de ingreso de clave |
| 8 | [`Menu`](#8-menu) | Vista | Menú principal de operaciones |
| 9 | [`Deposito`](#9-deposito) | Vista | Operación de depósito |
| 10 | [`Retiro`](#10-retiro) | Vista | Operación de retiro |
| 11 | [`CambioAcceso`](#11-cambioaccceso) | Vista | Verificación previa al cambio de clave |
| 12 | [`Cambio`](#12-cambio) | Vista | Ingreso de nueva clave |
| 13 | [`CambioVerificar`](#13-cambioverificar) | Vista | Confirmación de la nueva clave |

---

## Estructura de cada análisis

Cada clase se analiza bajo la siguiente estructura uniforme:

```
📌 Rol en el sistema
⚠️ Malas prácticas identificadas (con justificación)
🔴 Principios POO vulnerados
🟡 Patrones de diseño relevantes omitidos o mal aplicados
```

---

---

## 1. `CuentaBancaria`

### 📌 Rol en el sistema
Actúa como modelo central del sistema. Almacena el saldo, la clave de acceso y los contadores de transacciones. Es accedida directamente por las vistas para realizar operaciones financieras.

---

### ⚠️ Malas Prácticas Identificadas

#### 1.1 — Uso de atributos y métodos exclusivamente estáticos (Clase utilitaria disfrazada de modelo)
```java
private static double saldo = 10000000.00;
private static String clave = "1234";
private static int retiros = 0;
private static int depositos = 0;
```
**Justificación:** Declarar todos los atributos como `static` convierte a la clase en un contenedor global de estado, lo que equivale a usar variables globales. Esto viola el principio de **encapsulamiento** de la POO, ya que el estado deja de estar ligado a una instancia concreta. En un sistema real, esto impediría gestionar múltiples cuentas simultáneamente, ya que todas compartirían la misma información. El diseño correcto sería instanciar `CuentaBancaria` como un objeto con estado propio.

---

#### 1.2 — Clave hardcodeada como valor por defecto en el código fuente
```java
private static String clave = "1234";
```
**Justificación:** Incluir credenciales por defecto directamente en el código fuente representa una vulnerabilidad de seguridad grave. Cualquier persona con acceso al repositorio conoce la clave inicial del sistema. Esto viola el principio de **ocultamiento de información** y la buena práctica de no almacenar secretos en texto plano dentro del código.

---

#### 1.3 — Saldo inicial hardcodeado
```java
private static double saldo = 10000000.00;
```
**Justificación:** Un sistema bancario real no inicializa el saldo directamente en el código. Este valor debería provenir de una fuente de datos externa (base de datos, archivo de configuración). Al ser estático y fijo, el saldo se reinicia cada vez que se ejecuta la aplicación, lo que hace al sistema completamente no persistente.

---

#### 1.4 — Ausencia de persistencia de datos
**Justificación:** Ninguna operación (depósito, retiro, cambio de clave) persiste en ningún medio de almacenamiento. Al cerrar la aplicación, todo el estado se pierde. Esto viola el principio de responsabilidad en el dominio del modelo: un modelo bancario debe garantizar la durabilidad de las transacciones.

---

#### 1.5 — Comentarios triviales que no aportan valor
```java
public static double getSaldo() {
    return saldo; //ver plata
}
```
**Justificación:** Comentarios como `//ver plata`, `//sumar`, `//ver pin` no describen el **por qué** de la lógica sino el **qué**, que ya es evidente en el código. Esta práctica contamina la legibilidad y refleja una cultura de documentación inmadura.

---

### 🔴 Principios POO Vulnerados
- **Encapsulamiento:** Estado global mediante `static` elimina el aislamiento de datos.
- **Abstracción:** La clase no modela adecuadamente el concepto de una cuenta bancaria real.
- **Principio de Responsabilidad Única (SRP):** La clase mezcla lógica de dominio con almacenamiento de estado global.

---

### 🟡 Patrones de Diseño Relevantes Omitidos
- **Singleton:** Si se desea una única instancia compartida, debería aplicarse el patrón Singleton con instanciación controlada en lugar de miembros estáticos directos.
- **Repository:** Para la persistencia, debería existir una capa de repositorio que separe el acceso a datos del modelo de dominio.

---

---

## 2. `persona`

### 📌 Rol en el sistema
Representa al solicitante de un préstamo. Extiende a `prestamo` para heredar los datos del crédito y agrega información personal del titular.

---

### ⚠️ Malas Prácticas Identificadas

#### 2.1 — Nombre de clase en minúscula (violación de convenciones Java)
```java
public class persona extends prestamo {
```
**Justificación:** Las convenciones de codificación de Java (Java Naming Conventions) establecen que los nombres de clases deben comenzar con mayúscula en formato **PascalCase**. El nombre `persona` debería ser `Persona`. Esto afecta directamente la legibilidad, la interoperabilidad con herramientas de análisis estático y la coherencia del proyecto, donde otras clases sí siguen la convención (`Menu`, `Deposito`, etc.).

---

#### 2.2 — Herencia semánticamente incorrecta (violación del principio "es-un")
```java
public class persona extends prestamo {
```
**Justificación:** La herencia en POO debe satisfacer la relación **"es-un"** (principio de Liskov). Una `persona` **no es** un `prestamo`; más bien, una persona **tiene** un préstamo. Esta relación debería modelarse mediante **composición**: la clase `Persona` debería tener un atributo de tipo `Prestamo`, no heredar de él. El uso incorrecto de herencia aquí genera un acoplamiento artificial entre conceptos del dominio que son distintos.

---

#### 2.3 — Atributo de teléfono inicializado con método separado en lugar del constructor
```java
public void setTelefonos(String telCasa, String telMovil) {
    this.telCasa = telCasa;
    this.telMovil = telMovil;
}
```
**Justificación:** Al no estar en el constructor, los atributos `telCasa` y `telMovil` quedan en estado `null` entre la construcción del objeto y la llamada a `setTelefonos`. Esto crea objetos en estados inconsistentes, lo que es una mala práctica en diseño OO. Se debería permitir pasar los teléfonos en el constructor, o al menos asignar valores por defecto en la definición.

---

#### 2.4 — Ausencia de validación de datos de entrada
**Justificación:** Los atributos como `id`, `nombre`, `apellido1` y `apellido2` no son validados en el constructor. Se acepta cualquier cadena incluyendo vacías o nulas, lo que puede producir objetos inconsistentes desde el momento de su creación.

---

### 🔴 Principios POO Vulnerados
- **Principio de Sustitución de Liskov (LSP):** Una `persona` no puede sustituir semánticamente a un `prestamo`.
- **Principio de Responsabilidad Única (SRP):** La clase mezcla datos personales con datos financieros de un préstamo.
- **Encapsulamiento:** El estado puede quedar incompleto al separar la inicialización en dos pasos.

---

### 🟡 Patrones de Diseño Relevantes Omitidos
- **Composición sobre Herencia:** `Persona` debería contener una referencia a `Prestamo`, no extenderla.
- **Builder:** Dado que el objeto tiene múltiples atributos opcionales (teléfonos), el patrón Builder permitiría una construcción más segura y legible.

---

---

## 3. `prestamo`

### 📌 Rol en el sistema
Clase base que encapsula los datos de un préstamo: número, valor, fechas de autorización, entrega y pagos. Calcula internamente el calendario de cuotas.

---

### ⚠️ Malas Prácticas Identificadas

#### 3.1 — Nombre de clase en minúscula (violación de convenciones Java)
```java
public class prestamo {
```
**Justificación:** Al igual que `persona`, el nombre debería ser `Prestamo` siguiendo las convenciones de nomenclatura de Java para clases.

---

#### 3.2 — Atributos `protected` en lugar de `private` con accesores
```java
protected int numeroPrestamo;
protected double valor;
protected LocalDate fechaAutorizacion;
```
**Justificación:** Declarar los atributos como `protected` expone el estado interno a cualquier subclase, rompiendo el **encapsulamiento**. En POO, el estado interno de una clase debe ser `private`, y el acceso controlado mediante getters y setters. El uso de `protected` aquí es especialmente problemático dado que `persona` hereda de `prestamo` de forma incorrecta (ver clase `persona`), amplificando el problema de exposición de estado.

---

#### 3.3 — Lógica de negocio con regla de negocio hardcodeada
```java
if (fechaAutorizacion.getDayOfMonth() > 20)
    throw new IllegalArgumentException("Los préstamos solo se autorizan en los primeros 20 días del mes.");
```
**Justificación:** La regla de negocio sobre el día límite de autorización (día 20) está hardcodeada dentro de la clase. Si esta regla cambia, se debe modificar el código fuente directamente. Debería extraerse a una constante nombrada o, idealmente, a un archivo de configuración o a una clase de política de negocio separada.

---

#### 3.4 — Cálculo de fechas de pago con lógica simplificada (30 días fijos)
```java
fechas.add(fechaEntrega.plusDays(30L * i));
```
**Justificación:** Los meses no tienen exactamente 30 días. Usar `plusDays(30)` en lugar de `plusMonths(1)` produce fechas de pago incorrectas que no coinciden con meses calendario reales. Esta es una imprecisión en la lógica de dominio financiero que puede generar errores en la práctica.

---

#### 3.5 — Ausencia de clase de excepciones personalizada
**Justificación:** Se lanza `IllegalArgumentException` con mensajes de texto. Para un sistema financiero, es preferible definir excepciones personalizadas (p. ej. `PrestamoInvalidoException`) que permitan un manejo de errores más granular y semánticamente significativo.

---

### 🔴 Principios POO Vulnerados
- **Encapsulamiento:** Atributos `protected` exponen innecesariamente el estado interno.
- **Principio Abierto/Cerrado (OCP):** Las reglas de negocio hardcodeadas obligan a modificar la clase para cambios de política.

---

### 🟡 Patrones de Diseño Relevantes Omitidos
- **Template Method:** Si se prevén distintos tipos de préstamos (personal, hipotecario), el cálculo de fechas podría definirse como método plantilla en la clase base.
- **Strategy:** La política de autorización (restricción por día del mes) podría encapsularse en una estrategia intercambiable.

---

---

## 4. `principal`

### 📌 Rol en el sistema
Clase de punto de entrada para el flujo de registro de préstamos por consola. Instancia objetos de tipo `persona`, los agrega a una lista y muestra un resumen al final.

---

### ⚠️ Malas Prácticas Identificadas

#### 4.1 — Nombre de clase en minúscula (violación de convenciones Java)
```java
public class principal {
```
**Justificación:** Debería denominarse `Principal` según las convenciones de nomenclatura de Java.

---

#### 4.2 — Lógica de aplicación completamente dentro de `main`
```java
public static void main(String[] args) {
    // +50 líneas de lógica de negocio, E/S y control de flujo
}
```
**Justificación:** El método `main` debería ser un punto de arranque mínimo que delegue inmediatamente a otras clases. Concentrar toda la lógica —lectura de datos, validaciones, creación de objetos, control de flujo— en `main` genera un método con múltiples responsabilidades, difícil de probar y de mantener. Viola directamente el **Principio de Responsabilidad Única (SRP)**.

---

#### 4.3 — Variable `completos` con lógica de flujo confusa
```java
System.out.print("Presione la tecla ENTER para seguir con el proceso");
boolean completos = sc.nextLine().equalsIgnoreCase("s");
```
**Justificación:** El mensaje indica al usuario que presione ENTER, pero la variable `completos` evalúa si la respuesta fue `"s"`. Esto es contradictorio: si el usuario presiona ENTER (respuesta vacía), `completos` será `false`, aunque el mensaje no solicitó ninguna opción. Esta inconsistencia entre el mensaje mostrado y la lógica de evaluación es un error de diseño de interfaz de usuario que puede confundir al operador.

---

#### 4.4 — Constante `LIMITE_TOTAL` definida como variable local
```java
double LIMITE_TOTAL = 1_000_000;
```
**Justificación:** Una constante debería declararse como `static final` a nivel de clase, no como variable local dentro de `main`. Usar el estilo de nombre en mayúsculas (`LIMITE_TOTAL`) para una variable local es además contradictorio con la convención Java (las variables locales van en `camelCase`).

---

#### 4.5 — Mezcla de interfaz de consola con instanciación de vista Swing
```java
Menu menu = new Menu();
menu.setLocationRelativeTo(null);
menu.setVisible(true);
```
**Justificación:** Al finalizar el flujo de consola, `principal` instancia directamente una ventana Swing. Esto mezcla dos paradigmas de interfaz de usuario (consola y GUI) dentro de la misma clase, generando un fuerte acoplamiento entre el módulo de préstamos y la capa de presentación gráfica. La transición entre sistemas debería gestionarse mediante un controlador o coordinador externo.

---

#### 4.6 — Ausencia de separación entre capas (todo en una sola clase)
**Justificación:** La clase `principal` asume simultáneamente los roles de: controlador de flujo, lector de entrada (Scanner), validador de datos, creador de objetos y presentador de resultados. Esto viola tanto el SRP como el principio de separación de capas (presentación, negocio, datos).

---

### 🔴 Principios POO Vulnerados
- **Principio de Responsabilidad Única (SRP):** La clase tiene demasiadas responsabilidades concentradas.
- **Principio de Inversión de Dependencias (DIP):** Depende directamente de clases concretas de vista (`Menu`) desde la lógica de negocio.

---

### 🟡 Patrones de Diseño Relevantes Omitidos
- **MVC (Model-View-Controller):** Debería existir un controlador que coordine la interacción entre el modelo (`persona`, `prestamo`) y la vista (consola o GUI), sin que ninguno de los dos lados conozca al otro directamente.
- **Command:** Cada operación del menú podría encapsularse como un comando ejecutable, facilitando la extensión y el deshacer/rehacer de operaciones.

---

---

## 5. `Styles`

### 📌 Rol en el sistema
Clase utilitaria que aplica estilos visuales globales a los componentes `JOptionPane` mediante el `UIManager` de Swing.

---

### ⚠️ Malas Prácticas Identificadas

#### 5.1 — Método con visibilidad de paquete en lugar de `public`
```java
void aplicarEstiloJOptionPane() {
```
**Justificación:** El método no tiene modificador de acceso explícito, lo que le da visibilidad de paquete por defecto. Si la intención es que otras clases lo usen (como lo hace `Bienvenida`), debería ser `public`. La omisión del modificador parece ser un descuido más que una decisión deliberada de diseño.

---

#### 5.2 — Clase instanciable cuando debería ser estática o de utilidad
```java
Styles styles = new Styles();
styles.aplicarEstiloJOptionPane();
```
**Justificación:** La clase `Styles` no tiene estado de instancia significativo (sus atributos `COLOR_*` son constantes de instancia). Al no requerir estado por objeto, debería diseñarse como clase de utilidad con método estático, o aplicarse directamente en un bloque de inicialización estática. Crear una instancia de `Styles` solo para llamar un método es un desperdicio de recursos y genera confusión sobre el propósito de la clase.

---

#### 5.3 — Los estilos se aplican de forma inconsistente en el sistema
**Justificación:** `aplicarEstiloJOptionPane()` solo es invocada en `Bienvenida`, no en el resto de las vistas. Esto produce una experiencia visual inconsistente donde algunas pantallas tienen un estilo personalizado y otras usan el aspecto por defecto de Swing.

---

#### 5.4 — Constantes de color declaradas como `private final` de instancia
```java
private final Color COLOR_FONDO_CLARO = new Color(245, 250, 255);
```
**Justificación:** Al ser valores que no cambian y no dependen del estado de ningún objeto, estas constantes deberían declararse como `private static final` para evitar que se creen nuevas instancias de `Color` con cada instanciación de `Styles`.

---

### 🔴 Principios POO Vulnerados
- **Principio de Responsabilidad Única (SRP):** Bien enfocada en estilos, pero su diseño como clase instanciable es innecesariamente complejo.
- **Encapsulamiento:** La visibilidad por defecto del método no comunica claramente la intención de acceso.

---

### 🟡 Patrones de Diseño Relevantes Omitidos
- **Singleton o clase de utilidad estática:** Para aplicar estilos globales, un método estático o un Singleton de tema visual sería más apropiado.
- **Facade:** `Styles` podría funcionar como una fachada que exponga una API limpia para aplicar temas al sistema completo.

---

---

## 6. `Bienvenida`

### 📌 Rol en el sistema
Primera pantalla que ve el usuario. Muestra el nombre del banco y ofrece el punto de entrada al cajero, además de accesos directos a videos explicativos del proyecto.

---

### ⚠️ Malas Prácticas Identificadas

#### 6.1 — URLs de video hardcodeadas en el código fuente
```java
String url = "https://youtu.be/DBJTuK9cgn4";
```
**Justificación:** Las URLs son recursos externos que pueden cambiar. Incrustarlas directamente en el código fuente obliga a recompilar la aplicación cada vez que cambie el enlace. Deberían estar en un archivo de propiedades o constantes configurables externamente.

---

#### 6.2 — Temporizador de video basado en tiempo estimado, no en evento real
```java
private void TemporizadorVideo(int segundos) {
    new javax.swing.Timer(duracionEnMilisegundos, ...).start();
}
```
**Justificación:** El temporizador no detecta cuándo el video realmente termina; simplemente espera un tiempo fijo y luego muestra un mensaje. Esto produce falsos positivos (el mensaje aparece aunque el video esté pausado o el usuario haya cerrado el navegador) y es una aproximación técnicamente incorrecta del problema.

---

#### 6.3 — Nombre de método con inicial en mayúscula (violación de convenciones)
```java
private void TemporizadorVideo(int segundos) {
```
**Justificación:** En Java, los métodos deben nombrarse en `camelCase` comenzando con minúscula. `TemporizadorVideo` debería ser `temporizadorVideo`. Esta inconsistencia también se repite en la clase `Menu`.

---

#### 6.4 — `jLabel5` declarado pero nunca agregado al layout visible
**Justificación:** En el código generado por el Form Editor, `jLabel5` es instanciado pero nunca es integrado correctamente al panel visible. Esto genera componentes huérfanos que consumen memoria sin propósito.

---

#### 6.5 — Botón de video dentro de una pantalla de cajero automático
**Justificación:** Un cajero automático no debería incluir botones para reproducir videos de YouTube. Esta funcionalidad responde a necesidades académicas del proyecto, pero rompe la coherencia del modelo de dominio. Si se mantiene, debería estar completamente separada de la interfaz operativa del cajero.

---

### 🔴 Principios POO Vulnerados
- **Principio de Responsabilidad Única (SRP):** La pantalla de bienvenida mezcla la función de punto de entrada con la reproducción de contenido multimedia externo.
- **Principio Abierto/Cerrado (OCP):** Las URLs hardcodeadas impiden extensión sin modificación.

---

### 🟡 Patrones de Diseño Relevantes Omitidos
- **MVC:** La lógica de navegación (abrir la pantalla de acceso, abrir URLs) está directamente en la vista sin ningún controlador intermediario.
- **Observer:** Para manejar el evento de finalización del video, debería usarse algún mecanismo de notificación real en lugar de un temporizador simulado.

---

---

## 7. `Acceso`

### 📌 Rol en el sistema
Pantalla de ingreso de clave PIN de 4 dígitos. Implementa un teclado numérico virtual que reemplaza al teclado físico para mayor seguridad.

---

### ⚠️ Malas Prácticas Identificadas

#### 7.1 — Teclado numérico con botones de numeración no secuencial
**Justificación:** Los botones `jButton1` a `jButton23` están asignados a dígitos de forma no intuitiva (`jButton1` = 7, `jButton2` = 4, etc.). Esto se debe al orden en que el Form Editor de NetBeans genera los componentes. Aunque funciona, hace el código extremadamente difícil de leer y mantener, ya que no hay una correspondencia clara entre el nombre del botón y su función.

---

#### 7.2 — Clave comparada directamente en la vista
```java
if (claveIngresada.equals(CuentaBancaria.getClave())) {
```
**Justificación:** La lógica de autenticación debería residir en una capa de negocio o controlador, no en la clase de la vista. Al colocar la validación directamente en `Acceso`, se viola el principio de separación de responsabilidades: la vista no debería saber cómo se valida la autenticación, solo debería delegar esa decisión.

---

#### 7.3 — Navegación entre ventanas acoplada directamente en los eventos
```java
Menu menu = new Menu();
menu.setLocationRelativeTo(null);
menu.setVisible(true);
this.dispose();
```
**Justificación:** Este patrón de "crear la siguiente ventana y cerrar la actual" se repite en todas las clases de vista. Al estar directamente en los manejadores de eventos, se genera un fuerte acoplamiento entre pantallas. Cualquier cambio en el flujo de navegación requiere modificar múltiples clases.

---

#### 7.4 — Componente `jButton13` instanciado pero nunca usado
```java
jButton13 = new javax.swing.JButton();
// ...nunca se agrega al panel ni se le asigna función
```
**Justificación:** `jButton13` es declarado, instanciado e incluido en las variables de la clase, pero jamás se agrega a ningún contenedor ni se le asigna ninguna acción. Es un artefacto residual del diseño con el Form Editor que ocupa memoria innecesariamente.

---

### 🔴 Principios POO Vulnerados
- **Separación de responsabilidades:** La vista ejecuta lógica de autenticación.
- **Principio de Responsabilidad Única (SRP):** La clase gestiona UI, validación de negocio y navegación simultáneamente.

---

### 🟡 Patrones de Diseño Relevantes Omitidos
- **MVC:** Un controlador de autenticación debería intermediar entre la vista y el modelo `CuentaBancaria`.
- **Navigator / Router:** Un coordinador de navegación central evitaría el acoplamiento directo entre pantallas.

---

---

## 8. `Menu`

### 📌 Rol en el sistema
Pantalla principal post-autenticación. Presenta las opciones del cajero: consulta de saldo, préstamo, depósito, retiro, cambio de clave y cancelación.

---

### ⚠️ Malas Prácticas Identificadas

#### 8.1 — Consulta de saldo con formato de 5 decimales innecesarios
```java
DecimalFormat formato = new DecimalFormat("#,##0.00000");
String saldoPrint = formato.format(CuentaBancaria.getSaldo());
```
**Justificación:** Los saldos bancarios se presentan con 2 decimales como máximo. Mostrar 5 decimales (`$10,000,000.00000`) genera confusión al usuario y no corresponde con las convenciones monetarias estándar. El formato correcto sería `"#,##0.00"`, o mejor aún, usar `NumberFormat.getCurrencyInstance()` como hacen las clases `Deposito` y `Retiro`.

---

#### 8.2 — Integración de módulo de préstamos (consola) llamada desde un evento GUI
```java
String[] args = {};
principal.main(args);
```
**Justificación:** Llamar directamente al método `main` de otra clase desde un manejador de eventos Swing es una práctica aberrante. El método `main` abre un `Scanner` en `System.in`, lo que bloquea el hilo de despacho de eventos de Swing (EDT — Event Dispatch Thread), congelando potencialmente la interfaz gráfica. Esto demuestra una mezcla indebida entre la interfaz de consola y la interfaz gráfica sin ningún mecanismo de separación de hilos.

---

#### 8.3 — Duplicación del método `TemporizadorVideo` en múltiples clases
```java
private void TemporizadorVideo(int segundos) { ... }
```
**Justificación:** Este método aparece tanto en `Bienvenida` como en `Menu` con lógica idéntica. La duplicación de código viola el principio **DRY (Don't Repeat Yourself)** y es una señal clara de que esta funcionalidad debería estar centralizada en la clase `Styles` o en una clase utilitaria dedicada.

---

#### 8.4 — Nombre de método con inicial mayúscula (convención)
```java
private void TemporizadorVideo(int segundos) {
```
**Justificación:** Igual que en `Bienvenida`, el nombre del método viola las convenciones de Java para métodos.

---

### 🔴 Principios POO Vulnerados
- **DRY (Don't Repeat Yourself):** Código duplicado entre `Menu` y `Bienvenida`.
- **Principio de Responsabilidad Única (SRP):** El menú gestiona UI, formato de datos, apertura de módulos de consola y reproducción de video.
- **Principio de Responsabilidad Única (hilo):** Se bloquea el EDT al llamar a `principal.main()`.

---

### 🟡 Patrones de Diseño Relevantes Omitidos
- **Command:** Cada opción del menú (consultar, depositar, retirar) debería encapsularse como un comando, facilitando agregar nuevas operaciones sin modificar el menú.
- **Facade:** El acceso al módulo de préstamos debería ir a través de una fachada que encapsule la lógica de transición entre consola y GUI.

---

---

## 9. `Deposito`

### 📌 Rol en el sistema
Pantalla para realizar depósitos en la cuenta. Permite ingresar un monto numérico mediante teclado virtual y seleccionar el tipo de depósito (Cheque o Efectivo).

---

### ⚠️ Malas Prácticas Identificadas

#### 9.1 — `tipoDeposito` declarado como variable de instancia dentro del bloque de eventos
```java
private String tipoDeposito;
```
**Justificación:** La variable `tipoDeposito` es declarada en medio del archivo de código, fuera del bloque de declaraciones estándar de la clase, dentro de la sección de manejadores de eventos generada por NetBeans. Esto dificulta la lectura y el mantenimiento, ya que los atributos deben estar declarados al principio de la clase.

---

#### 9.2 — El ComboBox se inicializa en el constructor con `addItem` en lugar de un modelo
```java
jComboBox1.addItem("Cheque");
jComboBox1.addItem("Efectivo");
```
**Justificación:** Las opciones de un `JComboBox` deberían gestionarse mediante un `ComboBoxModel` o al menos definirse desde una fuente de datos centralizada (lista de constantes o enum). El uso directo de `addItem` en el constructor con cadenas literales hace el código frágil ante cambios futuros en los tipos de depósito.

---

#### 9.3 — La validación del depósito no verifica que se haya seleccionado un tipo
```java
JOptionPane.showMessageDialog(this, "Deposito de " + tipoDeposito + " exitoso.");
```
**Justificación:** Si el usuario no interactúa con el `JComboBox` antes de aceptar, `tipoDeposito` puede ser `null` (si el evento `jComboBox1ActionPerformed` no fue disparado), causando que el mensaje muestre `"Deposito de null exitoso."`. No existe validación previa que garantice que el tipo de depósito haya sido seleccionado.

---

#### 9.4 — Lógica de validación con visibilidad `public` sin necesidad
```java
public void validarDeposito() {
```
**Justificación:** El método `validarDeposito` es declarado `public`, pero solo es llamado desde dentro de la misma clase. Debería ser `private` para respetar el principio de mínima exposición. La visibilidad pública expone innecesariamente la lógica interna de la vista.

---

### 🔴 Principios POO Vulnerados
- **Encapsulamiento:** Método de validación `public` expuesto sin necesidad.
- **Principio de Responsabilidad Única (SRP):** La vista gestiona validación de negocio, formato de moneda, navegación y control de UI.

---

### 🟡 Patrones de Diseño Relevantes Omitidos
- **MVC:** La validación del monto debería delegarse a un controlador o servicio.
- **Enum + ComboBoxModel:** Los tipos de depósito deberían modelarse con un `enum` (`TipoDeposito.CHEQUE`, `TipoDeposito.EFECTIVO`) alimentando el modelo del combo.

---

---

## 10. `Retiro`

### 📌 Rol en el sistema
Pantalla para realizar retiros de efectivo. Funcionalmente análoga a `Deposito`, permite ingresar un monto y valida contra el saldo disponible.

---

### ⚠️ Malas Prácticas Identificadas

#### 10.1 — Código casi idéntico al de `Deposito` (violación del principio DRY)
**Justificación:** Las clases `Retiro` y `Deposito` comparten: la misma estructura de teclado numérico virtual, el mismo método `escribirNumero`, el mismo método de borrar carácter, el mismo botón de punto decimal, y el mismo formato de moneda. Esta duplicación masiva indica que debería existir una clase base abstracta o un componente reutilizable de "panel de ingreso de monto" que ambas clases utilicen, en lugar de copiar y pegar el código.

---

#### 10.2 — Lógica de validación con visibilidad `public` sin necesidad
```java
public void validarRetiro() {
```
**Justificación:** Igual que en `Deposito`, el método debería ser `private`.

---

#### 10.3 — Componente `jButton13` instanciado pero nunca usado (reutilización de artefacto)
**Justificación:** Al igual que en `Acceso`, `Cambio`, `CambioAcceso` y `CambioVerificar`, el botón `jButton13` aparece declarado e instanciado pero nunca es usado. Este artefacto se repite en al menos 6 clases del proyecto, sugiriendo que fue copiado junto con el template y nunca fue eliminado.

---

### 🔴 Principios POO Vulnerados
- **DRY:** Duplicación extensa con `Deposito`.
- **Principio Abierto/Cerrado (OCP):** Cualquier cambio en el teclado numérico debe aplicarse manualmente en `Deposito`, `Retiro` y potencialmente otras clases.

---

### 🟡 Patrones de Diseño Relevantes Omitidos
- **Template Method:** Una clase abstracta `PantallaOperacion` podría definir el flujo general (mostrar teclado, validar monto, ejecutar operación, navegar de vuelta), dejando que `Deposito` y `Retiro` implementen solo la lógica específica de cada operación.
- **Composite / Custom Component:** El teclado numérico virtual podría encapsularse como un `JPanel` personalizado y reutilizable.

---

---

## 11. `CambioAcceso`

### 📌 Rol en el sistema
Primera pantalla del flujo de cambio de clave. Solicita la clave actual del usuario antes de permitir el ingreso de una nueva.

---

### ⚠️ Malas Prácticas Identificadas

#### 11.1 — Duplicación total con la clase `Acceso`
**Justificación:** `CambioAcceso` es prácticamente una copia de `Acceso`. Ambas muestran el mismo teclado numérico, tienen la misma restricción de 4 dígitos, el mismo botón de mostrar/ocultar clave y casi la misma lógica de validación. La única diferencia es la ventana a la que navegan tras la autenticación exitosa. Esta duplicación debería resolverse parametrizando el destino de navegación en una única clase reutilizable.

---

#### 11.2 — El label muestra el mismo mensaje que en `Acceso` ("CLAVE DE ACCESO POR DEFECTO ES 1234")
```java
jLabel2.setText("LA CLAVE DE ACCESO POR DEFECTO ES \"1234\"");
```
**Justificación:** Este mensaje es apropiado en la pantalla de inicio de sesión, pero en el flujo de cambio de clave resulta confuso e innecesario. Indica que el usuario ya conoce su clave, no que la clave por defecto sea 1234. El texto debería actualizarse contextualmente.

---

### 🔴 Principios POO Vulnerados
- **DRY:** Duplicación masiva con `Acceso`.
- **Principio de Responsabilidad Única (SRP):** Gestiona UI, validación y navegación.

---

### 🟡 Patrones de Diseño Relevantes Omitidos
- **Parámetro de estrategia / Callback:** `Acceso` y `CambioAcceso` podrían ser la misma clase configurada con diferentes estrategias de éxito (a dónde navegar si la clave es correcta).

---

---

## 12. `Cambio`

### 📌 Rol en el sistema
Segunda pantalla del flujo de cambio de clave. Solicita al usuario que ingrese la nueva clave de acceso deseada.

---

### ⚠️ Malas Prácticas Identificadas

#### 12.1 — La clave se cambia antes de ser confirmada
```java
CuentaBancaria.cambiarClave(claveIngresada); // Se aplica aquí...
// Abrir CambioVerificar para que el usuario confirme
```
**Justificación:** En `Cambio.validarClave()`, la nueva clave es **aplicada inmediatamente** al modelo antes de que el usuario la confirme en `CambioVerificar`. Esto significa que si el usuario cancela en la pantalla de verificación, la clave ya fue cambiada. La clase `CambioVerificar` intenta revertir esto llamando a `CuentaBancaria.cambiarClave("1234")` al cancelar, pero esta estrategia es frágil, errónea en diseño y crea una ventana de tiempo en que el sistema tiene una clave a medio confirmar.

---

#### 12.2 — Método `validarClave` con visibilidad `public` sin necesidad
```java
public void validarClave() {
```
**Justificación:** Igual que en `Deposito` y `Retiro`, el método debería ser `private`.

---

#### 12.3 — Error tipográfico en el mensaje al usuario
```java
"La nueva Clave dede cumplir con los siguientes parámetros:"
```
**Justificación:** La palabra "dede" es un error tipográfico de "debe". Aunque es un detalle menor, en un sistema financiero la comunicación con el usuario debe ser precisa y profesional.

---

### 🔴 Principios POO Vulnerados
- **Principio de Consistencia del Estado:** El modelo se modifica antes de completar la operación, dejando el sistema en un estado inconsistente durante el flujo de verificación.
- **Encapsulamiento:** Lógica de transacción sin atomicidad.

---

### 🟡 Patrones de Diseño Relevantes Omitidos
- **Memento:** Para implementar correctamente el cambio de clave, se debería guardar el estado anterior de la clave y solo confirmarlo una vez superada la verificación, revirtiéndolo en caso de cancelación.
- **Transacción (Unit of Work):** El cambio de clave debería tratarse como una operación atómica que solo se persiste al completarse exitosamente.

---

---

## 13. `CambioVerificar`

### 📌 Rol en el sistema
Tercera y última pantalla del flujo de cambio de clave. Solicita al usuario que repita la nueva clave para confirmar que fue ingresada correctamente.

---

### ⚠️ Malas Prácticas Identificadas

#### 13.1 — El label muestra texto incorrecto para el contexto
```java
jLabel1.setText("DIGITE SU CLAVE DE ACCESO");
jLabel2.setText("LA CLAVE DE ACCESO POR DEFECTO ES \"1234\"");
```
**Justificación:** Ambos textos pertenecen a la pantalla de inicio de sesión (`Acceso`) y no fueron actualizados para el contexto de confirmación de nueva clave. El label debería decir algo como "CONFIRME SU NUEVA CLAVE". Esto evidencia que la clase fue creada por duplicación sin adaptación adecuada al nuevo contexto.

---

#### 13.2 — Reversión de clave mediante hardcode al cancelar
```java
CuentaBancaria.cambiarClave("1234");
```
**Justificación:** Al cancelar en esta pantalla, la lógica restaura la clave a `"1234"` de forma hardcodeada. Esto es incorrecto porque: (a) asume que "1234" siempre fue la clave anterior, y (b) si el usuario ya había cambiado la clave antes, al cancelar la segunda operación pierde su clave real. La clave anterior debería haberse guardado antes de iniciar el flujo de cambio.

---

#### 13.3 — Triplicación del código de teclado numérico (Acceso + CambioAcceso + Cambio + CambioVerificar)
**Justificación:** Las cuatro pantallas que requieren entrada de clave PIN comparten exactamente el mismo código de teclado numérico, las mismas restricciones de longitud, el mismo botón de mostrar/ocultar y la misma lógica de borrado. Esto representa el caso más crítico de violación del principio **DRY** en todo el proyecto.

---

### 🔴 Principios POO Vulnerados
- **DRY:** Cuarta duplicación del mismo componente de teclado numérico.
- **Principio de Consistencia del Estado:** La reversión de la clave a "1234" puede dejar al sistema en un estado diferente al que tenía antes de iniciar el flujo.

---

### 🟡 Patrones de Diseño Relevantes Omitidos
- **Memento:** Para guardar y restaurar el estado anterior de la clave correctamente.
- **Custom Component (JPanel de teclado):** Un componente Swing reutilizable de teclado numérico PIN eliminaría la duplicación en las 4 clases que lo necesitan.
- **Wizard Pattern:** El flujo de 3 pasos (CambioAcceso → Cambio → CambioVerificar) podría modelarse como un asistente con estado compartido entre pasos, en lugar de 3 clases independientes que se comunican a través del modelo global.

---

---

## 📊 Resumen General de Malas Prácticas

| Categoría | Clases Afectadas | Frecuencia |
|-----------|-----------------|------------|
| Violación del principio DRY (código duplicado) | Acceso, Cambio, CambioAcceso, CambioVerificar, Retiro, Deposito | 🔴 Crítica |
| Ausencia de patrón MVC | Todas las vistas | 🔴 Crítica |
| Nombres de clase/método fuera de convención Java | persona, prestamo, principal, TemporizadorVideo | 🟠 Alta |
| Lógica de negocio en la capa de vista | Acceso, Deposito, Retiro, Cambio, CambioVerificar | 🟠 Alta |
| Herencia semánticamente incorrecta | persona → prestamo | 🟠 Alta |
| Estado global mediante campos estáticos | CuentaBancaria | 🟠 Alta |
| Componentes UI huérfanos (jButton13) | Acceso, Cambio, CambioAcceso, CambioVerificar, Deposito, Retiro | 🟡 Media |
| Datos hardcodeados (clave, saldo, URLs) | CuentaBancaria, Bienvenida | 🟡 Media |
| Ausencia de persistencia | CuentaBancaria | 🟡 Media |
| Inconsistencia de estado durante flujo de cambio de clave | Cambio, CambioVerificar | 🟡 Media |
| Comentarios triviales sin valor documental | CuentaBancaria | 🟢 Baja |

---

## 🛠️ Recomendaciones Generales

1. **Aplicar el patrón MVC** separando las clases en tres capas: Modelo (`CuentaBancaria`, `Prestamo`, `Persona`), Vista (todas las clases Swing), y Controlador (nuevas clases intermediarias).

2. **Crear un componente reutilizable de teclado PIN** (`PanelTecladoPin extends JPanel`) que centralice toda la lógica compartida por `Acceso`, `Cambio`, `CambioAcceso` y `CambioVerificar`.

3. **Aplicar un NavigationController** que centralice las transiciones entre pantallas, eliminando el acoplamiento directo entre vistas.

4. **Corregir la jerarquía de herencia** modelando `Persona` con una referencia a `Prestamo` (composición) en lugar de herencia.

5. **Agregar persistencia** mediante serialización, base de datos embebida (H2, SQLite) o archivos de propiedades para que el estado sobreviva entre sesiones.

6. **Implementar el patrón Memento** para el flujo de cambio de clave, garantizando que la operación sea atómica y reversible de forma segura.

---

> *Documento generado con fines de análisis académico. Proyecto: CA-Banco — Cajero Automático JVAG.*
