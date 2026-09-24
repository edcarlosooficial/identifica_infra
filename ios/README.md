# iOS / iPadOS

O iOS não permite distribuir um executável Unix genérico nem fazer varredura de rede irrestrita como em Linux.

Esta pasta contém uma amostra nativa em Swift usando `Network.framework`. Ela testa apenas host/porta explicitamente informados e deve ser incorporada a um projeto Xcode assinado.

Para uso corporativo mais profundo em dispositivos Apple, a edição completa deve trabalhar com mecanismos permitidos pelo ecossistema, como MDM e APIs administrativas.
