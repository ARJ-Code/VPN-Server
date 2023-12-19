# VPN-Server

## Descripción

Este proyecto tiene como objetivo la creación de un servidor **VPN**, que sirva de intermediario en la comunicación entre el `cliente`
y el `servidor`. Se encuentran implementados los protocoles de red **TCP** y **UDP**, así como otras funcionalidades de la **VPN**, además de un `cliente` y un `servidor` de pruebas.

## Ejecución

Para ejecutar el proyecto debe contar un interprete de **Python** en su sistema operativo:

- Para iniciar el servidor **VPN**:

```
make run
```

- Para inicial el `cliente` de prueba:

```
make cliente protocol=<protocol_name>
```

- Para inicial el `servidor` de prueba:

```
make server protocol=<protocol_name>
```

Es posible que necesite ejecutar estos comandos con privilegios de administrador.

## Servidor VPN

Comandos y funcionalidades:

- `create_user <user> <password> <id_vlan>`: Crea un usuario nuevo.
- `remove_user <id>`: Elimina un usuario.
- `show_users`: Muestra los usuarios registrados.
- `start <protocol>`: Inicia el servidor con el protocolo establecido.
- `stop`: Detiene el servidor.
- `restrict_user <rule_name> <id_user> <dest_ip>`: Restringe el acceso de un usuario a una dirección ip.
- `restrict_vlan <rule_name> <id_vlan> <dest_ip>`: Restringe el accesos de todos los usuarios de una **VLAN**.
- `help`: Muestra información de los comandos.
- `exit`: Finaliza el programa.
