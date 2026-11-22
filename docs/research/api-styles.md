# Research: API styles

Scope: which API styles exist; how REST, gRPC and GraphQL compare (features, strengths and weaknesses, when to use each for browser/public APIs vs service-to-service, payload format and size: JSON vs Protocol Buffers); the Python libraries we will use for each.
Out of scope: authentication and authorization, API gateways, service meshes, HTTP/3, GraphQL federation, gRPC load balancing, and benchmark numbers (our own script in `examples/api/` will measure sizes later).

Every claim is followed by its source in brackets. Sources read on 2026-11-22. RFCs were read as plain text from rfc-editor.org. Editions and versions are listed under Sources.

Labels used in this note:

- "derived from …" means the claim follows from the cited facts, but no source states it in those words.
- "(vendor, cross-check)" marks a vendor page used only to cross-check.
- "(community spec)" marks a specification written by a community group, not a standards body.

Short names used in brackets:

- **Fielding 2000** = Roy T. Fielding, *Architectural Styles and the Design of Network-based Software Architectures*, PhD dissertation, 2000 (chapter 5 is REST, chapter 6 is the evaluation).
- **Fielding 2008** = Roy T. Fielding, "REST APIs must be hypertext-driven", blog post, 20 Oct 2008.
- **GraphQL spec** = GraphQL specification, September 2026 edition.
- **GoH** = GraphQL over HTTP specification, September 2026 edition.
- **gRPC HTTP/2 protocol** = `doc/PROTOCOL-HTTP2.md` in the grpc/grpc repository.
- **gRPC-Web protocol** = `doc/PROTOCOL-WEB.md` in the grpc/grpc repository.
- **gRPC status codes doc** = `doc/statuscodes.md` in the grpc/grpc repository.
- **OAS** = OpenAPI Specification v3.2.1.

## Terms

Full names:
API = Application Programming Interface [Fielding 2000 §6.5.1];
REST = Representational State Transfer [Fielding 2000 ch. 5 title];
RPC = Remote Procedure Call [RFC 5531 Abstract; protobuf.dev proto3 guide, "Defining Services"];
gRPC = "gRPC Remote Procedure Calls" (a recursive name) [grpc.io FAQ, "What does gRPC stand for?"];
GraphQL is not expanded by its spec; it calls itself "a query language and execution engine" [GraphQL spec, Introduction];
HTTP = Hypertext Transfer Protocol [RFC 9110 title];
HTTP/2 = version 2 of HTTP [RFC 9113 title];
HPACK = the header compression format for HTTP/2 (RFC 7541 gives no expansion of the letters) [RFC 7541 Abstract];
JSON = JavaScript Object Notation [RFC 8259 title];
IDL = Interface Definition Language [grpc.io Introduction to gRPC];
OAS = OpenAPI Specification, OAD = OpenAPI Description [OAS "What is the OpenAPI Specification?", §2];
URI = Uniform Resource Identifier [RFC 9110 §3.1];
CDN = content delivery network [graphql.org/learn/performance, "GET requests for queries"];
CSRF = Cross-Site Request Forgery [GoH §6.2.3];
CNCF = Cloud Native Computing Foundation [grpc.io FAQ, "Who's using this and why?"];
TLV = Tag-Length-Value [protobuf.dev Encoding, "Message Structure"];
MSB = most significant bit [protobuf.dev Encoding, "Base 128 Varints"];
ONC = Open Network Computing, XDR = eXternal Data Representation [RFC 5531 Abstract, §1];
SSE = Server-Sent Events [HTML Living Standard §9.2 title];
SOAP is no longer an acronym [SOAP 1.2 Part 1 §1, Note].

- **API style**: none of the sources read defines this term. The closest defined term is "architectural style": a coordinated set of constraints on the roles of architectural elements and the relationships allowed between them. [Fielding 2000 §1.5]
- **Network-based API**: an on-the-wire syntax, with defined semantics, for application interactions. [Fielding 2000 §6.5.1]
- **Resource**: any information that can be named, for example a document, a person, or "today's weather". [Fielding 2000 §5.2.1.1] HTTP calls the target of a request a "resource" and does not limit what it can be. [RFC 9110 §3.1]
- **Representation**: a sequence of bytes plus metadata that describes those bytes; it captures the current or intended state of a resource. [Fielding 2000 §5.2.1.2; RFC 9110 §3.2]
- **Media type**: the data format of a representation. [Fielding 2000 §5.2.1.2]
- **Uniform interface**: one generic interface shared by all components, made of four constraints: identification of resources, manipulation of resources through representations, self-descriptive messages, and hypermedia as the engine of application state. [Fielding 2000 §5.1.5]
- **Stateless**: each request carries all information needed to understand it; the server keeps no session context, so session state lives on the client. [Fielding 2000 §5.1.3]
- **Safe method**: a method whose meaning is essentially read-only; the client does not request a state change. GET, HEAD, OPTIONS and TRACE are safe. [RFC 9110 §9.2.1]
- **Idempotent method**: a method where many identical requests have the same intended effect as one. PUT, DELETE and the safe methods are idempotent. [RFC 9110 §9.2.2]
- **Contract / schema**: a machine-readable description of what an API offers. In OpenAPI it is an interface description for HTTP APIs [OAS §2]; in GraphQL it is the service's type system, called its "schema" [GraphQL spec §3.3]; in gRPC it is the service definition in a `.proto` file [grpc.io Core concepts, "Service definition"].
- **IDL (Interface Definition Language)**: a language for describing a service interface and its messages. gRPC uses Protocol Buffers as its IDL by default. [grpc.io Core concepts, "Service definition"] GraphQL also includes an IDL for describing a type system. [GraphQL spec §3]
- **Protocol Buffers (Protobuf)**: a language-neutral, platform-neutral, extensible mechanism for serializing structured data. [protobuf.dev Overview]
- **Service definition**: a list of methods that can be called remotely, with their parameters and return types. [grpc.io Core concepts, "Service definition"]
- **Unary RPC**: the client sends one request and gets one response back, like a normal function call. [grpc.io Core concepts, "Service definition"]
- **Streaming RPC**: one or both sides send a sequence of messages over a stream: server streaming, client streaming, or bidirectional streaming. [grpc.io Core concepts, "Service definition"]
- **Deadline**: a point in time past which a client will not wait for a response; a timeout is the same idea expressed as a duration. [grpc.io Deadlines guide, "Overview"]
- **Multiplexing**: carrying many concurrently open streams on one HTTP/2 connection, with frames from different streams interleaved. [RFC 9113 §5]
- **Query**: a GraphQL operation that is a read-only fetch. [GraphQL spec §2.4]
- **Mutation**: a GraphQL operation that is a write followed by a fetch. [GraphQL spec §2.4]
- **Subscription**: a GraphQL operation that is a long-lived request, fetching data in response to a sequence of events over time. [GraphQL spec §2.4]
- **Resolver**: the internal function a type provides to produce the value of one field. [GraphQL spec §6.4.2] Each field on each type is backed by a resolver written by the server developer. [graphql.org/learn/execution, "Field resolvers"]
- **Introspection**: querying a GraphQL service's own schema using GraphQL itself. [GraphQL spec §4]
- **Over-fetching / under-fetching**: the GraphQL spec names both and says a selection set avoids them by returning exactly the requested data and nothing more. [GraphQL spec §2.5] The spec does not define the two words further. Working reading, derived from §2.5 and §1: over-fetching is receiving fields you did not need; under-fetching is not receiving enough in one request, so more requests are needed. [derived from GraphQL spec §1, §2.5; graphql.org/learn/introduction, "Query exactly what you need"]
- **N+1 problem**: one request to a data source (for a list) leads to N more requests to resolve fields of each item in it. [graphql.org/learn/performance, "The N+1 Problem"]
- **Persisted query / persisted document**: a GraphQL document stored on the server under an identifier, usually a hash, so the client sends only the identifier. "Persisted queries" is the legacy name. [graphql.org/learn/security, "Trusted documents"; graphql.org/learn/performance, "GET requests for queries"]
- **Trusted document**: a persisted document judged not to be malicious, for example because it was written by your developers and code-reviewed; the server executes only known document IDs. [graphql.org/learn/security, "Trusted documents"]

## 1. The landscape: which API styles exist

One line each. None of the sources gives an official list of "API styles"; this list comes from the topic plan.

