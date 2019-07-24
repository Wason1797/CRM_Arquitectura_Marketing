
def get_campaign_clients(**kargs):

    from requests import get
    from datetime import datetime
    data = get('http://18.234.82.210:8081/clientes/{}/{}/{}/{}/{}/{}'.
               format(kargs.get('gender'), kargs.get('min_salary'), kargs.get('max_salary'),
                      kargs.get('location'), kargs.get('min_age'), kargs.get('max_age'))).json()

    for item in data:
        item['birth_date'] = datetime.fromisoformat(item['birth_date'])

    return data
    # return [
    #     {
    #         "location": {
    #             "provincia": "pichincha"
    #         },
    #         "email": "wabrborich@hotmail.com",
    #         "earnings": "270.00",
    #         "gender": "M",
    #         "birth_date": "1997-08-17",
    #         "dni": "1724561921",
    #         "full_name": "Wladymir Brborich"
    #     },
    #     {
    #         "location": {
    #             "provincia": "pichincha"
    #         },
    #         "email": "ssins@outlook.es",
    #         "earnings": "300.00",
    #         "gender": "M",
    #         "birth_date": "2019-07-01",
    #         "dni": "1802105641",
    #         "full_name": "Alexander Herrera"
    #     },
    #     {
    #         "location": {
    #             "provincia": "pichincha"
    #         },
    #         "email": "wbrborich@hotmail.com",
    #         "earnings": "700.00",
    #         "gender": "M",
    #         "birth_date": "2019-07-01",
    #         "dni": "1724561922",
    #         "full_name": "Alexander Mejia"
    #     }
    # ]


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


def get_list_chunks(_list, size):

    for i in range(0, size):
        yield _list[i::size]


def get_file_from_s3_service(url):
    from requests import get
    data = get(url)
    path = url.split('%2F')[-1].split('/')[0]
    open(path, 'wb').write(data.content)
    return path
