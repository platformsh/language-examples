# Platform.sh Language Examples microsite

This project builds a working copy of every language/service combination that Platform.sh supports.  It primarily serves as a component of the documentation.  Only the latest version of each is included.

## Structure

* `services.yaml` contains the latest version of every service Platform.sh offers that an application container can connect to.

* `/main` contains a trivial index container.

* Each other directory is an application container for the latest supportable version of each supported language.

* `routes.yaml` defines a route to each language container at `/$language`.

## App container specification

* Each container SHOULD connect to every service possible.
* Each container MUST gracefully handle running locally.
* Each container MUST gracefully handle running in a subdirectory itself, based on the Platform.sh route.
* `/$service` MUST respond with a code example to connect to `$service`.  It should be a bare string, not HTML.
* `/$service/output` MUST respond with the output of running the code for that service.  That is, all code examples are "life".  It should be a bare string, not HTML.
* `/` MUST respond with a collapsible collection of all services and the output of them. (See PHP as the reference implementation.)
* All other paths MUST respond with the bare string "Sorry, no sample code is available."
* Every container SHOULD make use of the appropriate Platform.sh client library to the extent reasonable. It does NOT need to use parts of the library that are not relevant.
* The implementation for each language SHOULD follow standard practices and conventions for the language in question so as to make a good impression for that language.
* The implementation for each language MAY use popular 3rd party libraries where appropriate, but keep the overhead small.
* Code examples should be as short as possible but no shorter.

## License

The license for the projects built by this tool vary.

All code unique to this repository is released under the [MIT License](LICENSE.md).
