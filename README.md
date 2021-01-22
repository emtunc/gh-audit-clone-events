# gh-audit-clone-events

POC Python code which demonstrates the addition of git audit events to the Github REST API; specifically clone events.

My understanding is that this only works for Github Enterprise Cloud customers.

The token you create only needs the `admin:org` permission.

You will occasionally get 502 server error responses back from the API - it's still technically BETA so perhaps they're still in the process of scaling up the API.

Example output:

```
Timestamp: 2021-01-22 01:13:10
Repo: my-org/repo-name
Actor: emtunc
Transport protocol: ssh
```
