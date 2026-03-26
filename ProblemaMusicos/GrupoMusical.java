import java.util.ArrayList;
import java.util.List;

import java.util.ArrayList;
import java.util.List;

public class GrupoMusical {

    private int idGrupo;
    private String nombre;
    private String genero;
    private List<Musico> listaMusicos = new ArrayList<>();
    private Repertorio repertorio;

    public void agregarMusico(Musico m) {
        listaMusicos.add(m);
    }

    public void removerMusico(Musico m) {
        listaMusicos.remove(m);
    }

    public void iniciarEvento() {
        System.out.println("El grupo musical inicia su presentación");
    }

    public void realizarEnsayo() {
        System.out.println("El grupo musical está ensayando");
    }

    public List<Musico> getListaMusicos() {
        return listaMusicos;
    }

    public void setRepertorio(Repertorio repertorio) {
        this.repertorio = repertorio;
    }
}