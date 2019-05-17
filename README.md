## Docker images for Verified Organizations Network components

# Included:
- [Hyperledger Indy-SDK](https://github.com/hyperledger/indy-sdk), along with `indy-node`, `indy-crypto`, `indy-cli`, `indy-plenum`, and `indy-anoncreds`
- [Python](https://www.python.org/) version 3.5 or 3.6
- [von-anchor](https://github.com/PSPC-SPAC-buyandsell/von_anchor)
- [von-x](https://github.com/PSPC-SPAC-buyandsell/von-x)
- [didauth](https://github.com/PSPC-SPAC-buyandsell/didauth)

# Two Python versions:
The `py35-*` images are intended for running `indy-node` containers such as `von-network`.
For other usage `py36-*` is recommended.

# OpenShift Compatibility:
Starting with `1.8-4` all images are compatible with OpenShift.  Prior to `1.8-4` only the `s2i` images were compatible with OpenShift.

# `s2i` images:
These images include configuration for building and deploying on OpenShift using the source-to-image builds.

# Enterprise Wallet images:
The `-ew-` images include the postgres-based Enterprise Wallet extensions to indy-sdk.

# Library versions:

| Image tag       | indy-sdk                   | von_anchor  | von-x       | didauth     | indy-node       |
|-----------------|----------------------------|-------------|-------------|-------------|-----------------|
| 1.8-4       | 1.8.3          | --      | --       | --       | 1.7.0.dev902     |
| 1.8-3       | 1.8.2          | --      | --       | --       | 1.7.0.dev902     |
| 1.8-2       | 1.8.2          | --      | --       | --       | dev-1.6.876     |
| 1.8-1       | 1.8.1-dev-1033 | --      | --       | --       | dev-1.6.862     |
| 1.8-0       | 1.8.0 | --      | --       | --       | dev-1.6.636     |
| 1.7-ew-0       | 1.7.0 with postgres plugin | 1.7.1      | 1.4.7       | 1.2.3       | dev-1.6.636     |
| 1.6-9           | 1.6.7                      | 1.6.33      | 1.4.2       | 1.2.2       | dev-1.6.636     |
| 1.6-8           | 1.6.7                      | 1.6.31      | 1.4.0       | 1.2.2       | dev-1.6.636     |
| 1.6-7           | 1.6.5                      | 1.6.28      | 1.4.0       | 1.2.2       | dev-1.4.463     |
| 1.6-6           | 1.6.5                      | 1.6.25      | 1.3.6       | 1.2.2       | dev-1.4.463     |
| 1.6-5           | 1.6.5                      | 1.6.25      | 1.3.4       | 1.2.1       | dev-1.4.463     |
| 1.6-4           | 1.6.5                      | 1.6.22      | 1.3.3       | 1.2.1       | dev-1.4.463     |
| 1.6-3           | 1.6.5                      | 1.6.20      | 1.3.3       | 1.2.1       | dev-1.4.463     |
| 1.6-2           | 1.6.2                      | 1.6.15      | 1.3.2       | 1.2.1       | dev-1.4.463     |
| 1.6-ew-13       | 1.6.7 with postgres plugin | 1.6.41      | 1.4.6       | 1.2.3       | dev-1.6.636     |
| 1.6-ew-12       | 1.6.7 with postgres plugin | 1.6.37      | 1.4.5       | 1.2.3       | dev-1.6.636     |
| 1.6-ew-11       | 1.6.7 with postgres plugin | 1.6.37      | 1.4.4       | 1.2.3       | dev-1.6.636     |
| 1.6-ew-10       | 1.6.7 with postgres plugin | 1.6.34      | 1.4.3       | 1.2.3       | dev-1.6.636     |
| 1.6-ew-9        | 1.6.7 with postgres plugin | 1.6.33      | 1.4.2       | 1.2.2       | dev-1.6.636     |
| 1.6-ew-7        | 1.6.5 with postgres plugin | 1.6.28      | 1.4.0       | 1.2.2       | dev-1.4.463     |
| 1.6-ew-4        | 1.6.5 with postgres plugin | 1.6.25      | 1.3.6       | 1.2.2       | dev-1.4.463     |
| 1.6-ew-3        | 1.6.5 with postgres plugin | 1.6.25      | 1.3.4       | 1.2.1       | dev-1.4.463     |
| 1.6-ew-2        | 1.6.5 with postgres plugin | 1.6.22      | 1.3.3       | 1.2.1       | dev-1.4.463     |
| 1.6-ew          | 1.6.5 with postgres plugin | 1.6.22      | 1.3.3       | 1.2.1       | dev-1.4.463     |

Source Dockerfiles are located on GitHub at [PSPC-SPAC-buyandsell/von-image](https://github.com/PSPC-SPAC-buyandsell/von-image).

# Rocket.Chat Notifications from your Docker Hub repository:

Refer to [Incoming WebHook Scripting](https://rocket.chat/docs/administrator-guides/integrations/) for information on how to setup an incoming WebHook in Rocket.Chat.

Use [rocket.chat.integration.js](./scripts/rocket.chat.integration.js) for the **Script** associated with the WebHook integration.

On the WebHook tab of your Docker Hub repository, add a new WebHook and use the generated **WebHook URL** from the Rocket.Chat integration.

The payload of the Docker WebHook is not well documented, a recent (2019.04.08) sample can be found here; [DockerHubWebhookPayloadExample.json](./scripts/DockerHubWebhookPayloadExample.json).

To get a more up to date sample you can use [rocket.chat.capturepayload.js](./scripts/rocket.chat.capturepayload.js) as the script for the Rocket.Chat integration.  This will print out the json blob POSTed by the WebHook.