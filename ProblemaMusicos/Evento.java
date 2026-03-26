import java.util.Date;

public class Evento {

    private int idEvento;
    private String tipo = "XV Años";
    private Date fecha;
    private String lugar;
    private int duracionHoras;

    public void iniciar() {
        System.out.println("El evento de XV años ha iniciado");
    }

    public void finalizar() {
        System.out.println("El evento ha finalizado");
    }
}