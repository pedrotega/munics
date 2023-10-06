import paho.mqtt.client as mqtt
from threading import Thread
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
# RSA-OAEP Encrypting and decrypting
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import paho.mqtt.client as mqtt

# MQTT broker address and port
mqttBroker = "mqtt.eclipseprojects.io"
mqttBroker = "18.101.47.122"
password = "HkxNtvLB3GC5GQRUWfsA"
mqtt_id = "sinf"
port = 1883
ids = ["alpe", "si1", 'si2', 'si3']
my_id = ids[1]
#path = [my_id, "si1", "si2", "alpe", "alpe", "si2", "si3", "si3", "si1"]
#path = [my_id, "si2", "si2", "si1", "alpe", "si3", "alpe", "alpe", "si3", "si3"]
path = ["alpe", "si1", "alpe", 'alpe', 'jal', "jal", 'alpe', 'si2', 'jal']
anonymous = False


pubkeydictionary = {
	"alpe": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkh11pHrMUzT0D9E1WVLwMJ2Uu9KP/wQMelB2P0kw4CMR0+6kNDKUSbxF23Ksimd0f9TqgWCkAZ375RRynR1y1GSa+GHItnM9n5rWshBbUbqN7O/4PjHrGde97mSRgsryurKuOIiKy53BF/oTqa4NaNKFx3noLlSpp++Lla9Qtf9Hv6Nl5PDeSr/7V+Uate26vyZAliPzpvcq7FMEz4RwnBcYvq7qoGaKcQTMZaHENJKaX/jrMfQEBMDy2QDIU5EYE4POIbHsFmas/iT0kDvBF9ZVo1llQZuhkhxAOpHeec8LsxqdQr7xMqzxJ+Pz4rEQvfkqoFHB3Sq0u+ZXypNDbwIDAQAB",
	"jal": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDYPsHbba2p0bRdakkF5hq3thtLlXOthSlcRIb11nigqL97nZ+/ZBaCDkvwT+jRlnA+VXIH3u0Cu+QCVXC9dxOhw3i6JUdOeG+GhtizdqqeId7pnh1/KP4EuOVXFQJy/hKdW/t21qMWsG/7NoqR1FNoFdHyu2yRIgvjR3v4Yh/blnt1mL783PtnmoWtfu4txi7qEOuMQS91u6SJEcRpYzBkabi0eMz2IxgKIDzjsQ+2BeN7pulMPoEaedZKWoMQo13vM8zeqgbUXpavf8D6YN7RtzEYx4PeP2xlkcxFUNMqx7UIiWlygAd8MX5fhmABYv0xKn/PuxMEJOk+7ndSQJ1Sx6EqbIUxtvI+S8eM67zlPP/byr8zNzYCkqgB+RF3DXOVrOpguWcFjV67x7dRoEpj2U60kvhrZID7Mya10CxkLAgl+NpvpaxaRkYN2wthycmioXGCfN7+EwEZBjMwZc1t5i1pMigkFANvbQK5vJE0innjJZIUpr2H8ZV8rkBhcV8=",
	"ANSB": "AAAAB3NzaC1yc2EAAAADAQABAAABgQC3b7S3QFbSpDb/PUA5BXQ8L6WZKFanf/lZFL2+8F5k6TM3R1CUM7/UiBkc8BqHa9nqbMyIkUonfM7q5aZRDXl8b7qXHDYxZppYw5VJotYtkQxG3lOfOwadPB2yhVX/IXD2Io7mQHvdpG6ntwfD0UEc9dl4oCHOVVvuGMzVGV6GmKkZfXuE2ucAeO7Yvo+Of+liw/XsqvSMlcHYmGLTXxTqVskBx53oWIJaURRgdGLIoSwWj8M/KmhwskBhQ1EN08PAssRpwMUyJyPAaj3f+ZRL5ISk/lJ5rkxYLYtNoyzxy7JKAbHYkx67b65Z4r/7+WG9Q+aS02pFgOYJavun32J3MsZhoawlqe1zfjq/fmOMOFv6+l2z0ktxkd9kBMZtAke8HkYmfX1oBG9d04w9/njQNtrxEc+7S+z9igeYb1TbTOJqgDCwbI9l1T7Jp03i0k4SPVzuLt4RtV9wZ2lnvIf1ZK/v0oL8u4hRB/TVyBHnbckV0TAYAskAiJ0BJz/v36c=",
	"dpm": "AAAAB3NzaC1yc2EAAAADAQABAAABgQCwp6J5uoGXeNEdvhPQsXlNL5W3HDGGp5OjS0k+RnbkC4bWmfhCbX2pw39+hNoaNychiwdSpRt/Y7nQ9/aIMKIb12q1EckucOdVN992uvo/F+OBMR3JBiqKa/qg9aFZ8oAUoGZtabApjo4e7gyvpTNQDCCYfY05SWJ9rwxmjlFhO5WiM+8xuwJLmbm1csBi3EGqMcPdpM+R8F4oHvtRuxJB+N0Dc+PXpL7BJPd2ON/W3Fz/iHwp4o9UNujMTf39JGhtLP45L93+fNJZb085yGwZp1IlPLjUB4HQ5Ch89sZp2VZlN6cAvsDW1bNjWsX5p/+Iz3otZXGsIAGH9N8Rp2UpYfcl1uax8lw7xnXz5WHQTI/Drtf30BXSpKmrfcg6e4CsGC3urXHDczsCtgilOI97Al8q8TM7tl+DvYMToYj8XabF0lQwD54sdJwmnAPHpUnZQCgfVasIr3aSN9oEKlqcspzT57W9A+uCm/n1d5OfcLgzvNBOvXCPdbWV+gj400M=",
	"egf": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDhtZd49XQT0yCiPA6rQ5gJ+rKDdDKkRO3H7QW+EwNChM2Evdob9AqbCt47E4PHhCs/SE/X8qq6chkT58uXM2cv4txPzceHLKRB//kvLNhpLL2y+3Tk7AY81krX3PY6xwKnska+sqhvnGujmxWsq2vdQXbxQQGrfg0zK07910+nQ52n+xmJg3eHR2n2G5y14alarbaIYYmAywjFlvU0HMA6eNxWKZ8xLvEGHa556Q/tTwN2uZeijiBBCyZp8v1ULcEU5ENFs6j5IaMHh8YAT7ftDJIdXidnpQN8DnYRTiNBIIvp1eSdZYpTSb+QQAa7N1CkPe8aXzfCEpmJbmk9Htn5rcgSNcofDIrpLcrzF8immj2vzDRPdfSBsstvzQyxBHJKmcVoTSQ2fyVDVb+yrW1NoYe9YdxuRCjrVFzWuvI4ky4oosYo2ns9Qc7Sl5+O/IrYEy1QuiUhFTlPxLMejimm+ZT7HmIgIAZrIXogWq3yf71L/fNXj5ubvrZDvNbsBc8a=",
	"RSD": "AAAAB3NzaC1yc2EAAAADAQABAAABAQC0FknfZI1mJhsD/ijmVrnuhpB/DlIrKGr1bZ1ibe/XAQUaCZeJNQGJaRWt6zRGwKHBIAykBx5o5JoNSidswGeqp7qFeG4YIvwSR0Jqxz3Miq6kp73JCp+o03i0JcHNc2zt/FbJsvyzm4w9Roxk75MBR8T3v/UfxCy0SqrlOgssxLAkdnkzycbziNPtyqc7DNnPU3cmodf+N5bgOA6/+cxgIesPsDJDPolfsTa53rbmdioiqlxVazvm3Ti1hsJJoCfsNiZqk2dq7pt0oVQDOhvKw4SnCbEW8PB41wyZcdD0RODISSxlTtBoBPdrHVZ5v0VT6ePM9CrOb/P/IM+YpHBJ",
	"lol": "AAAAB3NzaC1yc2EAAAADAQABAAABgQC3oBYYL47vtNFh5O7xthpktHaJ/pbe691exYkaZlXkDKuyhPpTpa3j5g8j7QSK4n+5YL4gf0QBHJRptNcUhn+gMCWWzsLPByWcdntkxHt+ZYFT4xZM9Bttj9/fy40x9CTX3dixMnOJeaw15YT6HrfBe7I6Yef+7hosz9JQR92Oq0S8EMYpDuhuITSeSyYEWZOGmfUDt5/BH/Z1fiAglFXnOOIyt+yU8G6bHwVyv+WHMPTkx89ebty3hnAH92rpL90+QYMICTH6oiqpvtErlI99bTzARm+yXBgXMCzyaVdXqPGg2AQZ0EBUi1VpW6q9P+pNE+gB4ulEC/3yopgEKjfj9jm8lu87R4PTTr8Yua+MtNdrXyia2C7vHDcfFK4fCypfz8ZcGp4I8wsZ5aCqLEfkbaqR6TqRRDswSER8BY5WFcyCUF/tCJ/jE9bVtgo0l/GSfFNhklyPjowCByi4dTO0JO/TL8lb1cJAoBBd1qsjd4VSBjhWGVqTDcHSXc7N+d8=",
	"poke": "AAAAB3NzaC1yc2EAAAADAQABAAABgQCzG1wqpoVFRHXru6ZgAtdqV+YDniXBDk4LvFEd/IP/dMNiFfSaXBvnmvCWmUsPOWFoanq4Fiz7jZD5R7zUnGxHsW7I27xN2746v+G+EnHAEwue9ykEP5sbN63vtYYsG0+11wmGQcLE/8FVRKc1iWHHLv7AHAyYklYCmYggDzUhi5PdJcSajm6FnbNMGIIM5qkza1emNseTN/lg2PhjbMovP3wfwZj/stA8uUS15V1UeRfE4dz5Wb32z180hK6c3tvKiGkjOXnZk+I4cxDkaWtxqG+Bi3yIkhpAKInxKYynM5KHR5yfTO8CPgj5MmMjAqIYZX9boCspkIfzDjleUkYrTiUopcumPp6JgeSYSRAkCtpbJKKaF8pZxNbro6rkpvH087SrWhbvbSxTDCBgnVAh8eXIp8jqiD/q2rmMEA+GZ73SgopNOya8MDkt07h8ipK25QMsRjls7u3fd8PB+b6Xp0R49EJygWWf3lYtkMsV35Vyq+TejZJGn/dQAwkKCiU=",
    "hnf": "AAAAB3NzaC1yc2EAAAADAQABAAABgQC3g8Kx94hXjblklCYPyAt8HCgrM6aN2bYfYn8xM0CauKMFZA3d9cgt/FS9kzkjW5lvGp/w+x3LEmB2n+ZV4X/PPid+cKKqXD9kcymD6cI6Ze5mRXJQfLctiqxvtV4JPbWaDbeaJG0ru/tIUGrBaq8SxAsU6ba2Rpa/LOxPQWZRR/jFkXtgcGi5Y6g506ibnyBgXzF5YZQOrxo8gIqkD1pp7Y948Hp1fjV4g3FeDgOGdvB6lpdCY2uAxJ0PBjKANiE2cXOmx6RDzLR0a1Ijj6xsMikY5e9lPmIFySvGzVZ86cAW45Dt6pL/XMVdAdcIruWHEx9jf5cUSOdyQd3V1p99SLMxjEbjj/SO7bi/26ng3Qdaa/es7EiK8d6DGizAoJnf1lNc3su2D8xZ4L64W286a+7A9Di/+Qi4Ow8CxOi0tLfbrOLMfdclC1Yv63K9y2slzaro0ZH15btuAeZUbSNZsQQjcSKT34axfdHBRiOsN5+VLswxZxaVMcRbYH6eLGE=",
    "MV37": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDUpIAQQ5HuqXNvvTUps8Dxgho20cOlDVQbRZQRzzm07PhobNI49e/7dgJd/NnkF30YJzwSv4mgEwQ/1mAnYMJX6Ow/R6nCH9OXJoUSw/xkccuuSRtU7+1Zr9IrquuTthqMCci/sAEb4s/ARl/WOWL32cwmjXaXP/aPpegAP/fZucoYHJIQds51OpGeHmCKewdfcnkoxTTN6EOk8ejd1Fgk1ESWXLQtuNfrSEnluD3WUFvkUAEewRSYGrMk6sq/Ql7u0y+UMb7DjZgZitGplAFTpZ3e/TONqiyZZTX6PD5qbfxVfcr0ev5FEXiRuvQ539MPBXD3i5M1JeD7x8MQMoa1KSn9r8Fdi99h83nG5dSlR9ptEW3l62ZWD7+y5D8KHmSuYIVgLRP8wR0CDgJfas+vznAiu8JkrOTts+5z5y0ldnxYTXPqjCLOnXYyxw+CvHq+N+LhrFnQGJtB5F46sS4zBnNZUjYAs8ZE0LEl2WRef/9He+DjjiC5DLY1C/3IOHs=",
    "alsb": "AAAAB3NzaC1yc2EAAAADAQABAAABgQCsIsAnPuL2k2fRp0EExnz3O66f8BGVb5g2jYET09XfS/wVmxdApDHr1BY6HqU+9rX4/vR/yRm4wygUc2FlGW5RpcRK/NXaT/ZWDwJOWiKiykbOXVz1Ew6OxYp2iu7DsCJe7sdG5RDET7SWxlV291+4u3eh0BJmJIVzDiszSpiLsI6jg2LLQ2A+FylMiXADigUpTYj7psyGdn94G+BUA6F6qmYSF3rYNtKIHDnYEQqxo4LTpHFL//7rfMNpvzc4IDNAC6O2vOBABJY2/EoOJ9W/mBveCMARcXMgo6S1j4aZjyq0UqvyOatyKiqgFm36qQ+Kv9DnYuEAvxc+2fJXtmES5gzeQWgekbSkR/8f2I51arRQK4fb4aqwRMNmLKlnspWhqKjCWHbb3Af60qgw+gThvrvXAxBUjjy39vVvIgy+wuefNflj6P1I7LQyLIRd3uYYhv/PZBfjdjhQXG3H8qrs6LDSaCGzhrIZw+2Bn5SewPjV0O7Y+EV2x1MTbR4BaoU=",
    "adri": "AAAAB3NzaC1yc2EAAAADAQABAAABgQCtVzu2/HFhGhT+6QOyKF0gSrGvk/qQTl+UnCcj18EUpZQi/J72z5qkeH9i8lFsvHr9nqLny9vEmiU5VCSyjpSL8g4x429aQ6oXH7R9rNFS2RZTtnZo1zo28FCOks2cKzJxgWUwIcW0mGdlj3OvD79bhlzv5TV1BIcEQp3hLq6fq68cp4AknqdqbczvN6ZETPqY5KqgKj3fJFHfF+zHwbK4d0DnwvXuSnD6j7Km8h7RetAYm2UG8u5vm/Gclt7GDHWeY/JdAQb4lQxzfDWJXxkufMGo0tXFpscmZKZNG1tHEy6s76qA/yRjuOugxRX5uBJEEapPPj+E4/ov5uXgKCniiaT9/mPKWrxrpcx/b5GYx3xtbSVBcy1/+r9dhzrlXMO6HeXOUAf+Ft1jStHn/QWQdCekIvQBMhMwUIHGPuerQwa1t0MV6eJ3DcArsBa1/+/IA4yWzDfYy3eZsF4V15UarllN1ydFiudeqBcVvCWnYKQ6kYfKDay8zbJNLV1TOZU=",
    "kd01": "AAAAB3NzaC1yc2EAAAADAQABAAABgQCwhBoKx0aV5EwOE6+6idVSRZlUD4VhPwZ5x0xLrKd8mNNy4Xzu2ch/6BCkx02Ca86k/T4btu5PgOZlqUpTbKwqG8iDbJIMtZSw9GLENdbaU45jRHDKykyrSZVZETELQtNMzhWWMgOIk4RJRXNhT0Xsdy8Vwz+0+u8F/Lkn53ohbeRpWr00dabdgt4cEGagupDQ7IIwActAgh98XCtJigohRL2thwOV00yDjQILipuBngYqe1sqHJwVwDf20pDIfmWuTiVmXyHZ4Cywuv6mTDdAKFJlZVAuKkDEvloz/28bb3I1jN7rwJ5xNoN5lczhDA6q8CxO3JeekmkVuoNyPO7bTA8G8UiIwW4+8xKWgwJ5ZbkqfgSmKMWQMdkTtY9jSyQWLiI8Rq/C7sJWeYaoVWqvQ9YGaA82nGfKIVATG93hQm7BcW3bFCt8jC8fD+9azYyRrUL9EHFAAZHd/1jSxuizNp2PU2SYsE9DaffOx0PKWGA600GrSHIz8uswf/mGPbM=",
    "MAUB": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDX0KBb4fhY2w4kyPyOpoBthmFsMVAfG6szp/RGSwIRvQgDEtQ6ZkjPTdJPvFoXvlj0iaTleiKzHVRmvXnVQY2K7XLNUZ52pfjpT504o1VGcIMGFtREu43er1za0MN5iaRHP4ixMhs1XbIByJRCH9tTE0p1d7Bbl4iEW5Klg4klBe7PkPevOg9FE99FsF7Ni0FwYAJZh+7l+015IuzuX39WfrYuTQULETmVgqrZqC2XsZAzIlhSzFv2jTm/asiRhnrwO1BMG42mHIufrhKJsLZut4mmQle5tDURsoXRjUF74Hk0eIfenmzwnJKwiekJP4PlciWaMYDLLqeDMsnvnNyjFT6t+zQfV8Fr8HCeuWIkm169zeqNoSO2Q4k3/4EWpxH/2FMsMdsXs8c6m/4opkT81oEJXHWCyseYLxfCTNDZf3JLNA2tGqrtJki7c0OsZ47sjLuR+XOZ2vmQf7I4DGm40TxlNiQss+6fXfXGSAypcJsIUSmQRTXvICM3zrq7S38=",
    "eau": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDOoViPC8KY6fEqOy0hxPdlbhYdI2d8zWvFUNg/IkV8K6IUWuJlQD+cmJpekH45/c90ZkApCk4qhymwKKFRbu4KxCmrICNGF83vNTjQF1yrBUvsduh93A1UdKidAq/NiQHv525OANzYzrDdDpKRVP8doGCff996wZthfVrGoPW9fQlKj2edAbqHWuQvlHl17uq+Y+vAjuZiWppObUmM0gq3axK9QCa7wlMhx1N8fpZJLBqSKwLC7yc+wlcpv0nhZ6oSK/rMQ6s0kaHwId0zM++WB58DzGpmmH+YV4gxv3VYROV7h+PG5aPQSfjYv3QS/jvJvpn9zjd6TIh6+zU7R2Jcg9jwW+e06lpLChep2+O1SrKBMYaiU9xjw9h81WDbBDFd4lgM+qjTck3YkGPVSFyJDAIuzFKFVcVY3UJfzB88m6Gpb9d9XavRIyCDCbZFF4F5K+Zde16tdAreH/UPtwyXs/BMvzYh5Oyv+wPGgD6HOQM61ecOiQcC3hBkBfbZy/E=",
    "JLGS": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDhVNqzQtcCowF9HU2EXmBOVrlbqruGI4lG/92Rr4gvGGpYVuVmrtCDKPUd1RGWXVDp8YUrQ2DvnG9brOidx77oHz7a8P8LeuAFn4wPFe5A66FzNnYoOrrlhictRSQjS44ufIblwduCGmBjJVx5gh0HuAw7k3xaEjgZcXTFeoOrQ7E9RSyiKrj2HJr6WDER1I+XtNtfgZP4wVJ1ojMFyTvtBbgmqm6p192kjZ/JxWRiw9dSq7ENIwtHtNvYURtaqk7jfdkuh60EKC2n3PB6ybljpgsTxCq+WTKO4FLiRMjA/d+Ls4gvGLEC6p6PtLRd96wIJ+uR80gjhmVsHgfypwdYsdpqi3jFQMoSJXtT5lZgA9hgLa5TIZAxWr90pM7YIjkkGm0GZjKkWfOqCynyh4mvm56DmjMsiNF4KFCPE1giJvaoJDMQXC/NdP6mBGW6aGVOM8wxRk3qgQwrwy6bH/lHW8HEFasWg2IvNnLvjZofmzHxW5nCatRDspZ2vRKfXUc=",
    "ivan": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDR14hvDZS7q1cZ7PTXy7jEVfLWCuUspJxc+Ei9YZKv+XQ+QlTJoyKlyxUJQ+egge+f7S7g2Z/mszpwte43auxkaePo47TfbYI5jvPebFX4jQk+mJ3/YKvbx66wfC+pT5dgeulhTA05TeUBxXMgZffDqQWPWjd6q3gQ275aic4Abk+oqKVgJZwtiZH8L9Cpz4TjYJFSSl2IMLAGE4v01MzTGEB2+Xh5wR45o/GjgFio0WwP8lN6YC1dPtIDPpNULHtfdC4n/st6RtmM9avThJTgSJfX6G01D79VEXYFnfPsABVV+ER3JoJ5AfSkK46HwSDoEk7bWTo4d2ZnuRx19/bg1BrqEPvpaGAxRnJIec5EOHSB0TBqpiY3q4nkrrWBj3ITe5L+spkyrWdDuLnTR+6F7AM6XQNZIGaAS3ZaqXCZvWoieqc8OAYVuDp0/0/YMAEZEdja7zoNkFPWX0AKu3Mz8BwyIY1dPtu/JwUysdRN5km/o7nV0MVby9tZz70joXM=",
    "cab": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDEL/O0w1oWCBBkMyM+AjsGdlpobfjf+wZ4uGp2UEiIu183gsYGUJRK0E5V6avHXcJbh8mLJ9nsDAXRMexy3B12RUU34SjlL37ByGJwKKe/zlcw7MaXAqsfYmkkwyJGS/8v0uOvF/oihz6GyblbWzFIsqekkKLOVcTOT+fFU7MiHpXW/Azna9zaGdWyUNS8GWDvI3rENIUP30rKCwvlSQGh1yDdEa4c8SrDgfEUuqdhjqzbw0D3NQkXOj4lxh5e0c/X9OtRuOsnjBZhAVBDE5syNg8gvtOsYYR195NgB0a3LaHa9SiqeyCdJOrM++4dxwxT8wgvvdxqUaPU1fsQ+GaTSHuYX3jy/jL/H+FuktVPNXtWHL72vr92x2HnyFB32LyGxgqx2GY2hGjImfqawn8NC6xKKAeSAo0xNJbmRcDwlcMpaUdVsNntJSynYoq1M86H083UsITh7j44IlbXmRnlvlFrUAYC3XQWii3ZZOGaUXiStnkESgcLRyDiykGQVOE=",
    "idi": "AAAAB3NzaC1yc2EAAAADAQABAAABgQC6QBeWNGPvaGb/t4MHL0WQ+NhJsghL9pwV+aJDoEowKeEl3bcK5cXQijWweG2d9N/wFgrnWtD7Flk4ZInM82HhemNexXLfv9s+2yDvfeFfmJfaXwo28fMuH9ExfqUMptLIxzlBphsR68NHDa5abFlq+yEI7VXwfUGPGg3+ntjYS+Z9vRQy/N6qtcHlhAHwHjPfT16D9wlMsfvw49Ca9ttWRnsRSxWbK+pNqGO3QhJ+IOAWTIxqXCU7S6BW6cHlLyCjK/GyV6wEq4sbAoljWH1dcn4ZyP7/d8mdOHorclkW3O4SA5gheeS9dPlNiMVRGuCbJ6vUd9DV1FV23KgrgV3wd7eBChL/5bxr1X4hliOyGwSRHusXcXHXN7S6P+Z/sDb3kIIKzn2oDl92XXesNFoXdZTFcv8Pjq8trzvQulYdaksmVY0Quelk7LaI6uEqr599fcbQrBnHrylcQXJvR3Zzxvgj/ZK2M+y6r7L7hMc9ds8Ih9Qe65Bpoeg/QZnxld108=",
    "DALN": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDjT/g48aaFE3518ncYRvScAKhpOI2MDX/8OxACoYzKRvzAiavDgaLE4rM2tYVc2WHuy05QGiFe1IHiX7ypcqwRZQDsxZ7y2o2wRsykdgLEQdJttaW+mpx5OLHDmzH5k6Qpvtbj9B0bxwbIsgO58gX/s3n2D/Ub1A0aPhXg4WkpD7mq6LK19ccM6bz0S79M2xihl2vKf0XG0ZzOTDJm18h8yyquPITWaQvsxfk/YbCnbGzjFwgLLn3co11lxDwzS+RleW5qmVaSQPHSwIO+mZZgboWR9bz2P3qpP2NgIgiUuTwU6rMCHrpDoAzSZaU19ahmKiazyKzIO9agFuaeo8wZVD5TMPislirGdq8maiKumXjmd0/ZcrxUiHwzwgFdfMSNkk3x5uU/xffHUTUf8oL9ciIsJf1XfKptHQs6299TNtS+4L9e2q5zmsnVNq5XqrZQwX49rViyQO+PA0QnAlnwhKcF2IILgx8XFrjvIjyTZTbL6gndnE+apFSlfl7RBqM=",
    "SNR8": "AAAAB3NzaC1yc2EAAAADAQABAAABgQCgklgDdqIPFX3+FEcUAz4khtwrfRHFOWPL48XZkxcMJkWhV0y0v4pZ2eBrwJIxQw058pk+JnnDu8CJGnaXPReHPA50OQzbpkbt/ncIOJ35qQC8ek69cQGpccnK2yjI1K7eXS/dXD1qAH9O/ez2vR23jWbZhHBSsrYgQzH1zOLql5nMQtc4YaPR6g3WUcm+QvR8zJq+W3EIYR8qQmq9PbC2zPNDpXSe5vnbqQV+yacC6qRZdcPVnBXJXhiVCn4KFRd4PwTIyP5IAvzi4rmYko6g8mGfLdXTtuVoVz0tfW/W9ajSft/q+jXuQB8rcehzbqO/+fBmtwAS904BVjRnrmRWQdriHWTXOIRnTj8tRS6FbH7v/JsbFONkn+LxZAfd12B/SQVMOBGyZ63aLkqE2gmjDBq64OkvW1zeMxEurtxcEpgDkFj7tZqKEjlzrogHTtLM+BPt0d3bjtzJJ/L7gFnVxrM5tK4v+CM7O6AVdoxbdjjE2QZEcj0756MzuwpsjmM=",
    "dhbo": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDupUvldN0vwz5qSJXbKi2oZbfUr5ViMThyb91lq0hqY7sKdvfXP3ArZGgbT1f6sjB3ptCdXfmrFhpPdI4KxQNiDTQ+ZkmV3y64SwpgEIwcrWSoyfI6mrQtFrdlripAL02IJk237WYf94CfWcxxg3W3et8mxCHF7RNjGFIjZu8J5x151QfhwLeFv9b5AlfhmGRe7GB4VP0P2rpOGTXOOB3sgV/u6wBUSimynR8aSoTsN1rwTQP2hmYtkFuIY4Xo3bhSB52LK76hcn7WO53ZkQKXiyJGgsMel+O+CNezFN0WFd5nkSFgPo9lwzofD/2/hqxQkw2yqJSyzF07pD924Nd7Qc/8Nk3N6DEKeEU33/PbJ2aVsSfV5bhWaT5TrOmMvCXIYctEyYcnN+VD2Kc3mJZuCtFBDjSFnuFbFDeZndwJV1cOhOK+yDCUkOYABpD9fC85bkzs23ch/usPAbP7uQw5De4WuvRgw4p2hFIts0jXYhnFpdBW8eRbSo2LKcGJWfs=",
    "si1":  "AAAAB3NzaC1yc2EAAAADAQABAAABgQC1Z8jJ2ILY1Wxfc3XvWC0fBeJey/9HwluKfbs84TCwkKY7+hVI4AyHFJMvXtq/jAs3lAAZgfBGYiH7xEXy/qkwoiU7PJve+aSXIu3jKj5QOu7QAxY/JxCLcwfjvy3q/XyoFJqVX6EfpSMDK4lwdZREdgW0SrOXtRNdOy+Ju3ucy8dz/2Fm6HHYIMyp+oP1ahi/kINOnThzlF8wthpVmrrI/gFx7sti4Zm145rVKtJHz5PoJFp4LPSlxYTy7v9Q2EmXuAC2Vv8rjdqV/1y9q9eC8aPI7GzXzap4Gy0Jb1FvNIRJw+mjXmzw/frUUQX25PDt2v0DUPNmlIkVXJZHWa6bUziMt2513oCPflj2lSQT9Vas57lKm2ktzII4GfImWlhXJNLCob2LG84BzV7ji6Wr8PeW0gbNVNBta44Vr34LBt0VqaUwKEnYIIK1quVUg68m8q9peNrbpUj+A/dGNwHuS4JPlUcyndbiLXYqMY5fOB9uOrL+fgKV/trvt8ipKik=",
    "si2":  "AAAAB3NzaC1yc2EAAAADAQABAAABgQDDOMtLBATeLjXxG3gp1ZTnMKhiRNWSaLLxF0r96pWRiapyrDCHo994X0Fzyx5OjbqTb/fY9ChR3vW3wH85L29KU7pb677LpaBhoake1dzNSb5ps+H+KnRh+SwjhYBnL1YM1r1ti4PZnyvfCd3vYvhyAGFsimyABWrlav8jngFJkIm6c0GHoyU9xHET9DT6sXzW8RlCKaurNFo28kqrIShthkhR0i35XOoC4NfLX8E72ZB2KtKwZObm7f6tspps8+Ijq6fK7ZRk2BWtjHPpp0m/T6ubuDTi1Uw9HghWJDHRUSLIe+YJ20llfuTTXjoDzRCAynA5TVRRskZh1uhYoUAifw7Ue9TX9fsB+EQanofalNHGyvix71DS9KwZNBFIItpAQyTVCiz5qX4NqyutaNKAUExLJWWmbUnX1IXxGz2Ah3UZgq1HcNKdrwt0pNe2thy2/EK25rDkCAAwzLGG+dnLZbZmFZEcj2KYmRhr7sld0TUkfJs71Glo/2o4NMWuHqc=",
    "si3":  "AAAAB3NzaC1yc2EAAAADAQABAAABgQDQetDzZMjqWHnFnUjGpJ8zVkBbyXKhZLwJzVAVFkeA9gI5gsOtP0de/EuTdNBMMZKi6hX/q4lkNHNhB8E1GltQFduV5kkxkvS6DS+scmwe/TlVT5o6PPchNFsuOFYw+/ZESOEaTbiHqr2mLTy/LV+c2ZbVwbuexKaoONeGBftzJoJZJ+XwU1peHehpubrbjBrqbe7jpSeMzPP91Li6kSRjEiecEltPOfpJs4xvUbiIkkEMANF2uIqfVF+RLD2lx8gCCKAAQ941mESh1/8n9ZcXKJPFUiuL1rlbO3oaluyhD+h8cfKY4XXmtAKlJrN8urAhoIrKnAztM/Ou+R/R2aXNJVWy3t/goUtP5btY0BIOlH5cKH2jy+7zBu3K4wrOXub7hPMdPEEwQa/ZzytoQYnO6xQGgQhZR1+xfaB6DbSOE9J8f1c4UtrauU2u2QV57Y6Xtwxf1XuOlu2TPYPN2gly3+5beaJDT7axafuXMgz9EkutlQMkU0eJTuLnZIDb8js="
}