- **REST**: an architectural style for distributed hypermedia systems, defined by a set of constraints, with a uniform interface at its centre. [Fielding 2000 ch. 5 introduction, §5.1.5]
- **RPC (Remote Procedure Call) in general**: the caller sends a call message with the procedure's parameters and waits for a reply message with its results, like a local procedure call. [RFC 5531 §4] What sets RPC apart is that the protocol names a procedure and passes it a fixed set of parameters. [Fielding 2000 §6.5.2]
- **gRPC**: a modern, open source, high-performance RPC framework that can run in any environment. [grpc.io About]
- **GraphQL**: a query language and execution engine for describing and performing the capabilities and requirements of data models for client-server applications. [GraphQL spec, Introduction]
- **SOAP 1.2**: a lightweight protocol for exchanging structured information, defined with XML technologies, that can run over a variety of underlying protocols. [SOAP 1.2 Part 1, Abstract]
- **JSON-RPC 2.0**: a stateless, light-weight RPC protocol that uses JSON and is transport agnostic (in-process, sockets, HTTP and others). [JSON-RPC 2.0 §1]
- **WebSocket**: a protocol for two-way communication between browser code and a server: an opening handshake, then message framing over TCP. [RFC 6455 Abstract]
- **Server-Sent Events**: the `EventSource` browser interface, which lets a server push data to a web page over HTTP using the `text/event-stream` format. [HTML Living Standard §9.2.1]
- **Webhooks**: HTTP callbacks by which one service notifies another of events; a sort of "reverse API". [Standard Webhooks spec v1.0.0, "What are Webhooks?" (community spec)]
  - No IETF RFC that standardizes generic webhooks was found in this research (see Open questions).
  - Standard Webhooks is a community spec; its steering committee members are employees of API and webhook vendors. [standardwebhooks.com, "Technical Steering Committee" (community spec)]
  - W3C WebSub is a W3C Recommendation for hub-based publish/subscribe "based on HTTP web hooks". [WebSub Abstract]
  - OpenAPI can describe webhooks an API provider may send, through its `webhooks` field. [OAS §4.1]
- **AsyncAPI**: a specification for describing message-driven APIs in a machine-readable format, for any protocol (for example AMQP, MQTT, WebSockets, Kafka, HTTP). It describes APIs; it is not itself a wire protocol. [AsyncAPI 3.1.0, Introduction]
- **tRPC**: a TypeScript library for typesafe APIs "without schemas or code generation", using TypeScript's type inference, aimed at full-stack TypeScript projects. It describes itself as combining concepts from REST and GraphQL. [trpc.io/docs, Introduction] It is not usable from Python. [derived from trpc.io/docs, Introduction]
- **OpenAPI is not a style.** It is a language-agnostic interface description for HTTP APIs. [OAS §2]

## 2. REST

### What it is / constraints

- REST is a hybrid style built from several network-based styles plus constraints that define a uniform connector interface. [Fielding 2000 ch. 5 introduction]
- It is derived by starting from the "null style" (no constraints) and adding constraints one at a time. [Fielding 2000 §5.1.1]
- **Client-server.** Separating user interface from data storage makes the UI portable and the server simpler, and lets both sides evolve independently. [Fielding 2000 §5.1.2]
- **Stateless.** Each request must contain all information needed to understand it. Session state is kept entirely on the client. [Fielding 2000 §5.1.3]
  - Gains: visibility (a monitor sees the whole request), reliability (easier recovery from partial failure) and scalability (the server frees resources quickly). [Fielding 2000 §5.1.3]
  - Costs: repeated per-request data, and less server control over consistent behaviour. [Fielding 2000 §5.1.3]
- **Cache.** Response data must be labelled, implicitly or explicitly, as cacheable or not. A client cache may reuse a cacheable response for later equivalent requests. [Fielding 2000 §5.1.4]
  - Gain: some interactions disappear, which cuts average latency. Cost: stale cached data can reduce reliability. [Fielding 2000 §5.1.4]
- **Uniform interface.** This is the central feature that sets REST apart from other network-based styles. [Fielding 2000 §5.1.5]
  - Gains: a simpler overall architecture, better visibility of interactions, and implementations decoupled from the services they provide. [Fielding 2000 §5.1.5]
  - Cost: it "degrades efficiency", because data moves in a standardized form rather than one specific to an application's needs. [Fielding 2000 §5.1.5]
  - The interface is designed to be efficient for large-grain hypermedia data transfer, the common case of the Web, and is "not optimal for other forms of architectural interaction". [Fielding 2000 §5.1.5]
  - Its four sub-constraints: identification of resources; manipulation of resources through representations; self-descriptive messages; hypermedia as the engine of application state. [Fielding 2000 §5.1.5]
- **Layered system.** Each component sees only the layer it talks to. This allows intermediaries for load balancing, shared caches and security policy at organizational boundaries. [Fielding 2000 §5.1.6]
  - Cost: layers add overhead and latency; shared caches can offset this. [Fielding 2000 §5.1.6]
- **Code-on-demand.** Clients may download and run code (applets, scripts). It is the only optional constraint. [Fielding 2000 §5.1.7]
- REST is pull-based: consumers usually pull representations. Fielding notes this is less efficient for one client watching one resource, but says an unregulated push model is infeasible at Web scale. [Fielding 2000 §5.4]
- Fielding summarizes REST as emphasizing scalability of component interactions, generality of interfaces, independent deployment, and intermediaries. [Fielding 2000 §5.5]
- "HTTP is not RPC": what makes HTTP different is that requests are directed to resources through a generic interface whose standard semantics intermediaries can interpret. [Fielding 2000 §6.5.2]
- RPC mechanisms, by contrast, "are defined in terms of language APIs, not network-based applications". [Fielding 2000 §6.5.2]
- RFC 9110 says HTTP "is designed to be usable as an interface to distributed object systems", with the method invoked much like a remote method invocation; but its standard methods are not resource-specific, citing REST for why. [RFC 9110 §9.1] This is a nuance, not a contradiction, with Fielding's "HTTP is not RPC". [derived from RFC 9110 §9.1 and Fielding 2000 §6.5.2]
- Fielding 2008: if application state is not driven by hypertext, "it cannot be RESTful and cannot be a REST API". [Fielding 2008]
- Fielding 2008 lists rules most often broken by "so-called REST APIs", including: a REST API must not define fixed resource names or hierarchies, and must be entered with no prior knowledge beyond the initial URI and standard media types. [Fielding 2008]
- Consequence: many HTTP APIs commonly called "REST" (fixed URL paths documented in advance, for example in an OpenAPI file) do not meet the hypertext constraint as Fielding states it. [derived from Fielding 2008 rules 4 and 6, and OAS §4.8 (the Paths Object "holds the relative paths to the individual endpoints")]

#### HTTP, the protocol REST was applied to

- HTTP methods are not resource-specific; RFC 9110 cites REST: "uniform interfaces provide for better visibility and reuse". [RFC 9110 §9.1]
- Standard methods: GET (transfer a current representation), HEAD, POST (resource-specific processing of the request content), PUT (replace all current representations), DELETE, CONNECT, OPTIONS, TRACE. [RFC 9110 §9.1, table]
- Safe methods exist so that crawlers and cache pre-fetching can work "without fear of causing harm". [RFC 9110 §9.2.1]
- Idempotent requests can be repeated automatically after a connection failure. [RFC 9110 §9.2.2]
- A client SHOULD NOT automatically retry a non-idempotent request unless it knows the request is idempotent or was never applied. A proxy MUST NOT automatically retry non-idempotent requests. [RFC 9110 §9.2.2]
- GET is "the primary mechanism of information retrieval and the focus of almost all performance optimizations". [RFC 9110 §9.3.1]
- Content negotiation picks one representation among several (formats, languages, encodings). RFC 9110 defines three patterns: proactive, reactive and request-content negotiation. [RFC 9110 §12]
- Caching:
  - A method must explicitly allow caching. RFC 9110 defines caching for GET, HEAD and POST, but "the overwhelming majority of cache implementations only support GET and HEAD". [RFC 9110 §9.2.3]
  - A POST response is cacheable only with explicit freshness information and a `Content-Location` equal to the POST target; it can then serve a later GET or HEAD, never another POST. [RFC 9110 §9.3.3]
  - The cache key is at least the request method and target URI; many caches only cache GET and use only the URI as the key. [RFC 9111 §2]
  - A cache must forward unsafe requests to the origin; it may not answer them itself. [RFC 9111 §4]
  - A stale stored response can be revalidated with `Last-Modified`/`If-Modified-Since` or `ETag`/`If-None-Match`. [RFC 9111 §4.3.1]

### Contract (OpenAPI), payload (usually JSON), errors (status codes)

Contract:

- REST itself defines no contract file. Fielding 2008 says a REST API should spend almost all of its descriptive effort on media types and link relations, not on which methods to use on which URIs. [Fielding 2008]
- OpenAPI defines "a standard, language-agnostic interface to HTTP APIs" so humans and computers can learn a service's capabilities without its source code. [OAS §2] It says "HTTP APIs", not "REST APIs". [OAS §2]
- An OpenAPI Description is used by documentation tools, code generators for servers and clients, and testing tools. [OAS §2]
- An OpenAPI document is a JSON object, written in JSON or YAML. [OAS §3]
- The API's own request and response bodies are not required to be JSON or YAML. [OAS §3, Note]
- The Schema Object is, by default, a superset of JSON Schema Draft 2020-12. [OAS §4.24]
- OAS 3.2.1 can describe sequential and streaming media types, including `text/event-stream`, with an `itemSchema` applied to each item. [OAS §4.14.3.1, §4.14.3.1.1]
- FastAPI generates an OpenAPI schema for the whole API automatically and serves it at `/openapi.json`; its tutorial example shows `"openapi": "3.1.0"`. [FastAPI docs, First Steps, "OpenAPI"]

