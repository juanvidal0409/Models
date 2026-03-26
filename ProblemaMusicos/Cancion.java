public class Cancion {

    private int idCancion;
    private String titulo;
    private String autor;
    private int duracionMinutos;
    private String genero;

    public void reproducir() {
        System.out.println("Reproduciendo canción: " + titulo);
    }

    public int getDuracion() {
        return duracionMinutos;
    }

    public void setTitulo(String titulo) {
        this.titulo = titulo;
    }

    public void setAutor(String autor) {
        this.autor = autor;
    }

    public void setDuracionMinutos(int duracionMinutos) {
        this.duracionMinutos = duracionMinutos;
    }

    public void setGenero(String genero) {
        this.genero = genero;
    }
}