privkeydictionary={
    "alpe": "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCSHXWkesxTNPQP0TVZUvAwnZS70o//BAx6UHY/STDgIxHT7qQ0MpRJvEXbcqyKZ3R/1OqBYKQBnfvlFHKdHXLUZJr4Yci2cz2fmtayEFtRuo3s7/g+MesZ173uZJGCyvK6sq44iIrLncEX+hOprg1o0oXHeeguVKmn74uVr1C1/0e/o2Xk8N5Kv/tX5Rq17bq/JkCWI/Om9yrsUwTPhHCcFxi+ruqgZopxBMxlocQ0kppf+Osx9AQEwPLZAMhTkRgTg84hsewWZqz+JPSQO8EX1lWjWWVBm6GSHEA6kd55zwuzGp1CvvEyrPEn4/PisRC9+SqgUcHdKrS75lfKk0NvAgMBAAECggEAFQugN7YmOu/cHXEdNYXwKZhw5VKxQeJz56QyO/BPVWFHvpZXWVtVp38yMqcEOhUnnwfsVQE17jOype65iW7F7Nimx5LSBZF4tUXomZIojQ+JRLDVuSOYgMrlxPIAUW3o40I8PNFR6H0K5Gi1L1HuBYSZFz+0VQQFwbYLjV5IikYIcqoZx7vP2Rwint3U0tMmclrgfpca7toih/xEmoDsEmu3NIYniIVD3xT/Xv9SaNDJjYgubVhnS1sl5f6N1SIT8nw9TyRUJTTbum4NyCzQoxadkTn1IQxCUM6/muZHfWYpiiNLHmuMSyS9HeyY9bPp/HwekLQ3GJkvkpAQOYNXrQKBgQDHWUr/YpF2YZ/CREksGiGAsVqlUfVB/Rgzc5jnBnxFrGoeyf+nQ3u8+k1Boe+KVbPhZTDPQ391LjSbST1PrXUF9EhSjG36EnXT5jJ3oPvtaQMn0ktnblF+zJ7Q24dzdSQyV4gEQxYq3bHE3bcVTe8+ojFwI9ls787OBkqG+tyztQKBgQC7o2QsCvlZz3GQOhgDzHcoQ1JUYBYU9wMe9IWmb53GCkzAPN5XkAtErJg0wNRtUEtegw3BLGN7ab53c3Ab3bHW2W8LKPUnXBFCHy49yvXEXNj99DcVFKbq1Z/rrBCauy5v9f+4zgLt/WjW7MSVE9hhJ/fBu2h8SJHaGvrWLdhZEwKBgC+Jb4Tu8FkWdo5Q0lId+RdDM6ZwoNeXjwnV6wRMW54Ru0yURs6QHRW3amzYPNL0FO0OwFDse5xp5EmTcXdqmZlN42Er853KgSaCok48qVa3z/TTBQApIm3mRYjwkKBLstH+ZYT+qm6WZynW5S3DY+W/r6JaKiL8HIisn2EIuVBxAoGAfqMkrVDuvz1xULzUjmPFm+frvcRnwth/Q7oWJaE5I3q6GBg8m249HKk7xIbMF8bUR0I92z0hGx7gDHBdnoD+UJnJBwgqhNjvUOgIZm3/dvqO/L6BGnoouV9aIk2rmzJvgeLOJyTq90JLKpr7hf2x0MiPvzHDr/Wucjw5RKoGVP8CgYEAi8qcrcj6wQ2h+xBIlGgDiUanFAfpDynkoyCsMAyo/2jgnsqknakQ9AyepwklGSXR+kRocyyuAqC7H4iu/GJnGBL7r8q76CF8AGftkAEIG9W48fzGfxLRVIbsE0vdCuo3znX+7kY0pRVYSueJMyBejqsiyHW/4Cw2bTcCh/V5dBE=",
    "si1":  "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",
    "si2":  "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",
    "si3":  "b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcnNhAAAAAwEAAQAAAYEA0HrQ82TI6lh5xZ1IxqSfM1ZAW8lyoWS8Cc1QFRZHgPYCOYLDrT9HXvxLk3TQTDGSouoV/6uJZDRzYQfBNRpbUBXbleZJMZL0ug0vrHJsHv05VU+aOjz3ITRbLjhWMPv2REjhGk24h6q9pi08vy1fnNmW1cG7nsSmqDjXhgX7cyaCWSfl8FNaXh3oabm624wa6m3u46UnjMzz/dS4upEkYxInnBJbTzn6SbOMb1G4iJJBDADRdriKn1RfkSw9pcfIAgigAEPeNZhEodf/J/WXFyiTxVIri9a5Wzt6GpbsoQ/ofHHymOF15rQCpSazfLqwIaCKypwM7TPzrvkf0dmlzSVVst7f4KFLT+W7WNASDpR+XCh9o8vu8wbtyuMKzl7m+4TzHTxBMEGv2c8raEGJzusUBoEIWUdfsX2geg20jhPSfH9XOFLa2rlNrtkFee2Ol7cMX9V7jpbtkz2DzdoJct/uW3miQ0+2sWn7lzIM/RJLrZUDJFNHiU7i52SA2/I7AAAFkA8LkugPC5LoAAAAB3NzaC1yc2EAAAGBANB60PNkyOpYecWdSMaknzNWQFvJcqFkvAnNUBUWR4D2AjmCw60/R178S5N00EwxkqLqFf+riWQ0c2EHwTUaW1AV25XmSTGS9LoNL6xybB79OVVPmjo89yE0Wy44VjD79kRI4RpNuIeqvaYtPL8tX5zZltXBu57Epqg414YF+3Mmglkn5fBTWl4d6Gm5utuMGupt7uOlJ4zM8/3UuLqRJGMSJ5wSW085+kmzjG9RuIiSQQwA0Xa4ip9UX5EsPaXHyAIIoABD3jWYRKHX/yf1lxcok8VSK4vWuVs7ehqW7KEP6Hxx8pjhdea0AqUms3y6sCGgisqcDO0z8675H9HZpc0lVbLe3+ChS0/lu1jQEg6UflwofaPL7vMG7crjCs5e5vuE8x08QTBBr9nPK2hBic7rFAaBCFlHX7F9oHoNtI4T0nx/VzhS2tq5Ta7ZBXntjpe3DF/Ve46W7ZM9g83aCXLf7lt5okNPtrFp+5cyDP0SS62VAyRTR4lO4udkgNvyOwAAAAMBAAEAAAGAExltUx8EmROJ9GS4ahpiy103gDEwY0DLSUqZ75Se8F2ZTpOAQbruWvFaKyQkgRZ5jJtNcKLSb2+uslD3jlnfy7J074KtafFAolra5z2EUkJ4oiwswPEc4tndEJrwqoQqx461sKc2JJer0DGMwybw/3mfq+2Xtq/lZLvwYsLhimcYwfo5wo6gVMcAp87wI3TuclOn8wsKWIfeQn7efZkWcE0Ve+Liopt5Jo9gakJeWYSsmODqT6oQaRBdwPsAmtN2gOlQu4FrW4JP14mdgOKGO2JXvycdCNssmSC2EMBFXehmsdnOFPn4HZKWgoL9Efl9/yu2iE6jUhjqO/cMW3h7pzqSSXia7FVlEY5Zgjy7R482Y+zxgIoa1H0vtEbzkU1+YutYGU4gVX2H2V8SV7ZZmdtLUBru0cW0QlCX+NAEw19p6/fzrQyfZF/b9aRnOWTvXMx9e7IMLWhYYvgWBkBQquiHl0LlB01ChW9AGEjX2Rb1TJsqomqc+JWNibJX7TJBAAAAwDTEFsPDcXql14bXeShMyEHTo//PztZ16Hrlwj+OOXMpjNN7ZPAxDAXcyCMeRMA70z7F+11w4RuQ/duC67jedKqj+MsBk8GWcD/CHBVQeqqbvhOlMWtCPc8AaWPIN3smzzrw9k7wtukDOxzdm1iv7uaXNd6GMfW51NVUWYIO7V3oHIM/hfe5B3vO3zkmgv/TLpZIcCKSSjvR9dcWQndBlKHkjgHzvlF0p3DHZ0FwUeBnswTVsZL9lK1BIomgGk+pjAAAAMEA+BalGddRsVeozwnO2YPTvKgWnuVeRSaDGYSkzI/RC6U8JFPE/UXANieZZrDV1Egv/Foq0ZpiSwIixEErTbx8Ju1hSX31rl9wns3/c4YjgQXsuOyA7vVZ3e6CHT5JtLaEpEmu037rL2rf6iBRdB5w7yt6Ij3h1dWyyOGIrMNSprDoSursjbfCXiHWjZ4WdNEDo+GJ9I59MXPEu3y2NXGUv5ltXizLgXONpwQW9HUGkIS/sGwi8G7TUxqVfbg9tpuDAAAAwQDXIM/iwCsXXlAE4sf98TQtnzm3yOR4/he2/7GYzQeJO2eD7b51kp+1NWzzAxn+IEuWR1NZ1KgLPsOTguZAtaylcQZ9ChYosVYL2gielZe6pa5TyPk7a9fUHTAXyOsLoI1Nb6saknUPbVp42oZvPy6yLDGJ8awGv1xoJaG4JHPWfn08lfeAIBuvRx7j0NASv7rNzpcMTKCVOhuRor5RBGMqnIbMEy38mmtw/tBcFuaeZ8C1VkZ3jHmIeUkuU1XBeOkAAAAVcG90ZXJvQEdSQUQwMzEwVUJVTlRVAQIDBAUG"
}

