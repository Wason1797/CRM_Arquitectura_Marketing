/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ec.edu.espe.centralderiesgo.servicio;

import ec.edu.espe.centralderiesgo.dao.PersonaDAO;
import ec.edu.espe.centralderiesgo.model.Persona;
import java.io.Serializable;
import java.util.logging.Logger;
import javax.ejb.Stateless;

/**
 *
 * @author joel
 */
@Stateless
public class PersonaServicio implements Serializable {

    private static final Logger LOG = Logger.getLogger(PersonaServicio.class.getName());

    public Persona obtenerPersona(String cedula) {
        Persona persona = new Persona();
        try {
            PersonaDAO personaDAO = new PersonaDAO();
            persona = personaDAO.obtenerPersona(cedula);
            personaDAO.cerrarPool();
        } catch (Exception ex) {
            LOG.severe(ex.toString());
        }
        return persona;
    }

    public void agregarPersona(Persona persona) {
        try {
            PersonaDAO personaDAO = new PersonaDAO();
            personaDAO.agregarPersona(persona);
            personaDAO.cerrarPool();
        } catch (Exception ex) {
            LOG.severe(ex.toString());
        }
    }
}
