import java.util.Scanner;
/* Juan Esteban Vidal Cabezas- Juan Felipe Niño Roberto- José Vicente Antonio de Jesús González Carrillo */

public class Main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        Evento evento = new Evento();
        GrupoMusical grupo = new GrupoMusical();
        Repertorio repertorio = new Repertorio();

        int opcion;
        int contadorMusicos = 0;

        System.out.println("=== REGISTRO DE MÚSICOS ===");

        // =============================
        // REGISTRO DE MUSICO
        // =============================

        do {

            System.out.println("\n1. Agregar músico");
            System.out.println("2. Terminar registro de músicos");
            opcion = sc.nextInt();
            sc.nextLine();

            if (opcion == 1) {

                System.out.println("Nombre del músico:");
                String nombreMusico = sc.nextLine();

                System.out.println("Rol del músico:");
                String rol = sc.nextLine();

                System.out.println("Años de experiencia:");
                int experiencia = sc.nextInt();
                sc.nextLine();

                // Crear instrumento
                Instrumento instrumento = new Instrumento();

                System.out.println("Nombre del instrumento:");
                String nombreInstrumento = sc.nextLine();

                System.out.println("Tipo de instrumento:");
                String tipoInstrumento = sc.nextLine();

                System.out.println("¿El instrumento requiere afinación? (true/false)");
                boolean requiereAfinacion = sc.nextBoolean();
                sc.nextLine();

                instrumento.setRequiereAfinacion(requiereAfinacion);
                instrumento.setAfinado(!requiereAfinacion);

                // Crear músico
                Musico musico = new Musico(instrumento);

                musico.setNombre(nombreMusico);
                musico.setRol(rol);
                musico.setExperienciaAnios(experiencia);

                grupo.agregarMusico(musico);

                contadorMusicos++;

                System.out.println("Músico agregado correctamente.");

            } 
            else if (opcion == 2 && contadorMusicos < 2) {

                System.out.println("El grupo debe tener mínimo 2 músicos.");
                opcion = 1;

            }

        } while (opcion != 2);

        // =============================
        // REGISTRO DE CANCIONES
        // =============================

        int contadorCanciones = 0;

        System.out.println("\n=== REGISTRO DE REPERTORIO ===");

        do {

            System.out.println("\n1. Agregar canción");
            System.out.println("2. Terminar repertorio");
            opcion = sc.nextInt();
            sc.nextLine();

            if (opcion == 1) {

                Cancion cancion = new Cancion();

                System.out.println("Título de la canción:");
                String titulo = sc.nextLine();

                System.out.println("Autor:");
                String autor = sc.nextLine();

                System.out.println("Duración en minutos:");
                int duracion = sc.nextInt();
                sc.nextLine();

                System.out.println("Género:");
                String genero = sc.nextLine();

                cancion.setTitulo(titulo);
                cancion.setAutor(autor);
                cancion.setDuracionMinutos(duracion);
                cancion.setGenero(genero);

                repertorio.agregarCancion(cancion);

                contadorCanciones++;

                System.out.println("Canción agregada.");

            } 
            else if (opcion == 2 && contadorCanciones < 1) {

                System.out.println("Debe agregar al menos una canción.");
                opcion = 1;

            }

        } while (opcion != 2);

        repertorio.calcularDuracionTotal();

        grupo.setRepertorio(repertorio);

        // =============================
        // ENSAYO
        // =============================

        System.out.println("\n=== ENSAYO DEL GRUPO ===");

        grupo.realizarEnsayo();

        for (Musico m : grupo.getListaMusicos()) {
            m.ensayar();
        }

        // =============================
        // EVENTO
        // =============================

        System.out.println("\n=== EVENTO DE XV AÑOS ===");

        evento.iniciar();

        grupo.iniciarEvento();

        System.out.println("\nLos músicos comienzan a tocar:");

        for (Musico m : grupo.getListaMusicos()) {
            m.tocar();
        }

        evento.finalizar();

        sc.close();
    }
}