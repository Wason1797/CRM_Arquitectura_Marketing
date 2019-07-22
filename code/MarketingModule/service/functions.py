import jwt


def get_campaign_clients(**kargs):
    return [
        {
            "location": {
                "provincia": "pichincha"
            },
            "email": "wabrborich@hotmail.com",
            "earnings": "270.00",
            "gender": "M",
            "birth_date": "1997-08-17",
            "dni": "1724561921",
            "full_name": "Wladymir Brborich"
        },
        {
            "location": {
                "provincia": "pichincha"
            },
            "email": "ssins@outlook.es",
            "earnings": "300.00",
            "gender": "M",
            "birth_date": "2019-07-01",
            "dni": "1802105641",
            "full_name": "Alexander Herrera"
        },
        {
            "location": {
                "provincia": "pichincha"
            },
            "email": "wbrborich@hotmail.com",
            "earnings": "700.00",
            "gender": "M",
            "birth_date": "2019-07-01",
            "dni": "1724561922",
            "full_name": "Alexander Mejia"
        }
    ]


def decode_token(token):
    return jwt.decode(token[1], 'secrets', algorithms=['HS256'])


def get_person_from_risk_db(dni, ip):
    from zeep import Client
    from zeep.helpers import serialize_object
    wsdl = 'http://{}:8080/CentralDeRiesgo-web/PersonaWS?WSDL'.format(ip)

    client = Client(wsdl=wsdl)
    result = client.service.obtenerPersona(cedula=dni)
    result = serialize_object(result, target_cls=dict)

    return result


def calculate_risk(client, ip):
    salary = client.earnings
    debt = get_person_from_risk_db(client.dni, ip)['deuda']

    return 'HIG' if debt > salary*2 else 'MID' if debt >= salary else 'LOW'
