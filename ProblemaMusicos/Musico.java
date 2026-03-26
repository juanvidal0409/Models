public class Musico {

    private int idMusico;
    private String nombre;
    private String rol;
    private int experienciaAnios;
    private Instrumento instrumento;

    public Musico(Instrumento instrumento) {
        this.instrumento = instrumento;
    }

    public void tocar() {

        if (instrumento.isRequiereAfinacion() && !instrumento.isAfinado()) {
            instrumento.afinar();
        }

        System.out.println(nombre + " está tocando su instrumento");
    }

    public void ensayar() {
        System.out.println(nombre + " está ensayando");
    }

    public Instrumento getInstrumento() {
        return instrumento;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public void setRol(String rol) {
        this.rol = rol;
    }

    public void setExperienciaAnios(int experienciaAnios) {
        this.experienciaAnios = experienciaAnios;
    }
}