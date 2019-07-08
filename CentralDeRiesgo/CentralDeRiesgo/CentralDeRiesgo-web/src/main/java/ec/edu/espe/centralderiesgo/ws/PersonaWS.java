/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ec.edu.espe.centralderiesgo.ws;

import ec.edu.espe.centralderiesgo.model.Persona;
import ec.edu.espe.centralderiesgo.servicio.PersonaServicio;
import javax.ejb.EJB;
import javax.jws.Oneway;
import javax.jws.WebMethod;
import javax.jws.WebParam;
import javax.jws.WebService;

/**
 *
 * @author joel
 */
@WebService(serviceName = "PersonaWS")
public class PersonaWS {

    @EJB
    private PersonaServicio personaServicio;

    @WebMethod(operationName = "obtenerPersona")
    public Persona obtenerPersona(@WebParam(name = "cedula") String cedula) {
        return personaServicio.obtenerPersona(cedula);
    }

    @WebMethod(operationName = "agregarPersona")
    @Oneway
    public void agregarPersona(@WebParam(name = "persona") Persona persona) {
        personaServicio.agregarPersona(persona);
    }
    
}
