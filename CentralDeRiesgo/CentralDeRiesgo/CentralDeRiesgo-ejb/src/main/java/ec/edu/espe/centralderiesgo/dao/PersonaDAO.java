/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ec.edu.espe.centralderiesgo.dao;

import ec.edu.espe.centralderiesgo.model.Persona;
import java.util.logging.Logger;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

/**
 *
 * @author joel
 */
public class PersonaDAO {

    private static final Logger LOG = Logger.getLogger(PersonaDAO.class.getName());

    private final String redisHost = "localhost";
    private final Integer redisPort = 6379;
    private JedisPool jedisPool;
    private Jedis jedis;

    public PersonaDAO() {
        jedisPool = new JedisPool(redisHost, redisPort);
    }

    public void agregarPersona(Persona persona) {
        try {
            jedis = jedisPool.getResource();
            jedis.set(persona.getCedula(), new Persona().obtenerStringPersona(persona));
        } catch (Exception ex) {
            LOG.severe(ex.toString());
        } finally {
            if (jedis != null) {
                jedis.close();
            }
        }
    }

    public Persona obtenerPersona(String cedula) {
        Persona persona = null;
        try {
            jedis = jedisPool.getResource();
            persona = new Persona().obtenerGsonPersona(jedis.get(cedula));
        } catch (Exception ex) {
            LOG.severe(ex.toString());
        } finally {
            if (jedis != null) {
                jedis.close();
            }
        }
        return persona;
    }

    public void cerrarPool() {
        jedisPool.close();
    }
}