def getKey(key_str: str):
    if key_str.startswith('MII'):
        if key_str.startswith('MIIEv'):
            key_str = '-----BEGIN PRIVATE KEY-----\n'+key_str+'\n-----END PRIVATE KEY-----'
            key_ascii = key_str.encode('ascii')
            key = serialization.load_pem_private_key(key_ascii, backend=default_backend(), password=None)
        else:
            key_str = '-----BEGIN PUBLIC KEY-----\n'+key_str+'\n-----END PUBLIC KEY-----'
            key_ascii = key_str.encode('ascii')
            key = serialization.load_pem_public_key(key_ascii, backend=default_backend())
    else:
        if key_str.startswith('b3Blbn'):
            key_str = '-----BEGIN OPENSSH PRIVATE KEY-----\n'+key_str+'\n-----END OPENSSH PRIVATE KEY-----'
            key_ascii = key_str.encode('ascii')
            key = serialization.load_ssh_private_key(key_ascii, backend=default_backend(),password=None)
        else:
            key_str = 'ssh-rsa '+key_str
            key_ascii = key_str.encode('ascii')
            key = serialization.load_ssh_public_key(key_ascii, backend=default_backend())

    return key

def encrypt(pubk, m: bytes) -> bytes:
    # Generate key
    key = AESGCM.generate_key(bit_length=128)
    # Encrypt key
    key_encrypt = pubk.encrypt(
            key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
        )
    )
    print(len(key_encrypt))
    # Encrypt message
    aesgcm = AESGCM(key)
    nonce = key
    ciphertext = aesgcm.encrypt(nonce, m, key)
    return key_encrypt + ciphertext