Payload:

- Neither Fielding nor RFC 9110 requires JSON. Representations come in media types, for example an HTML document or a JPEG image. [Fielding 2000 §5.2.1, Table 5-1; RFC 9110 §3.2]
- No primary source read says REST APIs "usually" use JSON. FastAPI returns JSON responses by default. [FastAPI docs, Custom Response]
- JSON is a text format for serializing structured data. [RFC 8259 §1]
- JSON has four primitive types (string, number, boolean, null) and two structured types (object, array). [RFC 8259 §1]
- A JSON object is an unordered collection of name/value pairs; a name is a string. [RFC 8259 §1, §4]
- JSON exchanged outside a closed ecosystem MUST be UTF-8. [RFC 8259 §8.1]
- The media type is `application/json`. [RFC 8259 §11]
- Integers in the range [-(2^53)+1, (2^53)-1] are interoperable; implementations may limit range and precision. [RFC 8259 §6]
- Insignificant whitespace is allowed around the six structural characters. [RFC 8259 §2]

Errors:

- A status code is a three-digit integer from 100 to 599. The first digit is the class: 1xx informational, 2xx successful, 3xx redirection, 4xx client error, 5xx server error. [RFC 9110 §15]
- A client MUST understand the class of any status code, and treats an unknown code as the x00 code of its class. [RFC 9110 §15]
- FastAPI: client errors use codes in the 400 range, raised with `HTTPException`. [FastAPI docs, Handling Errors]

### Strengths / weaknesses

Only as the sources state them, or as directly follows from cited facts.

Strengths:

- Scalability, generality of interfaces, independent deployment of components, and intermediaries that cut latency, enforce security and wrap legacy systems. [Fielding 2000 §5.5]
- Caching: "the most efficient network request is one that doesn't use the network". [Fielding 2000 §5.3.3] HTTP caches work best with GET. [RFC 9110 §9.2.3; RFC 9111 §2]
- Standard method semantics let clients retry idempotent requests and let crawlers and pre-fetchers use safe ones. [RFC 9110 §9.2.1, §9.2.2]
- Intermediaries can understand requests "almost as well as" the origin, which suits an "Internet-scale, multi-organization" system. [Fielding 2000 §6.5.2]

Weaknesses:

