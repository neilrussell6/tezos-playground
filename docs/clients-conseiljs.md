Clients : ConseilJS
===

ConseilJS does not interact directly with Tezos node,
instead it interacts via a deployed Conseil API eg.

```
https://conseil-dev.cryptonomic-infra.tech
https://conseil-prod.cryptonomic-infra.tech  
```

You provide server info when using ConseilJS like this:
```javascript
const serverInfo = {
  url: <CONSEIL_API_URL>,
  apiKey: <CONSEIL_API_KEY>,
}
```

### QUESTIONS

 - is it possible to setup a local instance of a Conseil server using Docker? are there docker images available?

Resources
---

 - [ConseilPy github](https://github.com/Cryptonomic/ConseilJS)
 - [ConseilPy docs](https://cryptonomic.github.io/ConseilJS)

Examples
---

 - [Web App](clients-conseiljs-webapp.md)
 - [Node CLI](clients-conseiljs-node-cli.md) (TODO)