def nested_hybrid_encryption(path: list, m: str):
    s = path[0]
    r = path[-1]

    m = m.encode()
    if anonymous:
        m = parseId('') + m
    else:
        m = parseId(s) + m

    m_prime = parseId('end') + m
    print("Cifrando con " + r)
    c = encrypt(pubk=getKey(pubkeydictionary[r]), m=m_prime)
    
    hops = path[1:-1]
    hops = hops[::-1]
    print("hops:"+str(hops))
    for n, id in enumerate(hops):
        pkg = parseId(path[-(1+n)])+c
        c = encrypt(pubk=getKey(pubkeydictionary[id]), m=pkg)

    return path[1], c


def decrypt(privk, m:bytes)->bytes:
    # Decrypt key
    try:
        key_bytes = m[:256]
        c = m[256:]
        key = privk.decrypt(
            key_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except:
        key_bytes = m[:384]
        c = m[384:]
        key = privk.decrypt(
            key_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    aesgcm = AESGCM(key)
    nonce = key
    return aesgcm.decrypt(nonce, c, key)

def decode_and_relay_messages(privk, c: bytes):
    # Decrypt key
    m = decrypt(privk=privk, m=c)
    print(m)
    next_hop = str(m[:5].replace(b'\x00', b'').decode('ascii'))
    print("next_hop - "+next_hop)
    m = m[5:]
    if next_hop in ids:
        print("YEEEAAAAAHHHH!!!!")
    if next_hop == 'end':
        print('Message received!!!!')
        print('\t> From: ' + m[:5].replace(b'\x00', b'').decode('utf-8'))
        print('\t> Message: ' + m[5:].decode('utf-8'))
    else:
        print("Sending message to " + next_hop + ".")
        client = mqtt.Client()
        client.username_pw_set(username=mqtt_id, password=password)
        client.connect(mqttBroker)
        client.publish(next_hop, m)
        client.disconnect()

    return m

def parseId(id: str):
    return id.encode().rjust(5, b'\x00')


def publisher():
    client = mqtt.Client()
    client.username_pw_set(username=mqtt_id, password=password)
    client.connect(mqttBroker)

    while True:
        m = input("\nMensaje: ")
        next_hop, c = nested_hybrid_encryption(path=path, m=m)
        client.publish(next_hop, c)
        print("\nJust published " + str(c) + " to topic "+ next_hop + ".")

def on_message(client, userdata, message):
    m = decode_and_relay_messages(getKey(privkeydictionary[my_id]), message.payload)

def subscriber():
    client = mqtt.Client()
    client.username_pw_set(username=mqtt_id, password=password)
    client.connect(mqttBroker)

    client.subscribe(my_id)
    client.on_message = on_message
    client.loop_forever()

t_publisher = Thread(target=publisher)
t_subscriber = Thread(target=subscriber)
t_publisher.start()
t_subscriber.start()