- The uniform interface costs efficiency, and is not optimal for non-hypermedia interactions. [Fielding 2000 §5.1.5]
- Statelessness repeats data in every request. [Fielding 2000 §5.1.3]
- Layers add overhead and latency. [Fielding 2000 §5.1.6]
- Pull-only: watching one resource for changes is less efficient. [Fielding 2000 §5.4]
- In most client-server applications without GraphQL, the server decides the shape of data returned by each endpoint. [GraphQL spec §1] (This is GraphQL's framing; Fielding names the same trade-off as the efficiency cost of a standardized form. [Fielding 2000 §5.1.5])

## 3. gRPC (and Protocol Buffers)

### What it is, IDL, 4 RPC kinds, deadlines, status codes

- gRPC is an open source, high-performance RPC framework. [grpc.io About]
- Google built it as the next version of its internal RPC system, Stubby, and open-sourced it in March 2015. [grpc.io About, "The story behind gRPC"]
- It is a CNCF project, licensed under Apache 2.0. [grpc.io FAQ]
- A client calls a method on a server on another machine "as if it were a local object". [grpc.io Introduction to gRPC, "Overview"]
- A service is defined by its methods, their parameters and their return types. [grpc.io Core concepts, "Service definition"]
- By default gRPC uses Protocol Buffers both as its IDL and as its message format; other formats such as JSON can be used. [grpc.io Introduction to gRPC; grpc.io Core concepts, "Service definition"]
- One design principle is "Payload Agnostic": protocol buffers, JSON, XML and Thrift should all be possible. [grpc.io blog, "gRPC Motivation and Design Principles"]
- Workflow: write a `.proto` file; `protoc` with the gRPC plugin generates client and server code. [grpc.io Introduction to gRPC]
- The server implements the methods. The client calls a local "stub" with the same methods, which wraps parameters in protobuf messages and sends them. [grpc.io Core concepts, "Using the API"]
- Most languages offer both synchronous and asynchronous APIs. [grpc.io Core concepts, "Synchronous vs. asynchronous"]

Four kinds of method [grpc.io Core concepts, "Service definition"]:

1. **Unary**: one request, one response. `rpc SayHello(HelloRequest) returns (HelloResponse);`
2. **Server streaming**: one request, a stream of responses. `returns (stream HelloResponse)`
3. **Client streaming**: a stream of requests, one response. `rpc LotsOfGreetings(stream HelloRequest) ...`
4. **Bidirectional streaming**: both sides stream; the two streams are independent.

- gRPC guarantees message ordering within one RPC call. [grpc.io Core concepts, "Service definition"]
- The response ends with status details (a code and an optional message) and optional trailing metadata. [grpc.io Core concepts, "Unary RPC"]

Deadlines and cancellation:

- A client can say how long it will wait; when that passes, the RPC ends with `DEADLINE_EXCEEDED`. [grpc.io Core concepts, "Deadlines/Timeouts"]
- By default gRPC sets no deadline, so a client may wait "effectively forever"; the guide says to always set a realistic deadline. [grpc.io Deadlines guide, "Deadlines on the Client"]
- A server cancels a call automatically (status `CANCELLED`) once the client's deadline has passed. [grpc.io Deadlines guide, "Deadlines on the Server"]
- Some implementations propagate the deadline to outgoing calls, converted to a timeout to avoid clock skew. [grpc.io Deadlines guide, "Deadline Propagation"]
- On the wire, the deadline is the `grpc-timeout` header; if it is missing, the server assumes an infinite timeout. [gRPC HTTP/2 protocol, "Requests"]
- Client and server decide independently whether a call succeeded, and their conclusions may differ. [grpc.io Core concepts, "RPC termination"]
- Either side can cancel at any time. Changes made before a cancellation are not rolled back. [grpc.io Core concepts, "Cancelling an RPC"]
- Cancellation should propagate to upstream calls; the server handler must check for it itself. [grpc.io Cancellation guide, "Overview", "Cancelling an RPC Call on the Client Side"]

Metadata and channels:

- Metadata is key-value data about one call, such as authentication details. Keys are case-insensitive ASCII; keys ending in `-bin` carry binary values; keys must not start with `grpc-`. [grpc.io Core concepts, "Metadata"]
- Binary metadata values are base64-encoded on the wire. [gRPC HTTP/2 protocol, "Requests"]
- A channel is a connection to a gRPC server on a given host and port; it has state such as connected and idle. [grpc.io Core concepts, "Channels"]

Status codes:

- gRPC defines 17 status codes, numbered 0 (`OK`) to 16 (`UNAUTHENTICATED`). [gRPC status codes doc; grpc.io Status Codes guide]
- Every RPC returns a status made of an integer code and a string message. [gRPC status codes doc]
- Seven codes are never generated by the gRPC library, only by application code: `INVALID_ARGUMENT`, `NOT_FOUND`, `ALREADY_EXISTS`, `FAILED_PRECONDITION`, `ABORTED`, `OUT_OF_RANGE`, `DATA_LOSS`. [gRPC status codes doc; grpc.io Status Codes guide]
- There is no fixed list of codes that are safe to retry; each application decides. [gRPC status codes doc]
- gRPC calls are not assumed idempotent unless explicitly marked. [gRPC HTTP/2 protocol, "Idempotency and Retries"]
- grpc.io's own comparison with REST: gRPC "largely follows HTTP semantics over HTTP/2" but allows full-duplex streaming, uses static paths for faster dispatch, and has "formalized a set of errors" it finds more applicable to APIs than HTTP status codes. [grpc.io FAQ, "Why is gRPC better/worse than REST?"]

### On the wire (HTTP/2, length-prefixed framing, trailers)

- The protocol is specified on top of HTTP/2 framing. [gRPC HTTP/2 protocol, "Introduction"]
- A request is: request headers, zero or more length-prefixed messages, end of stream. [gRPC HTTP/2 protocol, "Outline"]
- A response is: response headers, zero or more length-prefixed messages, trailers; or a "Trailers-Only" response for an immediate error. [gRPC HTTP/2 protocol, "Outline", "Responses"]
- Request headers include `:method POST`, `:path /<Service-Name>/<method name>`, `te: trailers` (used to detect incompatible proxies) and `content-type: application/grpc` with an optional `+proto` or `+json` suffix. [gRPC HTTP/2 protocol, "Requests"]
- With Protobuf, the content type is `application/grpc+proto` and the service name is the proto package plus the service name. [gRPC HTTP/2 protocol, "Appendix A"]
- Each message is framed as: a 1-byte compressed flag, a 4-byte big-endian length, then the message bytes. [gRPC HTTP/2 protocol, "Requests"] So every message carries a 5-byte prefix. [derived from the same]
- Flag 1 means the message is compressed with the algorithm named in `grpc-encoding` (identity, gzip, deflate, snappy, or custom). Each message gets a new compression context. [gRPC HTTP/2 protocol, "Requests"]
- The response's HTTP status is `:status 200`. The gRPC status goes in trailers as `grpc-status` and `grpc-message`, even when the status is OK. [gRPC HTTP/2 protocol, "Responses"]
- Because a gRPC error response uses HTTP 200, a gRPC server SHOULD answer a non-gRPC content type with HTTP 415, so other HTTP/2 clients do not read an error as success. [gRPC HTTP/2 protocol, "Requests"]
- HTTP/2 stream IDs are used as call IDs. [gRPC HTTP/2 protocol, "Stream Identification"]
- HTTP/2 DATA frame boundaries have no relation to gRPC message boundaries. [gRPC HTTP/2 protocol, "Data Frames"]
- An HTTP/2 `RST_STREAM` error maps to gRPC codes; for example `REFUSED_STREAM` maps to `UNAVAILABLE` (safe to retry elsewhere). [gRPC HTTP/2 protocol, "Errors"]
- The protocol document links to RFC 7540 for HTTP/2; RFC 9113 obsoletes RFC 7540. [gRPC HTTP/2 protocol, "Introduction"; RFC 9113 header]

What HTTP/2 gives gRPC:

- HTTP/1.0 allowed one outstanding request per TCP connection; HTTP/1.1 pipelining only partly helped, so clients opened several connections. [RFC 9113 §1]
- HTTP/2 interleaves messages on one connection and codes header fields efficiently. [RFC 9113 §1]
- One HTTP/2 connection can hold many concurrently open streams, with frames from different streams interleaved. [RFC 9113 §5]
- HTTP/2 uses binary framing; every frame starts with a fixed 9-octet header. [RFC 9113 §1, §4.1]
- Header fields are compressed with HPACK. [RFC 9113 §4.3; RFC 7541 Abstract]
- An HTTP/2 message is a HEADERS frame, zero or more DATA frames, and optionally a final HEADERS frame carrying the trailer section. [RFC 9113 §8.1]
- HTTP/2 does not solve TCP head-of-line blocking. [RFC 9113 §1]
- Trailers are fields sent after the content, useful for things like post-processing status. [RFC 9110 §6.5] HTTP/1.1 can carry them only with chunked transfer coding. [RFC 9110 §6.5.1]
- A gRPC channel uses zero or more HTTP/2 connections; each connection has a limit on concurrent streams, and extra RPCs queue on the client. [grpc.io Performance Best Practices, "General"]

### Protobuf encoding and why it is small

- Protobuf is "like JSON, except it's smaller and faster", and generates native language bindings. [protobuf.dev Overview] The page gives no numbers for "smaller" or "faster". [protobuf.dev Overview]
- Protobuf is a combination of a definition language (`.proto` files), generated code, runtime libraries, and a serialization format. [protobuf.dev Overview]
- It targets typed, structured data packets "up to a few megabytes in size". [protobuf.dev Overview, "What Problems Does Protobuf Solve?"]
- Serialized messages must be smaller than 2 GiB. [protobuf.dev Encoding, "Encoded Proto Size Limitations"]

Field numbers, not names:

- A message is a series of key-value pairs. The binary format uses the field number as the key; field names and types are known only from the `.proto` file. [protobuf.dev Encoding, "Message Structure"]
- Each field gets a number from 1 to 536,870,911; 19,000–19,999 are reserved. [protobuf.dev proto3 guide, "Assigning Field Numbers"]
- A field number cannot change once the message type is in use, because it identifies the field on the wire. [protobuf.dev proto3 guide, "Assigning Field Numbers"]
- Field numbers 1–15 take one byte to encode; 16–2047 take two bytes. Use 1–15 for the most frequently set fields. [protobuf.dev proto3 guide, "Assigning Field Numbers"]
- Each record is a field number, a wire type and a payload ("Tag-Length-Value"). The wire type tells a parser how big the payload is, so old parsers can skip fields they don't know. [protobuf.dev Encoding, "Message Structure"]
- The tag is a varint: `(field_number << 3) | wire_type`. There are six wire types: VARINT, I64, LEN, SGROUP, EGROUP (both deprecated) and I32. [protobuf.dev Encoding, "Message Structure"]

Varints and the `08 96 01` example:

- A varint encodes an unsigned 64-bit integer in 1 to 10 bytes; small values use fewer bytes. [protobuf.dev Encoding, "Base 128 Varints"]
- Each byte's MSB is a continuation bit; the low 7 bits are payload, in little-endian groups. [protobuf.dev Encoding, "Base 128 Varints"]
- 1 encodes as `01`; 150 encodes as `96 01`. [protobuf.dev Encoding, "Base 128 Varints"]
- `message Test1 { int32 a = 1; }` with `a = 150` serializes to three bytes: `08 96 01`. [protobuf.dev Encoding, "A Simple Message"]
- `08` is the tag: field 1, wire type 0 (VARINT). `96 01` is 150. [protobuf.dev Encoding, "Message Structure"]
- A string is a LEN record: tag, varint length, then UTF-8 bytes. `string b = 2` set to `"testing"` is `12 07 74 65 73 74 69 6e 67` (9 bytes). [protobuf.dev Encoding, "Length-Delimited Records"]
- A submessage is also LEN: `Test3 { Test1 c = 3; }` with `c.a = 150` is `1a 03 08 96 01` (5 bytes). [protobuf.dev Encoding, "Submessages"]
- `double` and `fixed64` take 8 bytes; `float` and `fixed32` take 4. [protobuf.dev Encoding, "Non-varint Numbers"]
- A negative `int32` or `int64` always uses all ten varint bytes. `sint32`/`sint64` use ZigZag encoding, so small negative numbers stay small. [protobuf.dev Encoding, "Signed Integers"]
- Repeated scalar numeric fields are "packed" into one LEN record by default. [protobuf.dev Encoding, "Repeated Elements"; protobuf.dev proto3 guide, "Repeated Fields are Packed by Default"]

Defaults and missing fields:

- A field that is not present is simply left out. "Huge" protos with few fields set are sparse. [protobuf.dev Encoding, "Missing Elements"]
- In proto3, an implicit-presence scalar field set to its default (zero, empty string, false) is not serialized. [protobuf.dev proto3 guide, "Specifying Field Cardinality", "Default Field Values"]
- For such fields, a reader cannot tell "set to the default" from "not set". The guide recommends `optional` fields, which record whether they were set. [protobuf.dev proto3 guide, "Specifying Field Cardinality", "Default Field Values"]

Schema evolution:

- Adding fields is wire-safe: old code ignores new fields, new code reads old messages with defaults. [protobuf.dev proto3 guide, "Binary Wire-safe Changes"; protobuf.dev Overview, "Updating Proto Definitions Without Updating Code"]
- Removing fields is safe if the field number is never reused (reserve it). [protobuf.dev proto3 guide, "Binary Wire-safe Changes", "Reserved Field Numbers"]
- Reusing a field number makes decoding ambiguous and can cause data corruption or leaked personal data. [protobuf.dev proto3 guide, "Consequences of Reusing Field Numbers"]
- Proto3 keeps unknown fields when parsing and writes them back out. Converting to JSON loses them. [protobuf.dev proto3 guide, "Unknown Fields"]

Where Protobuf is not a good fit [protobuf.dev Overview, "When Is Protobuf Not a Good Fit?"]:

- Data larger than a few megabytes (whole messages are loaded into memory).
- Comparing messages byte-for-byte: the same data can have many binary serializations.
- Compression: protobuf messages are not compressed.
- Large multi-dimensional float arrays (scientific formats are better).
- Self-description: you cannot fully interpret a message without its `.proto` file.
- Environments that require a formal standard: Protobuf is "not a formal standard of any organization".

ProtoJSON (the JSON mapping):

- Protobuf has a canonical JSON encoding for systems that don't use the binary format. [protobuf.dev proto3 guide, "JSON Mapping"]
- The binary format is the preferred format between two systems that both use Protobuf. [protobuf.dev proto3 guide, "JSON Mapping"]
- ProtoJSON keys are the lowerCamelCase field names; `int64` values are JSON strings; `bytes` are base64 strings. [protobuf.dev ProtoJSON Format, "Representation of each type"]
- ProtoJSON "is not as efficient as binary wire format and never will be": more CPU, and (except in rare cases) more space. [protobuf.dev ProtoJSON Format, "Non-goals of the Format"]
- ProtoJSON drops unknown fields and puts field names into messages, so renaming fields later is hard. [protobuf.dev ProtoJSON Format, "Non-goals of the Format"]

### Browsers (gRPC-Web, proxy needed)

- Because of browser limitations, gRPC-Web uses a different protocol from native gRPC, designed so a proxy can translate between them, "the most likely deployment model". [gRPC-Web protocol, introduction]
- A design goal is to decouple from HTTP/2 framing, which browsers do not expose and "will never" directly expose. [gRPC-Web protocol, "Design goals"]
- A 2019 guest post on grpc.io adds that a browser cannot force HTTP/2 and cannot access raw HTTP/2 frames. [grpc.io blog, "The state of gRPC in the browser", 2019] (This post is dated; used only for background.)
- gRPC-Web runs over any HTTP version and closes the stream with end-of-body. [gRPC-Web protocol, "HTTP wire protocols"]
- Content types: `application/grpc-web` (default `+proto`) and `application/grpc-web-text` (base64-encoded). [gRPC-Web protocol, "Content-Type"]
- Trailers travel inside the response body, marked by the MSB of the first byte of a gRPC frame. [gRPC-Web protocol, "Message framing"]
- gRPC-Web clients connect through a special proxy; the default is Envoy. [grpc-web README] Other options listed: the gRPC-Web Go proxy, Apache APISIX, Nginx, and server frameworks with built-in support such as Armeria (JVM) and Tonic (Rust). [grpc-web README, "Proxy Interoperability", "Server Frameworks with gRPC-Web support"]
- Supported RPC kinds: unary, and server streaming only in `grpcwebtext` mode. Client streaming and bidirectional streaming are not supported. [grpc-web README, "Streaming Support"]
- In the binary `grpcweb` mode, only unary calls are supported. [grpc-web README, "Wire Format Mode"]
- The gRPC-Web project is Generally Available. [grpc.io FAQ, "Can I use it in the browser?"]
- The protocol document says retries and caching "will" be specified later. [gRPC-Web protocol, "Other features"]
- Stale prediction: the protocol document expected gRPC-Web to become optional "in 1-2 years" once browsers could speak native gRPC via the WHATWG streams API. [gRPC-Web protocol, "Design goals"] The current README still says client and bidirectional streaming are not supported. [grpc-web README, "Streaming Support"]

### Strengths / weaknesses / usage scenarios per grpc.io

Usage scenarios as grpc.io states them:

- "Efficiently connecting polyglot services in microservices style architecture." [grpc.io About, "The main usage scenarios"]
- "Connecting mobile devices, browser clients to backend services." [grpc.io About, "The main usage scenarios"]
- "Generating efficient client libraries." [grpc.io About, "The main usage scenarios"]
- Low-latency, highly scalable distributed systems; mobile clients talking to a cloud server; designing a new protocol that must be accurate, efficient and language independent. [grpc.io FAQ, "Why would I want to use gRPC?"]
- It can connect services "in and across data centers", and also the "last mile" (devices, mobile apps, browsers). [grpc.io About]

Strengths as sources state them:

- Idiomatic client libraries in 11 languages; "highly efficient on wire"; bidirectional streaming over HTTP/2; pluggable auth, tracing, load balancing and health checking. [grpc.io About, "Core features"]
- A service is defined once in `.proto`; clients and servers in any supported language are generated. [grpc.io Python Basics tutorial, "Why use gRPC?"]
- Higher-level features that plain HTTP libraries usually lack: application-level flow control, cascading cancellation, load balancing and failover. [grpc.io FAQ, "Why is gRPC better than any binary blob over HTTP/2?"]
- Mobile: streaming and connection features help save bandwidth, use fewer TCP connections, and save CPU and battery. [grpc.io FAQ, "How does gRPC help in mobile application development?"]

Weaknesses and cautions as sources state them:

- Streams cannot be load balanced once started, are hard to debug, and can reduce scalability; use them only for a substantial benefit. [grpc.io Performance Best Practices, "General"]
- In gRPC Python, streaming RPCs are "much slower than unary RPCs", unlike other languages. [grpc.io Performance Best Practices, "Python"]
- No deadline by default. [grpc.io Deadlines guide]
- Browsers need gRPC-Web, a proxy, and lose client and bidirectional streaming. [grpc-web README]
- Messages are not self-describing without the `.proto` file. [protobuf.dev Overview]
- Generic HTTP caches will not cache gRPC responses, because every call is a POST and most caches only cache GET and HEAD. [derived from gRPC HTTP/2 protocol "Requests" (`:method POST`), RFC 9110 §9.2.3, RFC 9111 §2]
- Intermediaries that read only HTTP status codes see 200 for gRPC errors. [derived from gRPC HTTP/2 protocol, "Requests", "Responses"]

## 4. GraphQL

### What it is, schema, single endpoint, operations

- The spec defines GraphQL as "a query language and execution engine". [GraphQL spec, Introduction]
- graphql.org calls it "a query language for your API, and a server-side runtime for executing queries using a type system you define for your data". [graphql.org/learn/introduction]
- It was created in 2012; work on the open standard started in 2015. [GraphQL spec, Introduction]
- It is not a programming language for arbitrary computation and mandates no programming language or storage system. [GraphQL spec §1]
- Design principles: product-centric (driven by views and front-end engineers), hierarchical, strongly typed, client-specified response, self-describing. [GraphQL spec §1]
- A document holds one or more operations; with several, the client must name the one to run. [GraphQL spec §2.3]
- Three operation types: `query` (read-only fetch), `mutation` (write followed by fetch), `subscription` (long-lived, events over time). [GraphQL spec §2.4]
- A schema is the service's collective type system: its types, directives, and a root type for each operation type. [GraphQL spec §3.3]
- The query root type is required; mutation and subscription roots are optional. [GraphQL spec §3.3.1]
- Introspection lets a client query the schema with GraphQL itself; introspection names start with `__`. [GraphQL spec §4]
- Validation runs before execution. A service may skip it for a request it has already validated, for example by memoizing. [GraphQL spec §5]
- Top-level mutation fields execute serially, to avoid race conditions between side effects. [GraphQL spec §6.2.2]
- A resolver is often asynchronous because it reads a database or a networked service. [GraphQL spec §6.4.2]
- GraphQL requires no particular serialization format or transport. [GraphQL spec §6, Note; §7.2]
- JSON is the most common serialization format. [GraphQL spec §7.2.1]
- Response: an execution result is a map with a `data` entry, plus an `errors` entry only if errors were raised. [GraphQL spec §7.1.1]
- A response may contain partial data and a list of errors together. [GraphQL spec §7]
- A request error (parse, validation, unknown operation, bad variables) produces no `data` entry. It is "typically the fault of the requesting client". [GraphQL spec §7.1.3, §7.1.6]
- An execution error happens in one field; that field becomes null, siblings continue, and the error carries a `path`. It is "typically the fault of a GraphQL service". [GraphQL spec §7.1.6]
- Single endpoint: entities are not identified by URLs; a GraphQL server uses one URL, usually `/graphql`. [graphql.org/learn/serving-over-http, "API endpoint"] Ending the path with `/graphql` is "a common convention". [GoH §2]

### Over/under-fetching as graphql.org states it

- A selection set receives exactly the requested information "and nothing more, avoiding over-fetching and under-fetching data". [GraphQL spec §2.5]
- In most applications without GraphQL, the service determines the shape of data from each endpoint; a GraphQL response contains exactly what the client asks for. [GraphQL spec §1]
- A client can get the data it needs, in the expected shape, "with a single request". [graphql.org/learn/introduction, "Query exactly what you need"]
- "Minimizing over-fetching and making fewer roundtrips to the server" are listed as inherent performance benefits. [graphql.org FAQ, "How does GraphQL affect my product's performance?"]

### Over HTTP (GET/POST, status codes, media type)

From the GraphQL over HTTP spec, September 2026 edition:

- It extends the GraphQL spec, which "deliberately does not specify the transport layer"; HTTP is the most common choice. [GoH, Introduction]
- Subscriptions are out of its scope. [GoH §1, Note]
- Servers and clients MUST support JSON and MAY support other formats. [GoH §3]
- Media types: `application/json` for requests, `application/graphql-response+json` for responses. [GoH §3.1]
- A server MUST support POST and MAY support GET. [GoH §4]
- Request parameters: `query` (required; the document text, despite the name), `operationName`, `variables`, `extensions`. [GoH §4.1]
- A client MUST send `application/graphql-response+json` in its `Accept` header. [GoH §4.2]
- GET puts the parameters in the URL query string. GET MUST NOT run mutations; the server answers with a 4xx, 405 recommended, to keep HTTP's safe-method semantics. [GoH §4.3]
- POST carries a JSON body with `Content-Type: application/json`. [GoH §4.4]
- Status codes [GoH §5.4]:
  - `data` present and not null: MUST be 2xx.
  - `data` and no `errors`: SHOULD be 200.
  - `data` (even null) and `errors`: SHOULD be 294 "Partial Success".
  - No `data` (a request error): MUST be 4xx or 5xx. Examples: unparseable JSON body or GraphQL document → 400; not a well-formed request → 422; validation failure → 422; mutation via GET or unsupported method → 405; unsupported `Content-Type` → 415.
- 294 is a custom code defined by the GraphQL group, not registered with IANA. HTTP clients that don't know it must treat it as 200. [GoH §6.1]
- With `application/graphql-response+json`, clients should read the body to learn the outcome, whatever the status code. [GoH §5.4]
- A server MAY add validation rules such as depth and complexity limits. [GoH §5.2]
- `application/json` requests need a CORS preflight when sent cross-origin; form encodings may not, which opens CSRF risk. [GoH §6.2.3]

Where the sources disagree:

- graphql.org's "Serving over HTTP" page calls the GraphQL-over-HTTP spec a draft "not yet finalized". [graphql.org/learn/serving-over-http] A September 2026 edition was released on 2026-11-13. [github.com/graphql/graphql-over-http releases]
- The same graphql.org page says validation errors "typically" get a 400 status. [graphql.org/learn/serving-over-http, "Status Codes"] The September 2026 edition says validation failure SHOULD get 422. [GoH §5.4]
- graphql.org says a 2xx is used for partial results because HTTP has no "partial success" code. [graphql.org/learn/serving-over-http, "Status Codes"] The September 2026 edition recommends its own 294. [GoH §5.4, §6.1] (294 is still a 2xx code, so the two are compatible in class.)

### Caching, N+1, security (depth/complexity, trusted documents), versioning stance

Caching:

- In an endpoint-based API the URL is a global identifier for caching; GraphQL has no URL-like primitive, so the best practice is a globally unique `id` field. [graphql.org/learn/caching]
- graphql.org says GraphQL is "as cacheable as any API that enables parameterized requests", such as a REST endpoint with query parameters. [graphql.org/learn/performance]
- GET requests for queries can use HTTP caching and CDNs when the server sends caching headers. [graphql.org/learn/performance, "GET requests for queries"]
- Long documents may exceed URL length limits; persisted queries (trusted documents or automatic persisted queries) send a hash instead. [graphql.org/learn/performance, "GET requests for queries"]
- GraphQL over POST is not cached by most HTTP caches. [derived from RFC 9110 §9.2.3 and RFC 9111 §2]
- Sensitive data in HTTP caches should be cached privately or not at all. [graphql.org/learn/security, "Transport layer security"]

N+1:

- Each field has a single-purpose resolver; a naive service can therefore be "chatty". [graphql.org/learn/performance, "The N+1 Problem"]
- The common fix is batching, for example Facebook's DataLoader. [graphql.org/learn/performance, "The N+1 Problem"]

Security / demand control [graphql.org/learn/security]:

- Trusted documents: an allowlist of operations, stored by hash at build time; the server runs only known IDs. They "can't be used for public APIs", because third-party operations are not known in advance.
- Paginate list fields to cap items per request.
- Limit query depth; use a smaller limit for nested lists, which can grow results exponentially.
- Limit breadth: top-level fields, aliases, and operations per batch.
- Rate-limit in the business logic layer, because a request's cost isn't known from counting requests.
- Query complexity analysis: give fields weights and reject requests over a budget. The GraphQL spec gives no guidance on this; there is a community-maintained draft spec for cost directives.
- Introspection may be disabled for first-party APIs, but that alone is "security through obscurity".
- Hide detailed error messages in production; schema shape can be inferred from them.
- Cursor-based pagination is recommended; offset pagination has performance and security downsides on large data sets. [graphql.org/learn/pagination]

Versioning stance:

- "GraphQL takes a strong opinion on avoiding versioning." New types and fields can be added without breaking changes, because clients only get what they ask for. [graphql.org/learn/schema-design, "Versioning"]
- Nothing prevents versioning a GraphQL API. [graphql.org FAQ, "How does versioning work in GraphQL?"]
- Fields can be marked `@deprecated`; deprecated fields still work. [GraphQL spec §3.6.2; graphql.org/learn/introduction, "Evolve your API without versioning"]
- Any change that makes a previously valid request invalid is a breaking change; services are encouraged to avoid them. [GraphQL spec §5, "Type System Evolution"]
- Every GraphQL field is nullable by default, so one failed field becomes null instead of failing the whole request. [graphql.org/learn/schema-design, "Nullability"]

Subscriptions transport:

- GraphQL does not specify a transport for subscriptions; in practice they use WebSockets or server-sent events, with community-maintained specs for each. [graphql.org/learn/subscriptions]
- Subscriptions are typically backed by a separate publish/subscribe system. [graphql.org/learn/subscriptions]

## 5. Side by side

"Derived" cells follow from the cited facts; no source states them in those words.

| | REST (as used over HTTP) | gRPC | GraphQL |
|---|---|---|---|
| What it is | An architectural style [Fielding 2000 ch. 5] | An RPC framework [grpc.io About] | A query language and execution engine [GraphQL spec, Introduction] |
| Transport | REST is not tied to one protocol [Fielding 2008]; HTTP is the protocol it was applied to [RFC 9110 §9.1] | HTTP/2 [gRPC HTTP/2 protocol]; gRPC-Web runs over any HTTP version [gRPC-Web protocol] | No transport required [GraphQL spec §6]; HTTP most common [GoH, Introduction] |
| How you address work | A URI per resource, plus a standard method [RFC 9110 §3.1, §9.1] | `POST /<Service>/<Method>` [gRPC HTTP/2 protocol, "Requests"] | One endpoint, usually `/graphql`; the operation is in the body or query string [GoH §2, §4] |
| Payload format | Any media type [Fielding 2000 §5.2.1.2]; FastAPI uses JSON by default [FastAPI Custom Response] | Protobuf by default; JSON and others possible [grpc.io Introduction; grpc.io FAQ] | No required format; JSON most common [GraphQL spec §7.2]; JSON is mandatory over HTTP [GoH §3] |
| Contract / IDL | None in REST itself; OpenAPI describes HTTP APIs [OAS §2] | `.proto` files (Protobuf IDL) [grpc.io Core concepts] | Schema in GraphQL's IDL; queryable by introspection [GraphQL spec §3, §4] |
| Code generation | From an OpenAPI Description [OAS §2] | `protoc` plus gRPC plugin [grpc.io Core concepts, "Using the API"] | Tools may generate client code from the IDL [GraphQL spec §3] |
| Response shape | Decided by the server per endpoint [GraphQL spec §1] | Fixed by the `.proto` message [grpc.io Core concepts] | Chosen by the client, field by field [GraphQL spec §1, §2.5] |
| Streaming | Not a REST constraint; REST is pull-based [Fielding 2000 §5.4]. Over HTTP, SSE gives server push [HTML §9.2.1] | Unary, server, client and bidirectional streaming [grpc.io Core concepts] | Subscriptions; transport unspecified, WebSockets or SSE in practice [GraphQL spec §2.4; graphql.org/learn/subscriptions] |
| Browser support | Native over HTTP (derived). Fielding's model application "exactly matches" a hypermedia browser, though REST does not assume browsers [Fielding 2000 §5.3.3] | Only via gRPC-Web and a proxy; unary and server streaming only [grpc-web README] | Plain HTTP POST/GET with JSON [GoH §4]; mind CSRF and preflight [GoH §6.2.3] |
| HTTP caching | GET responses are what caches store [RFC 9110 §9.2.3; RFC 9111 §2] | None from generic HTTP caches, because every call is POST (derived from gRPC HTTP/2 protocol; RFC 9111 §2); gRPC-Web caching not yet specified [gRPC-Web protocol] | Possible with GET plus persisted documents [graphql.org/learn/performance]; POST is not cached by most caches (derived from RFC 9110 §9.2.3); client caches keyed by global IDs [graphql.org/learn/caching] |
| Error model | HTTP status codes, five classes [RFC 9110 §15] | 17 gRPC status codes in trailers; HTTP status is 200 [gRPC status codes doc; gRPC HTTP/2 protocol] | `errors` list in the body, partial `data` possible [GraphQL spec §7.1]; HTTP status per GoH [GoH §5.4] |
| Evolution | Not covered by the REST sources read (see Open questions) | Add fields freely; never reuse field numbers [protobuf.dev proto3 guide] | Avoid versions; add fields, deprecate old ones [graphql.org/learn/schema-design; GraphQL spec §3.6.2] |
| Python library | FastAPI, which generates OpenAPI [FastAPI Features; FastAPI First Steps] | `grpcio` and `grpcio-tools` [grpc.io Python Quick start] | Strawberry, recommended by FastAPI's docs [FastAPI How-to: GraphQL] |

## 6. Payload size: what the sources say

Exact facts:

- JSON is a text format. [RFC 8259 §1] Every object member is a name (a string) and a value. [RFC 8259 §4] So every field name travels as text in every object, in every message. [derived from RFC 8259 §4]
- Protobuf's binary format uses field numbers, not names, as keys. [protobuf.dev Encoding, "Message Structure"]
- A field number 1–15 plus its wire type fits in one tag byte. [protobuf.dev proto3 guide, "Assigning Field Numbers"]
- 150 as a varint is 2 bytes; the whole one-field message is 3 bytes: `08 96 01`. [protobuf.dev Encoding, "A Simple Message", "Base 128 Varints"]
- Fields at their default value (implicit presence) are not sent at all. [protobuf.dev proto3 guide, "Default Field Values"]
- Fields that are not set are left out. [protobuf.dev Encoding, "Missing Elements"]
- Protobuf is not always smaller: a negative `int32` takes 10 varint bytes. [protobuf.dev Encoding, "Signed Integers"]
- ProtoJSON is bigger than binary Protobuf "except in rare cases". [protobuf.dev ProtoJSON Format, "Non-goals of the Format"]
- Protobuf does not compress messages. [protobuf.dev Overview, "When Is Protobuf Not a Good Fit?"] gRPC can compress each message (for example gzip). [gRPC HTTP/2 protocol, "Requests"]
- JSON, being mostly text, "compresses exceptionally well" with gzip, deflate and brotli; graphql.org encourages gzip. [graphql.org/learn/performance, "JSON (with GZIP)"]
- gRPC adds a 5-byte prefix per message [derived from gRPC HTTP/2 protocol, "Requests"]; each HTTP/2 frame adds a 9-octet header [RFC 9113 §4.1]; headers are HPACK-compressed [RFC 7541 Abstract].
- A GraphQL response contains only the requested fields, so its size depends on the query. [derived from GraphQL spec §1, §2.5]
- Sending a persisted document's hash instead of the query text reduces request size. [graphql.org/learn/performance, "GET requests for queries"]

Worked byte counts, using the encodings the protobuf.dev Encoding page gives and the same data as compact JSON (no whitespace). The JSON counts are UTF-8 byte lengths, measured with Python's `len(s.encode("utf-8"))`. This is arithmetic, not a benchmark. [derived from protobuf.dev Encoding and RFC 8259 §4, §8.1]

| Message | Protobuf bytes | Protobuf size | JSON | JSON size |
|---|---|---|---|---|
| `Test1 { int32 a = 1 }`, a = 150 | `08 96 01` | 3 | `{"a":150}` | 9 |
| `Test2 { string b = 2 }`, b = "testing" | `12 07 74 65 73 74 69 6e 67` | 9 | `{"b":"testing"}` | 15 |
| `Test3 { Test1 c = 3 }`, c.a = 150 | `1a 03 08 96 01` | 5 | `{"c":{"a":150}}` | 15 |
| `Test1`, a = -2 (`int32`) | 1 tag byte + 10 varint bytes | 11 | `{"a":-2}` | 8 |

- The last row shows Protobuf can be larger than JSON for negative `int32` values; `sint32` avoids this. [derived from protobuf.dev Encoding, "Signed Integers"]
- Real field names are longer than `a`, which grows the JSON side only. [derived from protobuf.dev Encoding, "Message Structure"; RFC 8259 §4]

Unsupported common claims:

- No primary source read gives a general ratio such as "Protobuf is N× smaller" or "gRPC is 7× faster than REST". protobuf.dev says only "smaller and faster", without numbers. [protobuf.dev Overview] grpc.io's benchmarking page measures gRPC against itself across languages, not against REST. [grpc.io Benchmarking guide]
- Real numbers for our own messages will come from the script planned for `examples/api/`.

## 7. When to use each (as the official sources frame it)

REST:

- Designed for "large-grain hypermedia data transfer", the common case of the Web. [Fielding 2000 §5.1.5]
- Suited to an "Internet-scale, multi-organization, anarchically scalable information system", because intermediaries can understand the requests. [Fielding 2000 §6.5.2]
- Emphasizes scalability, generality of interfaces, independent deployment, and intermediaries. [Fielding 2000 §5.5]
- Not optimal for other forms of interaction. [Fielding 2000 §5.1.5]

gRPC:

- Polyglot microservices; connecting services in and across data centers. [grpc.io About]
- Low-latency, highly scalable distributed systems; mobile clients to cloud servers. [grpc.io FAQ, "Why would I want to use gRPC?"]
- Browser clients are listed as a scenario [grpc.io About], but only through gRPC-Web and a proxy, without client or bidirectional streaming. [grpc-web README]
- Use streams for long-lived flows of data, not as a default. [grpc.io Performance Best Practices, "General"]
- Avoid Protobuf for messages over a few megabytes, or where a formal standard is required. [protobuf.dev Overview, "When Is Protobuf Not a Good Fit?"]

GraphQL:

- Driven by the needs of views and front-end engineers. [GraphQL spec §1]
- Aggregating data from multiple UI components; static types; fewer breaking changes. [graphql.org FAQ, "Why should I use GraphQL?"]
- With microservices, graphql.org recommends one GraphQL schema as an API gateway in front of them, rather than clients calling many GraphQL services. [graphql.org FAQ, "Is GraphQL the right fit for designing a microservice architecture?"]
- GraphQL does not necessarily replace REST; the two can co-exist, for example REST behind a GraphQL server. [graphql.org FAQ, "Does GraphQL replace REST?"]
- Public APIs cannot rely on trusted documents; they need depth, breadth, pagination, rate and complexity limits instead. [graphql.org/learn/security, "Trusted documents"]
- FastAPI's docs: GraphQL "solves some very specific use cases"; weigh the benefits against the drawbacks. [FastAPI How-to: GraphQL]

Browser / public API vs service-to-service. No source gives this table; each cell is derived from the cited facts.

| | Browser or public API | Service-to-service (inside our system) |
|---|---|---|
| REST | Fits: HTTP, cacheable GETs, intermediaries, many independent organizations [Fielding 2000 §5.5, §6.5.2; RFC 9111 §2] | Works; costs some efficiency [Fielding 2000 §5.1.5] |
| gRPC | Needs gRPC-Web, a proxy, limited streaming [grpc-web README] | grpc.io's primary scenario [grpc.io About; grpc.io FAQ] |
| GraphQL | Fits front ends that need flexible shapes [GraphQL spec §1]; public APIs need demand control instead of trusted documents [graphql.org/learn/security] | graphql.org positions it as one gateway in front of microservices, not as the link between them [graphql.org FAQ] |

## 8. Python side

REST: FastAPI

- Package: `fastapi`; the docs install it with `uv add "fastapi[standard]"`. [fastapi.tiangolo.com home page]
- FastAPI is based on OpenAPI and JSON Schema, and generates interactive docs (Swagger UI and ReDoc). [FastAPI Features, "Based on open standards", "Automatic docs"]
- The OpenAPI schema is served at `/openapi.json`; the interactive docs at `/docs`. [FastAPI First Steps]
- Returns JSON by default. [FastAPI Custom Response]
- Errors: raise `HTTPException` with a 4xx code. [FastAPI Handling Errors]
- Docs: https://fastapi.tiangolo.com/

gRPC: grpcio, grpcio-tools, protobuf

- Install `grpcio`, and `grpcio-tools` for code generation. [grpc.io Python Quick start, "gRPC", "gRPC tools"]
- `grpcio-tools` includes the protocol buffer compiler `protoc` and the plugin that generates server and client code. [grpc.io Python Quick start, "gRPC tools"]
- Generate code with `python -m grpc_tools.protoc -I<dir> --python_out=. --pyi_out=. --grpc_python_out=. <file>.proto`. [grpc.io Python Basics tutorial, "Generating client and server code"]
- Output: `<name>_pb2.py` (message classes) and `<name>_pb2_grpc.py` (a `...Stub` for clients, a `...Servicer` base class, and `add_...Servicer_to_server`). [grpc.io Python Basics tutorial, "Generating client and server code"]
- The "2" in `pb2` is the Protocol Buffers Python API version, not proto2 vs proto3. [grpc.io Python Basics tutorial, Note]
- Messages serialize with `SerializeToString()` and parse with `ParseFromString()`. [protobuf.dev Protobuf Basics: Python]
- The Protobuf runtime on PyPI is the `protobuf` package. [pypi.org/project/protobuf]
- The quick start lists Python 3.7 or higher. [grpc.io Python Quick start, "Prerequisites"] (page last modified 2024-11-25)
- Python caution: streaming RPCs are much slower than unary; asyncio may help; avoid the future API. [grpc.io Performance Best Practices, "Python"]
- Docs: https://grpc.io/docs/languages/python/ and https://protobuf.dev/

GraphQL: Strawberry

- FastAPI can mount any ASGI-compatible GraphQL library next to normal path operations. [FastAPI How-to: GraphQL]
- FastAPI lists Strawberry, Ariadne, Tartiflette and Graphene (via starlette-graphene3). [FastAPI How-to: GraphQL, "GraphQL Libraries"]
- FastAPI recommends Strawberry because its design is closest to FastAPI's (type annotations). [FastAPI How-to: GraphQL, "GraphQL with Strawberry"]
- Install: `pip install 'strawberry-graphql[fastapi]'`; mount with `strawberry.fastapi.GraphQLRouter`. [strawberry.rocks FastAPI integration]
- Docs: https://strawberry.rocks/docs and https://fastapi.tiangolo.com/how-to/graphql/

## Open questions

- **Size and speed ratios.** No primary source gives numbers for JSON vs Protobuf size or REST vs gRPC speed. Our `examples/api/` script will measure size for our own messages.
- **"REST" in our pages.** Fielding's strict definition requires hypertext-driven APIs [Fielding 2008]; most FastAPI-style JSON APIs with fixed paths do not meet it (derived). The owner should decide whether pages say "REST" or "HTTP/JSON API (REST-style)".
- **REST and versioning.** The REST sources read (Fielding 2000 ch. 5–6, Fielding 2008, RFC 9110) do not give a versioning stance comparable to GraphQL's. Not researched further.
- **Webhooks standard.** No IETF RFC for generic webhooks was found in this research, but no exhaustive search was done. W3C WebSub (a hub-based pattern) is a W3C Recommendation; Standard Webhooks is a community spec.
- **GraphQL status 294.** Not IANA-registered; how real proxies and caches handle it is unknown. [GoH §6.1]
- **Persisted documents.** graphql.org says standardizing them in GraphQL-over-HTTP is underway [graphql.org/learn/security]; the September 2026 edition mentions them only in a note. [GoH §5.3]
- **graphql.org vs GoH.** graphql.org's "Serving over HTTP" page has not caught up with the September 2026 edition (400 vs 422; "draft" status).
- **GraphQL subscription transports.** The community specs for WebSockets and SSE were not read.
- **gRPC-Web future.** Whether browsers will ever run native gRPC (the "1-2 years" prediction) is unresolved.
- **FastAPI and OAS 3.2.** FastAPI's tutorial shows OpenAPI 3.1.0; whether current FastAPI can emit 3.2 was not checked.
- **gRPC Python prerequisite.** The quick start says Python 3.7+; the page was last modified 2024-11-25 and may be stale.
- **Not researched:** gRPC over HTTP/3, the Connect protocol, gRPC JSON transcoding, Strawberry's DataLoader support, current package versions on PyPI (the PyPI JSON API timed out for most packages).
- **UTF-8 byte counts.** That an ASCII character is one byte in UTF-8 was checked by running Python, not by reading the UTF-8 RFC (RFC 3629).

## Sources

All read on 2026-11-22.

REST and HTTP:

- Fielding, R. T. (2000). Dissertation, Chapter 1 "Software Architecture": https://ics.uci.edu/~fielding/pubs/dissertation/software_arch.htm
- Fielding, R. T. (2000). Chapter 5 "Representational State Transfer (REST)": https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm
- Fielding, R. T. (2000). Chapter 6 "Experience and Evaluation": https://ics.uci.edu/~fielding/pubs/dissertation/evaluation.htm
- Fielding, R. T. (2008). "REST APIs must be hypertext-driven", Untangled blog, 20 Oct 2008: https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven
- RFC 9110, HTTP Semantics (June 2022, STD 97): https://www.rfc-editor.org/rfc/rfc9110.txt
- RFC 9111, HTTP Caching (June 2022, STD 98): https://www.rfc-editor.org/rfc/rfc9111.txt
- RFC 8259, The JavaScript Object Notation (JSON) Data Interchange Format (December 2017): https://www.rfc-editor.org/rfc/rfc8259.txt
- OpenAPI Specification v3.2.1 (10 September 2026), the latest listed on spec.openapis.org: https://spec.openapis.org/oas/latest.html (version index: https://spec.openapis.org/oas/)
- FastAPI docs, Features: https://fastapi.tiangolo.com/features/
- FastAPI docs, Tutorial "First Steps": https://fastapi.tiangolo.com/tutorial/first-steps/
- FastAPI docs, Advanced "Custom Response": https://fastapi.tiangolo.com/advanced/custom-response/
- FastAPI docs, Tutorial "Handling Errors": https://fastapi.tiangolo.com/tutorial/handling-errors/
- FastAPI docs, home page (installation): https://fastapi.tiangolo.com/
- FastAPI docs, How-to "GraphQL": https://fastapi.tiangolo.com/how-to/graphql/

gRPC and Protobuf:

- grpc.io, Introduction to gRPC (last modified 2024-11-12): https://grpc.io/docs/what-is-grpc/introduction/
- grpc.io, Core concepts, architecture and lifecycle (last modified 2026-05-11): https://grpc.io/docs/what-is-grpc/core-concepts/
- grpc.io, FAQ (last modified 2025-03-17; states latest release v1.85.0): https://grpc.io/docs/what-is-grpc/faq/
- grpc.io, About gRPC: https://grpc.io/about/
- grpc.io, Python Quick start (last modified 2024-11-25): https://grpc.io/docs/languages/python/quickstart/
- grpc.io, Python Basics tutorial (last modified 2024-11-25): https://grpc.io/docs/languages/python/basics/
- grpc.io, Web platform page and Web Basics tutorial: https://grpc.io/docs/platforms/web/ , https://grpc.io/docs/platforms/web/basics/
- grpc.io, Deadlines guide (last modified 2025-07-07): https://grpc.io/docs/guides/deadlines/
- grpc.io, Cancellation guide (last modified 2024-02-29): https://grpc.io/docs/guides/cancellation/
- grpc.io, Status Codes guide (last modified 2024-08-21): https://grpc.io/docs/guides/status-codes/
- grpc.io, Performance Best Practices (last modified 2024-11-12): https://grpc.io/docs/guides/performance/
- grpc.io, Benchmarking guide: https://grpc.io/docs/guides/benchmarking/
- grpc.io blog, "gRPC Motivation and Design Principles" (Louis Ryan, 2015-09-08): https://grpc.io/blog/principles/
- grpc.io blog, "The state of gRPC in the browser" (Johan Brandhorst, guest post, 2019-01-08; dated, background only): https://grpc.io/blog/state-of-grpc-web/
- gRPC over HTTP2 protocol, `doc/PROTOCOL-HTTP2.md`, grpc/grpc master (last commit 2025-04-17): https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md
- gRPC Web protocol, `doc/PROTOCOL-WEB.md`, grpc/grpc master (last commit 2023-03-17): https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-WEB.md
- gRPC status codes, `doc/statuscodes.md`, grpc/grpc master (last commit 2023-10-06): https://github.com/grpc/grpc/blob/master/doc/statuscodes.md
- grpc-web README, grpc/grpc-web master (latest release 2.1.1, 2026-08-27): https://github.com/grpc/grpc-web
- protobuf.dev, Overview: https://protobuf.dev/overview/
- protobuf.dev, Language Guide (proto 3): https://protobuf.dev/programming-guides/proto3/
- protobuf.dev, Encoding (examples assume Edition 2023 or later): https://protobuf.dev/programming-guides/encoding/
- protobuf.dev, ProtoJSON Format: https://protobuf.dev/programming-guides/json/
- protobuf.dev, Protobuf Basics: Python: https://protobuf.dev/getting-started/pythontutorial/
- protobuf.dev, Protobuf Compiler Installation: https://protobuf.dev/installation/
- PyPI, `protobuf` project: https://pypi.org/project/protobuf/
- RFC 9113, HTTP/2 (June 2022; obsoletes RFC 7540 and 8740): https://www.rfc-editor.org/rfc/rfc9113.txt
- RFC 7541, HPACK: Header Compression for HTTP/2 (May 2015): https://www.rfc-editor.org/rfc/rfc7541.txt

GraphQL:

- GraphQL specification, September 2026 edition (released 2026-11-12; newest release listed on spec.graphql.org; previous: September 2025, October 2021): https://spec.graphql.org/September2026/ (index: https://spec.graphql.org/)
- GraphQL over HTTP specification, September 2026 edition (released 2026-11-13; the first released edition; a working draft also exists): https://graphql.github.io/graphql-over-http/September2026/ (index: https://graphql.github.io/graphql-over-http/)
- graphql.org/learn, Introduction: https://graphql.org/learn/introduction/
- graphql.org/learn, Execution: https://graphql.org/learn/execution/
- graphql.org/learn, Serving over HTTP: https://graphql.org/learn/serving-over-http/
- graphql.org/learn, Caching: https://graphql.org/learn/caching/
- graphql.org/learn, Performance: https://graphql.org/learn/performance/
- graphql.org/learn, Security: https://graphql.org/learn/security/
- graphql.org/learn, Pagination: https://graphql.org/learn/pagination/
- graphql.org/learn, Schema Design: https://graphql.org/learn/schema-design/
- graphql.org/learn, Best Practices: https://graphql.org/learn/best-practices/
- graphql.org/learn, Subscriptions: https://graphql.org/learn/subscriptions/
- graphql.org, FAQ: https://graphql.org/faq/
- Strawberry docs, home and FastAPI integration: https://strawberry.rocks/docs , https://strawberry.rocks/docs/integrations/fastapi

Other styles:

- RFC 5531, RPC: Remote Procedure Call Protocol Specification Version 2 (May 2009): https://www.rfc-editor.org/rfc/rfc5531.txt
- SOAP Version 1.2 Part 1: Messaging Framework (Second Edition), W3C Recommendation 27 April 2007: https://www.w3.org/TR/soap12-part1/
- JSON-RPC 2.0 Specification (origin 2010-03-26, updated 2013-01-04): https://www.jsonrpc.org/specification
- RFC 6455, The WebSocket Protocol (December 2011): https://www.rfc-editor.org/rfc/rfc6455.txt
- HTML Living Standard, §9.2 Server-sent events (last updated 22 November 2026): https://html.spec.whatwg.org/multipage/server-sent-events.html
- Standard Webhooks, site and spec v1.0.0 (community spec): https://www.standardwebhooks.com/ , https://github.com/standard-webhooks/standard-webhooks/blob/main/spec/standard-webhooks.md
- WebSub, W3C Recommendation 02 June 2026: https://www.w3.org/TR/websub/
- AsyncAPI Specification 3.1.0: https://www.asyncapi.com/docs/reference/specification/latest
- tRPC docs, Introduction: https://trpc.io/docs
