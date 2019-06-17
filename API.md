# Projeto SIGA

<p style='text-align: justify;'>
Esta API fornece uma maneira simples de acessar os modelos gerados por este projeto.
Esta é uma [API REST](http://en.wikipedia.org/wiki/Representational_State_Transfer "RESTful") que utiliza Basic Authentication para fins de autenticação.
Atualmente o formato de resposta para todos os endpoints é [JSON](http://json.org/ "JSON").
A URL base da API é https://siga-dev.fortestecnologia.com.br/api
</p>

## Autenticação e Autorização

Nesta API será utilizada a autenticação e autorização baseada em usuário e senha, previamente
especificados nas configurações de aplicação do próprio Azure. Portanto, qualquer tentativa de acesso
sem as credenciais de autorização retornará o erro <code>401</code>.
Os valores de usuário (AUTH_USER) e senha (AUTH_PASS) podem ser visualizados e editados na seção *application settings*
no portal do Azure em https://portal.azure.com.

## Endpoints

A resposta do modelo será um JSON contendo todas as janelas que foram utilizadas previamente pelos usuários, através do parâmetro <code>frames</code>,
do modelo. Modelo este que pode ser encontrado na chave <code>model</code> contendo várias janelas e os índices das janelas com maior probabilidade.
A reposta conterá o nome do produto na chave <code>product</code>, além do <code>cnpj</code> e usuário, <code>user</code> caso sejam informados na requisição.


## Resposta

A resposta pode ser dividida em três partes:
- Frames:

Informa as janelas para as quais o modelo contém informação.
```json5
{
    "frames": [
        "TfrmOIProvisaoFeriasDecimoGEV",
        "TfrmDgAlertaEventosNaoMapeados",
        "TfrmOiBalancete",
        "TfrmOiGrfEvolucaoGrafica",
        "TfrmDgPRFPRDCons",
        "TfrmDgFOL",
        "TfrmOICTEstatisticaGeral",
        "TfrmFrGFIP",
        "TfrmCdLEP",
        "TfrmCdGev",
        "TfrmCdGPS",
        "TfrmDgImpErr",
        "TfrmCdUFD",
        "TfrmFrCentralConecta",
        "TfrmCdPEP",
        "TfrmDgFOLCons"
    ]
}
```
- Model:

Informa os índices para onde o usuário poderá ir, com maior probabilidade, a partir de uma janela específica. Os valores numéricos
representam o índice do array de frames explanado anteriormente. Por exemplo, a partir da janela *TfrmOiBalancete*, os 
índices mais prováveis são, da maior probabilidade para a menor, o 14, 17 e 33, o que representa no conjunto de frames as janelas
*TfrmOIProvisaoFeriasDecimoGEV*, *TfrmDgFOL* e *TfrmCdGPS*.

```json
{
    "model": {
        "TfrmCdLCP": [
            12
        ],
        "TfrmOiBalancete": [
            0,
            5,
            10
        ],
        "TfrmOIFolha": [
            12,
            24
        ],
        "TfrmPrAC": [
            21,
            16,
            0,
            8
        ],
        "TfrmCdGPS": [
            6,
            1,
            5
        ],
        "TfrmDgFOLCons": [
            32
        ]
    }
}
```
- Dados do Cliente

Especifica os dados do cliente que fez a requisição, retornando os atributos passados por parâmetro.
```json
{
    "cnpj": "cnpj",
    "product": "product",
    "user": "user"
}
```

Caso o usuário chame, por exemplo, o endpoint do produto, no qual não são passados o cnpj e o usuário a resposta deve ser a seguinte:
```json
{
    "product": "product",
    "cnpj": null,
    "user": null
}

```

#### Produto

- <code>GET</code> /product/:produto

A URL a ser requisitada ficaria, por exemplo: https://siga-dev.fortestecnologia.com.br/api/product/sigaProduct

Neste endpoint podemos encontrar os resultados do modelo aplicado apenas a um produto específico, ou seja, sem contar dados previamente cadastrados do usuário ou da empresa.


```javascript
{
    "frames": [
        "TfrmOIProvisaoFeriasDecimoGEV",
        "TfrmDgAlertaEventosNaoMapeados",
        "TfrmOiBalancete",
        "TfrmOiGrfEvolucaoGrafica",
        "TfrmDgPRFPRDCons",
        "TfrmDgFOL",
        "TfrmOICTEstatisticaGeral",
        "TfrmFrGFIP",
        "TfrmCdLEP",
        "TfrmCdGev",
        "TfrmCdGPS",
        "TfrmDgImpErr",
        "TfrmCdUFD",
        "TfrmFrCentralConecta",
        "TfrmCdPEP",
        "TfrmDgFOLCons"
    ],
    "model": {
        "TfrmCdLCP": [
            12
        ],
        "TfrmOiBalancete": [
            14,
            17,
            25,
            16,
            21,
            33
        ],
        "TfrmOIFolha": [
            12,
            24
        ],
        "TfrmPrAC": [
            21,
            16,
            22,
            0,
            23,
            6,
            13,
            8
        ],
        "TfrmCdGPS": [
            6,
            3,
            1,
            25,
            5
        ],
        "TfrmDgFOLCons": [
            32
        ]
    },
    "product": "sigaProduct",
    "cnpj": null,
    "user": null
}
```

#### CNPJ e Produto

- <code>GET</code> /cnpj/:cnpj/product/:produto

A URL a ser requisitada ficaria, por exemplo: https://siga-dev.fortestecnologia.com.br/api/cnpj/012356/product/sigaProduct

Neste endpoint podemos encontrar os resultados do modelo aplicado a uma empresa (número do cnpj) e produto específicos 
passado como parâmetro na url. Neste endpoint não são considerados os dados de usuário.


```json5
[
    {
        "frames": [
            "TfrmOIProvisaoFeriasDecimoGEV",
            "TfrmDgAlertaEventosNaoMapeados",
            "TfrmOiBalancete",
            "TfrmOiGrfEvolucaoGrafica",
            "TfrmDgPRFPRDCons",
            "TfrmDgFOL",
            "TfrmOICTEstatisticaGeral",
            "TfrmFrGFIP",
            "TfrmCdLEP",
            "TfrmCdGev",
            "TfrmCdGPS",
            "TfrmDgImpErr",
            "TfrmCdUFD",
            "TfrmFrCentralConecta",
            "TfrmCdPEP",
            "TfrmDgFOLCons"
        ],
        "model": {
            "TfrmCdLCP": [
                12
            ],
            "TfrmOiBalancete": [
                14,
                17,
                25,
                16,
                21,
                33
            ],
            "TfrmOIFolha": [
                12,
                24
            ],
            "TfrmPrAC": [
                21,
                16,
                22,
                0,
                23,
                6,
                13,
                8
            ],
            "TfrmCdGPS": [
                6,
                3,
                1,
                25,
                5
            ],
            "TfrmDgFOLCons": [
                32
            ]
        },
        "cnpj": "012356",
        "product": "sigaProduct",
        "user": null
    }
]
```

#### CNPJ, Produto e Usuário

- <code>GET</code> /user/:usuario/cnpj/:cnpj/product/:produto

A URL a ser requisitada ficaria, por exemplo: https://siga-dev.fortestecnologia.com.br/api/user/sigaUser/cnpj/012356/product/sigaProduct

Neste endpoint podemos encontrar os resultados do modelo aplicado a um usuário, cnpj e produto passado como parâmetro na url.

```json
{
    "frames": [
        "TfrmOIProvisaoFeriasDecimoGEV",
        "TfrmDgAlertaEventosNaoMapeados",
        "TfrmOiBalancete",
        "TfrmOiGrfEvolucaoGrafica",
        "TfrmDgPRFPRDCons",
        "TfrmDgFOL",
        "TfrmOICTEstatisticaGeral",
        "TfrmFrGFIP",
        "TfrmCdLEP",
        "TfrmCdGev",
        "TfrmCdGPS",
        "TfrmDgImpErr",
        "TfrmCdUFD",
        "TfrmFrCentralConecta",
        "TfrmCdPEP",
        "TfrmDgFOLCons"
    ],
    "model": {
        "TfrmCdLCP": [
            12
        ],
        "TfrmOiBalancete": [
            14,
            17,
            25,
            16,
            21,
            33
        ],
        "TfrmOIFolha": [
            12,
            24
        ],
        "TfrmPrAC": [
            21,
            16,
            22,
            0,
            23,
            6,
            13,
            8
        ],
        "TfrmCdGPS": [
            6,
            3,
            1,
            25,
            5
        ],
        "TfrmDgFOLCons": [
            32
        ]
    },
    "cnpj": "012356",
    "product": "sigaProduct",
    "user": "sigaUser"
}
```

## Erros

#### Os erros que podem ser retornados pelo servidor são os seguintes:

- <code>400</code> Requisição inválida. O pedido não pôde ser entregue devido à sintaxe incorreta.
- <code>401</code> Você não está autorizado a acessar esta página ou os dados de autenticação passados são inválidos.
- <code>403</code> Você não tem as permissões necessárias para acessar esta página.
- <code>404</code> Página não encontrada no servidor. Verifique se a URL foi digitada corretamente.
- <code>405</code> Foi feita uma solicitação de um recurso usando um método de pedido que não é compatível com 
esse recurso, por exemplo, usando GET em um formulário, que exige que os dados a serem apresentados via POST, PUT ou usar em um recurso somente de leitura.
- <code>500</code> Erro interno no servidor ao processar a solicitação.
