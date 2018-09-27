# Docker images for Verified Organizations Network components

## Included:
- [Hyperledger Indy-SDK](https://github.com/hyperledger/indy-sdk), along with `indy-node`, `indy-crypto`, `indy-cli`, `indy-plenum`, and `indy-anoncreds`
- [Python](https://www.python.org/) version 3.5 or 3.6
- [von-anchor](https://github.com/PSPC-SPAC-buyandsell/von_anchor)
- [von-x](https://github.com/PSPC-SPAC-buyandsell/von-x)
- [didauth](https://github.com/PSPC-SPAC-buyandsell/didauth)

## Two Python versions:
The `py35-*` images are intended for running `indy-node` containers such as `von-network`.
For other usage `py36-*` is recommended.

## `s2i` images:
These images include configuration for building and deploying on OpenShift using source-to-image.

## `ew` images:
These images include the postgres-based Enterprise Wallet extensions to Indy-SDK.

## Library versions:

| Image tag       | Indy-SDK                   | von_anchor  | von-x       | didauth     |
|-----------------|----------------------------|-------------|-------------|-------------|
| 1.6-5           | 1.6.5                      | 1.6.25      | 1.3.4       | 1.2.1       |
| 1.6-4           | 1.6.5                      | 1.6.22      | 1.3.3       | 1.2.1       |
| 1.6-3           | 1.6.5                      | 1.6.20      | 1.3.3       | 1.2.1       |
| 1.6-2           | 1.6.2                      | 1.6.15      | 1.3.2       | 1.2.1       |
| 1.6-ew-3        | 1.6.5 with postgres plugin | 1.6.25      | 1.3.4       | 1.2.1       |
| 1.6-ew-2        | 1.6.5 with postgres plugin | 1.6.22      | 1.3.3       | 1.2.1       |
| 1.6-ew          | 1.6.5 with postgres plugin | 1.6.22      | 1.3.3       | 1.2.1       |

Source Dockerfiles are located on GitHub at [PSPC-SPAC-buyandsell/von-image](https://github.com/PSPC-SPAC-buyandsell/von-image).
