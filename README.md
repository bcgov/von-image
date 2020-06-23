# Docker images for Verified Organizations Network components

In support of VON a set of Docker images are published for running Hyperledger Indy components. The image repository is located [on Docker Hub](https://hub.docker.com/r/bcgovimages/von-image/).

The images variously include:

- [Hyperledger Indy SDK](https://github.com/hyperledger/indy-sdk) and Indy CLI
- [Hyperledger Indy Node](https://github.com/hyperledger/indy-node)
- [Python](https://www.python.org/)

These images help to support the following projects:

- [von-network](https://github.com/bcgov/von-network)
- [The OrgBook](https://github.com/bcgov/TheOrgBook)
- [Aries CloudAgent Python (ACA-Py)](https://github.com/hyperledger/aries-cloudagent-python)
- [GreenLight](https://github.com/bcgov/greenlight)
- [VON Agent Template](https://github.com/bcgov/von-agent-template)
- [von-x](https://github.com/PSPC-SPAC-buyandsell/von-x)

## Indy SDK images

The following images include Python 3.6, the Indy SDK library and Python wrapper, Indy CLI, and the `postgres_storage` wallet storage plugin.

| Image tag         | indy-sdk version           | python version             |
|-------------------|----------------------------|----------------------------|
| py36-1.11-1       | 1.11.1                     | 3.6.9                      |
| py36-1.11-0       | 1.11.0                     | 3.6.9                      |
| py36-1.10-0       | 1.10.1                     | 3.6.8                      |
| py36-1.9-0        | 1.9.0                      | 3.6.8                      |

## Indy Node images

These images include the Indy Node library for hosting an Indy ledger node or pool. Also included are Python 3.5, the Indy SDK library and Python wrapper, Indy CLI, and the `postgres_storage` wallet storage plugin. They form the basis of `von-network`.

| Image tag         | indy-node version          | indy-sdk version           | python version             |
|-------------------|----------------------------|----------------------------|----------------------------|
| node-1.12-3       | 1.12.3                     | 1.15.0                     | 3.6.9                      |
| node-1.12-2       | 1.12.2                     | 1.14.1                     | 3.6.9                      |
| node-1.9-4        | 1.9.2 (gettext added)      | 1.11.1                     | 3.5.7                      |
| node-1.9-3        | 1.9.2                      | 1.11.1                     | 3.5.7                      |
| node-1.9-2        | 1.9.0                      | 1.11.0                     | 3.5.7                      |
| node-1.9-1        | 1.9.0                      | 1.10.1                     | 3.5.6                      |
| node-1.9-0        | 1.9.0                      | 1.8.3                      | 3.5.6                      |

## Indy SDK 1.8 images (out-dated)

The following images have `py35-` variants for Indy Node containers such as `von-network`, as well as `py36-` images for more common usage. Each image includes both Indy SDK and Indy Node.

| Image tag       | indy-sdk version           | indy-node version       |
|-----------------|----------------------------|-------------------------|
| 1.8-4           | 1.8.3                      | 1.7.0.dev902            |
| 1.8-3           | 1.8.2                      | 1.7.0.dev902            |
| 1.8-2           | 1.8.2                      | dev-1.6.876             |
| 1.8-1           | 1.8.1-dev-1033             | dev-1.6.862             |
| 1.8-0           | 1.8.0                      | dev-1.6.636             |

## Historical images

Images with `-ew-` included in the version tag include the `postgres_storage` Enterprise Wallet storage plugin for `indy-sdk`. Also included are the following Python libraries:

- [von-anchor](https://github.com/PSPC-SPAC-buyandsell/von_anchor)
- [von-x](https://github.com/PSPC-SPAC-buyandsell/von-x)
- [didauth](https://github.com/PSPC-SPAC-buyandsell/didauth)

### OpenShift compatibility

Starting with `1.8-4` all images are compatible with OpenShift.  Prior to `1.8-4` only the `s2i` images were compatible with OpenShift, including configuration for building and deploying on OpenShift using the source-to-image builds.

### Two Python versions:

The `py35-*` images are intended for running `indy-node` containers such as `von-network`. For other usage `py36-*` is recommended.

| Image tag       | indy-sdk                   | von_anchor  | von-x       | didauth     | indy-node       |
|-----------------|----------------------------|-------------|-------------|-------------|-----------------|
| 1.7-ew-0        | 1.7.0 with postgres plugin | 1.7.1       | 1.4.7       | 1.2.3       | dev-1.6.636     |
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


# Rocket.Chat Notifications from your Docker Hub repository:

Refer to [Incoming WebHook Scripting](https://rocket.chat/docs/administrator-guides/integrations/) for information on how to setup an incoming WebHook in Rocket.Chat.

Use [rocket.chat.integration.js](./scripts/rocket.chat.integration.js) for the **Script** associated with the WebHook integration.

On the WebHook tab of your Docker Hub repository, add a new WebHook and use the generated **WebHook URL** from the Rocket.Chat integration.

The payload of the Docker WebHook is not well documented, a recent (2019.04.08) sample can be found here; [DockerHubWebhookPayloadExample.json](./scripts/DockerHubWebhookPayloadExample.json).

To get a more up to date sample you can use [rocket.chat.capturepayload.js](./scripts/rocket.chat.capturepayload.js) as the script for the Rocket.Chat integration.  This will print out the json blob POSTed by the WebHook.
