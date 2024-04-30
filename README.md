
```sh
bin/zot-darwin-arm64 serve examples/config-ui.json
```

```sh
oras push --artifact-type mr/model --annotation "key1=val1" --annotation "key2=val2" localhost:8080/hello:v1 models/mymodel.onnx
oras attach --artifact-type mr/manifest --annotation-file annotations.json localhost:8080/hello:v1 example-modelregistry-metadata.yaml
```

```gql
{
  Image(image: "hello:v1") {
    RepoName
    Tag
    Digest
    MediaType
    Size
    DownloadCount
    LastUpdated
    Description
    IsSigned
    Licenses
    Labels
    Title
    Source
    Documentation
    Vendor
    Authors
    IsDeletable
    Manifests {
      Referrers {
        Digest
      }
      Digest
      ConfigDigest
      LastUpdated
      Size
      IsSigned
      DownloadCount
      ArtifactType
      Layers {
        Size
        Digest
      }
    }
    Referrers {
      Annotations {
        Key
        Value
      }
      MediaType
      ArtifactType
      Size
      Digest
    }
  }
}
```

results in 

```json
{
  "data": {
    "Image": {
      "RepoName": "hello",
      "Tag": "v1",
      "Digest": "sha256:0aa63934b9dacbf3e865eb3c84cc9af52ccdf80d2c67cfb43caa1fdc477f74f9",
      "MediaType": "application/vnd.oci.image.manifest.v1+json",
      "Size": "422008",
      "DownloadCount": 0,
      "LastUpdated": "2024-04-30T13:37:14Z",
      "Description": "",
      "IsSigned": false,
      "Licenses": "",
      "Labels": "",
      "Title": "",
      "Source": "",
      "Documentation": "",
      "Vendor": "",
      "Authors": "",
      "IsDeletable": null,
      "Manifests": [
        {
          "Referrers": [
            {
              "Digest": "sha256:0d2c41aff6f92dacf7d1732997771db6f27a3eb7d304e854e40021d8493dc249"
            }
          ],
          "Digest": "sha256:0aa63934b9dacbf3e865eb3c84cc9af52ccdf80d2c67cfb43caa1fdc477f74f9",
          "ConfigDigest": "sha256:44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
          "LastUpdated": "2024-04-30T13:37:14Z",
          "Size": "422008",
          "IsSigned": false,
          "DownloadCount": 0,
          "ArtifactType": "mr/model",
          "Layers": [
            {
              "Size": "421403",
              "Digest": "sha256:2536d32a8d81c95b8261926e57e34e00b32a7ea22eef96c653ce29be1e64f7e1"
            }
          ]
        }
      ],
      "Referrers": [
        {
          "Annotations": [
            {
              "Key": "mr_str:name",
              "Value": "Investment Portfolio Optimization Model"
            },
            {
              "Key": "mr_str:owner",
              "Value": "mmortari"
            },
            {
              "Key": "mr_str:description",
              "Value": "This is a first installment of the Investment portfolio opt. model\n"
            },
            {
              "Key": "mr_str:uri",
              "Value": "https://github.com/tarilabs/demo20231212/raw/main/v1.nb20231206162408/mnist.onnx"
            },
            {
              "Key": "mr_json:customProperties",
              "Value": "{\"my-prop1\": {\"metadataType\": \"MetadataStringValue\", \"string_value\": \"ciao\"}, \"my-prop2\": {\"metadataType\": \"MetadataDoubleValue\", \"double_value\": 99.999}, \"Portfolio Optimization\": {\"metadataType\": \"MetadataStringValue\", \"string_value\": \"\"}, \"Investment Strategy\": {\"metadataType\": \"MetadataStringValue\", \"string_value\": \"\"}, \"Financial\": {\"metadataType\": \"MetadataStringValue\", \"string_value\": \"\"}}"
            },
            {
              "Key": "mr_str:author",
              "Value": "mmortari"
            },
            {
              "Key": "mr_str:model_format_version",
              "Value": "1"
            },
            {
              "Key": "mr_str:id",
              "Value": "0"
            },
            {
              "Key": "mr_str:model_format_name",
              "Value": "onnx"
            },
            {
              "Key": "org.opencontainers.image.created",
              "Value": "2024-04-30T13:37:45Z"
            }
          ],
          "MediaType": "application/vnd.oci.image.manifest.v1+json",
          "ArtifactType": "mr/manifest",
          "Size": 1613,
          "Digest": "sha256:0d2c41aff6f92dacf7d1732997771db6f27a3eb7d304e854e40021d8493dc249"
        }
      ]
    }
  }
}
```