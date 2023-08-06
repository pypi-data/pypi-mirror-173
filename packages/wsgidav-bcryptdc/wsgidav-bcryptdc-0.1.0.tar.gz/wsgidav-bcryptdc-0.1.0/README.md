# wsgidav-bcryptdc

An implementation of the [wsgidav](https://wsgidav.readthedocs.io/en/latest/index.html) simple-dc that uses bcrypt hashes instead of plain text passwords.


## Installation

Install bcrypt dependency (requires rust to be present, if i'm not mistaken)
```shell
$ pip install wsgidav-bcryptdc
```

## Configuration

Configuration is basically the same as for the [simple-dc](https://wsgidav.readthedocs.io/en/latest/user_guide_configure.html#simpledomaincontroller), with the exception that it uses the `bcrypt_dc` config key, and a `password_hash` property is used instead of `password`.

```yaml
# NOTE: only HTTP basic auth is supported, make sure your communication to the wsgidav service is using SSL encryption
http_authenticator:
    domain_controller: wsgidavbcryptdc.SimpleBcryptDomainController
    accept_basic: true
    accept_digest: false
    default_to_digest: false

bcrypt_dc:
    user_mapping:
        '*': # default user mapping for all shares
            'username':
                password_hash: '$2y$05$u5fxm.Fb0sW64j6bFLFoKuTki0/ZSymNSlEBFR03SHngCZBA56XIS' # bcrypt hash for 'top-secret'
                roles: ['admin']
```
