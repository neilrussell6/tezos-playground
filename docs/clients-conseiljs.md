Clients : ConseilJS
===

ConseilJS does not interact directly with Tezos node,
instead it interacts via a deployed Conseil API eg.

```
https://conseil-dev.cryptonomic-infra.tech
https://conseil-prod.cryptonomic-infra.tech  
```

You must provide the Tezos node when using ConseilJS not the above API ^.
Your local node must be publically accesible (TODO: how to get this working?)

Questions
---

 - is it possible to setup a local instance of a Conseil server using Docker? are there docker images available?
 - passing a localhost Tezos node to ConseilJS does not work, how to get this to work?

Issues
---

### Public Tezos nodes
for me this is working everytime:
```
https://rpcalpha.tzbeta.net
```
but this sometimes works sometimes fails
```
https://tezos-dev.cryptonomic-infra.tech
```
eg. this request
```
POST https://tezos-dev.cryptonomic-infra.tech/injection/operation?chain=main
```
 - sometimes returns 500 "TypeError: Failed to fetch"
 - and sometimes succeeds

Resources
---

 - [ConseilPy github](https://github.com/Cryptonomic/ConseilJS)
 - [ConseilPy docs](https://cryptonomic.github.io/ConseilJS)

Examples
---

 - [Web App](clients-conseiljs-webapp.md)
 - [Node CLI](clients-conseiljs-node-cli.md) (TODO)
