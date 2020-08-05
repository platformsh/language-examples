# Language examples design spec

* Every language is its own container, named for the language.  It should run the most recent version of the language possible.
* All services should be named to their version, and thus the name updated when the version is updated.  That sidesteps the upgrade problems that various service types suffer from.
* Each container should connect to every service possible.
* Every container should respond to requests at `/foo` with the source code example to connect to the `foo` service.
* Every container should respond to requests at `/foo/output` with the output of the source code example. That is, all source code examples should be "live".
* The example source and output should be "bare", not full HTML pages, as they are intended to be embedded into other resources.
* The example source should be reasonably documented, as it will be shown to users.
* Every container should respond to requests at `/` with a collapsible collection of all services and the output of them. (See PHP as the reference implementation.)
* Responses to any other URL should get the bare string "Sorry, no sample code is available."
* Every container should make use of the appropriate Platform.sh client library to the extent reasonable. It does NOT need to use parts of the library that are not relevant.
* The implementation for each language should follow standard practices and conventions for the language in question so as to make a good impression for that language.
* The implementation for each language can use popular 3rd party libraries where appropriate.
* Code examples should be as short as possible but no shorter.
