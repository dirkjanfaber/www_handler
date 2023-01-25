Python script taking care of handling web requests for `index.html` and
`logo.html` on a GX device.

This script is there to loose the dependency on PHP on the device.

The script only handles a few cases and are typically called via javascript:
- GET:
  - `/current_logo` - retrieves the current logo
  - `/reset_logo` - resets the logo
- PUT:
  - `/upload` - uploads the new logo
- POST:
  - `/salt` - retrieves the salt

# Nginx configuration

Make sure to proxy the following:
```
    location ~ ^/((current|reset)_logo|upload|salt) {
        proxy_pass                http://127.0.0.1:9249/$1;
        proxy_set_header          Host            $host;
        proxy_set_header          X-Real-IP       $remote_addr;
        proxy_set_header          X-Forwarded-For $proxy_add_x_forwarded_for;
        client_max_body_size      1M;
    }
```

# Startup

The `--port/-p` option allows for an alternative port to listen on. Note that the script
will only listen on localhost.
