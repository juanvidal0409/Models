import java.util.ArrayList;
import java.util.List;

public class Repertorio {

    private int idRepertorio;
    private int duracionTotal;
    private List<Cancion> listaCanciones = new ArrayList<>();

    public void agregarCancion(Cancion c) {
        listaCanciones.add(c);
    }

    public void eliminarCancion(Cancion c) {
        listaCanciones.remove(c);
    }

    public int calcularDuracionTotal() {

        int total = 0;

        for (Cancion c : listaCanciones) {
            total += c.getDuracion();
        }

        duracionTotal = total;
        return duracionTotal;
    }

    public List<Cancion> getListaCanciones() {
        return listaCanciones;
    }
}