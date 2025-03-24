# Module copy-cloud-config

This module allows you to copy Viam cloud config to a running Viam machine and restart it (overwriting the existing cloud config for that machine).
This is helpful if you are replacing hardware but want to bring that up with the same machine config as the previous hardware.

NOTE: This module writes to a file location you specify, which is a potentially destructive operation - be sure you know what you are doing!

## Model mcvella:copy-cloud-config:copy-cloud-config

### Configuration

The following attribute template can be used to configure this model:

```json
{
"part_id": <string>,
"api_key_id": <string>,
"api_key": <string>,
"config_location": <string>
}
```

#### Attributes

The following attributes are available for this model:

| Name          | Type   | Inclusion | Description                |
|---------------|--------|-----------|----------------------------|
| `part_id` | string  | Required  | The part id from which you wish to copy cloud config. |
| `api_key_id` | string | Required  | An api_key_id that has access to the part_id. |
| `api_key` | string | Required  | An api_key that has access to the part_id. |
| `config_location` | string | Optional  | The location to write the Viam cloud config to - defaults to /etc/viam.json. |
