# Android — Termux

A versão FREE para Android usa o mesmo núcleo Python via Termux.

```bash
pkg update
pkg install python
git clone https://github.com/edcarlosooficial/identifica_infra.git
cd identifica_infra
python mareo_mapper.py 192.168.1.0/24
```

O Android pode limitar acesso a informações de camada 2, portanto MAC/ARP depende do dispositivo e da versão do sistema.
