public class Instrumento {

    private int idInstrumento;
    private String nombre;
    private String tipo;
    private boolean requiereAfinacion;
    private boolean afinado;

    public void afinar() {

        if (requiereAfinacion) {
            afinado = true;
            System.out.println("El instrumento ha sido afinado");
        } else {
            System.out.println("Este instrumento no requiere afinación");
        }
    }

    public String getTipo() {
        return tipo;
    }

    public void setRequiereAfinacion(boolean requiereAfinacion) {
        this.requiereAfinacion = requiereAfinacion;
    }

    public void setAfinado(boolean afinado) {
        this.afinado = afinado;
    }

    public boolean isRequiereAfinacion() {
        return requiereAfinacion;
    }

    public boolean isAfinado() {
        return afinado;
    }
}