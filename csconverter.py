import re


def findInCS(cs: str, key: str):
    fields = cs.split(";")
    for field in fields:
        if field.startswith(key):
            result = field.split("=", 1)  # password may have '='
            return result[-1]


class ConnectionString:
    def __init__(self,
                 server,
                 port,
                 database,
                 user,
                 password,
                 encrypt=True,
                 thrust_server_certificate=False,
                 timeout=30):
        self._server = server
        self.port = port
        self._database = database
        self._user = user
        self._password = password
        self._encrypt = encrypt
        self._thrust_server_certificate = thrust_server_certificate
        self._timeout = timeout

    @classmethod
    def from_odbc(cls, connectionstring):
        _server_port = findInCS(connectionstring, 'Server')
        _server = re\
            .search(r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]", _server_port)\
            .group(0)
        _port = _server_port.split(",")[-1]
        return cls(
            server=_server,
            port=_port,
            database=findInCS(connectionstring, 'Database'),
            user=findInCS(connectionstring, 'Uid'),
            password=findInCS(connectionstring, 'Pwd'),
            encrypt=findInCS(connectionstring, 'Encrypt') == 'yes',
            thrust_server_certificate=findInCS(connectionstring, 'TrustServerCertificate') == 'yes',
            timeout=int(findInCS(connectionstring, 'Connection Timeout'))
        )

    @classmethod
    def from_ado_net(cls, connectionstring):
        _server_port = findInCS(connectionstring, 'Server')
        _server = re \
            .search(r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]", _server_port) \
            .group(0)
        _port = _server_port.split(",")[-1]
        return cls(
            server=_server,
            port=_port,
            database=findInCS(connectionstring, 'Initial Catalog'),
            user=findInCS(connectionstring, 'User ID'),
            password=findInCS(connectionstring, 'Password'),
            encrypt=findInCS(connectionstring, 'Encrypt') == 'True',
            thrust_server_certificate=findInCS(connectionstring, 'TrustServerCertificate') == 'True',
            timeout=int(findInCS(connectionstring, 'Connection Timeout'))
        )

    @classmethod
    def from_jdbc(cls, connectionstring):
        _server_port = connectionstring.split(';')[0]
        _server = re \
            .search(r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]", _server_port) \
            .group(0)
        _port = _server_port.split(":")[-1]
        return cls(
            server=_server,
            port=_port,
            database=findInCS(connectionstring, 'database'),
            user=findInCS(connectionstring, 'user').split('@')[0],
            password=findInCS(connectionstring, 'password'),
            encrypt=findInCS(connectionstring, 'encrypt') == 'true',
            thrust_server_certificate=findInCS(connectionstring, 'thrustServerCertificate') == 'true',
            timeout=int(findInCS(connectionstring, 'loginTimeout'))
        )

    # Since one standard have fields others don't have, lets build minimal connectionStrings
    def to_odbc(self,
                driver="{ODBC Driver 13 for SQL Server}"):
        _result = f"Driver={driver};" \
                 f"Server=tcp:{self._server},{self.port};" \
                 f"Database={self._database};" \
                 f"Uid={self._user};" \
                 f"Pwd={self._password};" \
                 f"Encrypt={['no','yes'][self._encrypt]};" \
                 f"TrustServerCertificate={['no','yes'][self._thrust_server_certificate]};" \
                 f"Connection Timeout={self._timeout};"
        return _result