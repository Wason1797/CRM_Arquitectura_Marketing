/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ec.edu.espe.centralderiesgo.model;

import com.google.gson.Gson;
import java.math.BigDecimal;
import java.util.logging.Logger;

/**
 *
 * @author joel
 */
public class Persona {

    private static final Logger LOG = Logger.getLogger(Persona.class.getName());

    private String cedula;
    private String nombre;
    private String apellido;
    private BigDecimal deuda;

    public String getCedula() {
        return cedula;
    }

    public void setCedula(String cedula) {
        this.cedula = cedula;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getApellido() {
        return apellido;
    }

    public void setApellido(String apellido) {
        this.apellido = apellido;
    }

    public BigDecimal getDeuda() {
        return deuda;
    }

    public void setDeuda(BigDecimal deuda) {
        this.deuda = deuda;
    }

    public String obtenerStringPersona(Persona persona) {
        String personaStr = null;
        Gson gson = new Gson();
        try {
            personaStr = gson.toJson(persona);
        } catch (Exception ex) {
            LOG.severe(ex.toString());
        }
        return personaStr;
    }

    public Persona obtenerGsonPersona(String personaStr) {
        Persona persona = null;
        Gson gson = new Gson();
        if (personaStr != null && !personaStr.isEmpty()) {
            persona = gson.fromJson(personaStr, Persona.class);
        }
        return persona;
    }
}
