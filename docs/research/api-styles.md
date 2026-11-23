# Research: API styles

Scope: which API styles exist; how REST, gRPC and GraphQL compare (features, strengths and weaknesses, when to use each for browser/public APIs vs service-to-service, payload format and size: JSON vs Protocol Buffers); the Python libraries we will use for each.
Out of scope: auth design beyond which header carries credentials (§9.2), API gateways, service meshes, HTTP/3, GraphQL federation, gRPC load balancing, and benchmark numbers (our own script, `examples/communication/request_payload_size.py`, measures sizes).

Every claim is followed by its source in brackets. Sources read on 2026-11-22; §9 was read on 2026-11-23. RFCs were read as plain text from rfc-editor.org. Editions and versions are listed under Sources.

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
- Real numbers for our own messages come from `examples/communication/request_payload_size.py`: one order is 143 bytes as JSON and 40 bytes as Protobuf.

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

## 9. Rework facts (2026-11-23): more compare rows, snippets, analogies

Sources for this section were read on 2026-11-23. Facts already in §1–8 are not repeated. Short names used here:

- **code.proto** = `google/rpc/code.proto` in the googleapis/googleapis repository (Google's API definitions, not the gRPC docs).
- **gRPC HTTP mapping doc** = `doc/http-grpc-status-mapping.md` in grpc/grpc.
- **gRPC health doc** = `doc/health-checking.md` in grpc/grpc.
- **gRPC Python API** = the gRPC Python API reference at grpc.github.io, v1.85.0.
- **grpcurl README** = the README of fullstorydev/grpcurl.

### 9.1 gRPC status codes

- The count (17, numbered 0–16) is in §3. The guide adds: "Applications should only use values defined below." [grpc.io Status Codes guide, "Overview"]
- Names, numbers and meanings [grpc.io Status Codes guide, "The full list of status codes"]:
  - `OK` (0): "Not an error; returned on success."
  - `INVALID_ARGUMENT` (3): "The client specified an invalid argument." It means the argument is bad "regardless of the state of the system (e.g., a malformed file name)".
  - `DEADLINE_EXCEEDED` (4): "The deadline expired before the operation could complete." For operations that change state, it may be returned "even if the operation has completed successfully".
  - `NOT_FOUND` (5): "Some requested entity (e.g., file or directory) was not found."
  - `PERMISSION_DENIED` (7): "The caller does not have permission to execute the specified operation." It must not be used when the caller cannot be identified; use `UNAUTHENTICATED` then.
  - `UNAVAILABLE` (14): "The service is currently unavailable." It is "most likely a transient condition", fixed by retrying with a backoff, but retrying non-idempotent operations is not always safe.
  - `UNAUTHENTICATED` (16): "The request does not have valid authentication credentials for the operation."
- An HTTP status for each gRPC code: **Not found** in the grpc.io Status Codes guide or in `doc/statuscodes.md`. [grpc.io Status Codes guide; gRPC status codes doc]
- code.proto calls its enum "The canonical error codes for gRPC APIs" and adds an "HTTP Mapping" comment to each code. [code.proto, `enum Code`]
  - `OK` → 200 OK; `INVALID_ARGUMENT` → 400 Bad Request; `DEADLINE_EXCEEDED` → 504 Gateway Timeout; `NOT_FOUND` → 404 Not Found; `PERMISSION_DENIED` → 403 Forbidden; `UNAVAILABLE` → 503 Service Unavailable; `UNAUTHENTICATED` → 401 Unauthorized. [code.proto]
  - The rest: `CANCELLED` → 499 Client Closed Request; `UNKNOWN`, `INTERNAL`, `DATA_LOSS` → 500; `ALREADY_EXISTS`, `ABORTED` → 409; `RESOURCE_EXHAUSTED` → 429; `FAILED_PRECONDITION`, `OUT_OF_RANGE` → 400; `UNIMPLEMENTED` → 501. [code.proto]
  - 499 is not defined in RFC 9110. [RFC 9110 §15, §18.3]
  - This mapping lives in Google's repository, not in the gRPC protocol documents. [derived from code.proto and the gRPC docs above]
- The gRPC HTTP mapping doc covers the opposite direction only: a client that gets an HTTP response **without** a `grpc-status`, for example from an intermediary such as a proxy. [gRPC HTTP mapping doc]
  - "This table is to be used _only_ for clients that received a response that did not include grpc-status." If `grpc-status` is present, it "_must_ be used". [gRPC HTTP mapping doc]
  - "Servers _must not_ use this table to determine an HTTP status code to use; the mappings are neither symmetric nor 1-to-1." [gRPC HTTP mapping doc]
  - Table: 400 → `INTERNAL`; 401 → `UNAUTHENTICATED`; 403 → `PERMISSION_DENIED`; 404 → `UNIMPLEMENTED`; 429, 502, 503, 504 → `UNAVAILABLE`; all other codes → `UNKNOWN`. A 200 without `grpc-status` is `UNKNOWN`. [gRPC HTTP mapping doc]
  - So the two tables disagree on purpose: a proxy's 404 becomes `UNIMPLEMENTED`, not `NOT_FOUND`, and a proxy's 400 becomes `INTERNAL`, not `INVALID_ARGUMENT`. [derived from code.proto and the gRPC HTTP mapping doc]

### 9.2 Auth headers

HTTP:

- The `Authorization` header lets a user agent authenticate with an origin server, "usually, but not necessarily, after receiving a 401 (Unauthorized) response". Its value is `credentials`. [RFC 9110 §11.6.2]
- "A proxy forwarding a request MUST NOT modify any Authorization header fields in that request." [RFC 9110 §11.6.2]
- RFC 6750 example: `Authorization: Bearer mF_9.B5f-4.1JqM`. Syntax: `credentials = "Bearer" 1*SP b64token`. [RFC 6750 §2.1]
- Clients SHOULD send a bearer token in the `Authorization` header with the `Bearer` scheme; resource servers MUST support this method. [RFC 6750 §2.1]
- Anyone holding a bearer token can use it, "without demonstrating possession of a cryptographic key". [RFC 6750 Abstract]
- "Bearer tokens SHOULD NOT be passed in page URLs (for example, as query string parameters)." [RFC 6750 §5.3]
- FastAPI's `OAuth2PasswordBearer` looks for an `Authorization` header whose value is `Bearer` plus a token. Without one, it answers 401 directly. [FastAPI Security First Steps]

gRPC:

- Metadata carries "authentication credentials"; schemes such as OAuth2 or JWT can use "the standard HTTP Authorization header". [grpc.io Metadata guide, "Overview"]
- "Some of the headers, such as authorization, are generated by gRPC for you." [grpc.io Metadata guide, "Headers"]
- Servers may limit request header size, "with a default of 8 KiB suggested". [grpc.io Metadata guide, "Be Aware"]
- An OAuth token "is always part of per-call credentials". It is sent "normally as part of HTTP Authorization header", and the server usually checks it in an interceptor. [grpc.io Authentication guide, "Using OAuth token-based authentication"]
- Python: `grpc.access_token_call_credentials(access_token)` puts the token in the authorization header, for example `authorization: Bearer <access_token>`. [gRPC Python API, `access_token_call_credentials`]
- The `credentials` argument of a call is "Only valid for secure Channel". The `metadata` argument sends extra key-value pairs. [gRPC Python API, `UnaryUnaryMultiCallable.__call__`]
- The official metadata example passes pairs such as `("accesstoken", "...")` with `metadata=` over `grpc.insecure_channel`. [grpc/grpc `examples/python/metadata/metadata_client.py`]
- The official token example server expects the metadata pair `("authorization", "Bearer example_oauth2_token")` and otherwise aborts with `UNAUTHENTICATED`. [grpc/grpc `examples/python/auth/token_based_auth_server.py`]
- So a gRPC bearer token uses the same key and value shape as HTTP: key `authorization`, value `Bearer <token>`. [derived from the gRPC Python API and the token example]

GraphQL:

- "GraphQL execution should begin after authentication middleware confirms the user's identity and passes that information to the GraphQL layer." [graphql.org/learn/authorization]
- "Authorization logic should be delegated to the business logic layer, not the GraphQL layer." [graphql.org/learn/authorization, "Recap"]
- It recommends passing "a fully-hydrated user object instead of an opaque token or API key" to the business logic layer. [graphql.org/learn/authorization]
- GraphQL should sit after all authentication middleware, so it has the same session and user information as other HTTP handlers. [graphql.org/learn/serving-over-http]
- Which header carries credentials: **Not found** in graphql.org's Authorization or Serving over HTTP pages.
- GoH says only that a server MAY refuse requests "to require authentication or payment", with a relevant 4xx or 5xx code. [GoH §2] It leaves authentication to standard HTTP practice. [GoH §6.2.1]
- GoH: "The server should not make authorization decisions based on any part of the GraphQL request". [GoH §2, Note]
- Strawberry's own auth example reads `request.headers.get("Authorization", None)` in a custom context. [Strawberry Authentication guide]

### 9.3 Client timeouts over HTTP

- A request field by which the client tells the server how long it will wait: **Not found** in RFC 9110. The word "timeout" appears only in the 408 and 504 status codes and in an inactivity timeout for reusing credentials. [RFC 9110 §11.5, §15.5.9, §15.6.5]
  - 408 means the server "did not receive a complete request message within the time that it was prepared to wait". This is the server's own timer. [RFC 9110 §15.5.9]
  - 504 means a gateway or proxy "did not receive a timely response from an upstream server". [RFC 9110 §15.6.5]
- Servers usually close idle connections after a timeout; persistent connections set "no requirements on the length (or existence) of this timeout". [RFC 9112 §9.5]
- The closest standard is RFC 7240's `Prefer: wait=N`: an upper bound, in seconds, on how long the client expects processing to take. The server may then answer asynchronously (for example 202), and the preference "could be ignored". [RFC 7240 §4.3]
- So, unlike gRPC's `grpc-timeout` header (§3), an HTTP timeout is a client-library setting, not something the server is told. [derived from RFC 9110 and RFC 7240 §4.3]
- HTTPX: "HTTPX is careful to enforce timeouts everywhere by default." The default raises `TimeoutException` "after 5 seconds of network inactivity". [HTTPX Timeouts]
  - Per request: `httpx.get(url, timeout=10.0)`; `timeout=None` disables it. Per client: `httpx.Client(timeout=10.0)`. [HTTPX Timeouts]
  - There are four kinds: connect, read, write and pool. [HTTPX Timeouts, "Fine tuning the configuration"]
- Requests: "By default, requests do not time out unless a timeout value is set explicitly." [Requests docs, Advanced Usage, "Timeouts"]
  - "Nearly all production code should use this parameter in nearly all requests." [Requests docs, Quickstart, "Timeouts"]
  - The timeout is not a limit on the whole download; it fires when no bytes arrive for that many seconds. [Requests docs, Quickstart, "Timeouts"]
- FastAPI's `TestClient` "is based on HTTPX". It needs `httpx` installed, and it comes from Starlette (`starlette.testclient`). [FastAPI Testing]
- curl: `-m, --max-time <seconds>` sets the maximum time allowed for each transfer. [curl man page]
- gRPC Python: a call takes a `timeout` keyword, "An optional duration of time in seconds to allow for the RPC." [gRPC Python API, `UnaryUnaryMultiCallable.__call__`]
  - The official example calls `stub.SayHello(helloworld_pb2.HelloRequest(name=message), timeout=3)`, catches `grpc.RpcError`, and reads `rpc_error.code()`. A slow call "Should fail with DEADLINE_EXCEEDED". [grpc/grpc `examples/python/timeout/greeter_client.py`]
- Defaults side by side: gRPC sets no deadline (§3), HTTPX gives up after 5 seconds of inactivity, and Requests has no timeout at all. [derived from grpc.io Deadlines guide, HTTPX Timeouts, Requests docs]

### 9.4 Health checks

gRPC:

- "gRPC specifies a standard service API (health/v1)". An implementation is provided, but you must update the health status of your services yourself. [grpc.io Health Checking guide, "Overview"]
- The proto: package `grpc.health.v1`, service `Health`, with `rpc Check(HealthCheckRequest) returns (HealthCheckResponse);` and `rpc Watch(HealthCheckRequest) returns (stream HealthCheckResponse);`. [gRPC health doc, "Service Definition"]
- `ServingStatus` values: `UNKNOWN = 0`, `SERVING = 1`, `NOT_SERVING = 2`, `SERVICE_UNKNOWN = 3` (used only by `Watch`). [gRPC health doc, "Service Definition"]
- The request has one field, `service`. An empty string means the whole server. An unregistered service name gets a `NOT_FOUND` gRPC status. [gRPC health doc]
- A client calling `Check` should set a deadline. [gRPC health doc]
- `Check` suits central monitoring or load balancers but "does not scale" to a fleet of clients checking constantly. `Watch` streams status changes and is used by client-side health checking. [grpc.io Health Checking guide, "The Server Side Health Service"]
- A client turns on health checking in the channel's service config, for example `{"healthCheckConfig": {"serviceName": "foo"}}`. Requests wait until the service reports healthy. [grpc.io Health Checking guide, "Enabling Client Health Checking"]
- Python: the official example imports `health`, `health_pb2` and `health_pb2_grpc` from `grpc_health.v1`, creates `health.HealthServicer(...)`, registers it with `health_pb2_grpc.add_HealthServicer_to_server`, and sets status with `health_servicer.set(service, status)`. [grpc/grpc `examples/python/health_checking/greeter_server.py`]
- The pip package name: **Not found** in the grpc.io guide or the gRPC Python API page. PyPI lists `grpcio-health-checking` (1.85.3, "Standard Health Checking Service for gRPC"), whose documentation link is the gRPC Python API. [PyPI grpcio-health-checking]

REST / HTTP:

- A standard health endpoint: **Not found** in RFC 9110. The only IETF document found, "Health Check Response Format for HTTP APIs" (`draft-inadarei-api-health-check-06`), is an expired Internet-Draft, not an RFC. [IETF Datatracker]
- The Kubernetes probe example uses `httpGet` with `path: /healthz` and `port: 8080`. [kubernetes.io Probes, "Define a liveness HTTP request"]
- "Any code greater than or equal to 200 and less than 400 indicates success. Any other code indicates failure." [kubernetes.io Probes, "Define a liveness HTTP request"]
- `/healthz` is a Kubernetes convention, not a standard. Kubernetes' own API server `healthz` endpoint "is deprecated (since Kubernetes v1.16)"; use `livez` and `readyz` instead. [kubernetes.io API health endpoints]
- Kubernetes can probe gRPC directly (`livenessProbe: grpc: port: 2379`) for apps that implement the gRPC Health Checking Protocol. "Stable since Kubernetes v1.27". [kubernetes.io Probes, "Define a gRPC liveness probe"]
  - The feature gate was alpha in 1.23, beta (on by default) in 1.24–1.26, and stable in 1.27. [kubernetes.io Feature Gates (removed)]
  - An optional `service` field names "the service to place in the gRPC HealthCheckRequest". [kubernetes.io Pod v1 API, GRPCAction]
  - gRPC probes do not support named ports and connect over plaintext by default; TLS mode is alpha since v1.37. [kubernetes.io Probes]
  - `timeoutSeconds` defaults to 1s. [kubernetes.io Probes, "Define a gRPC liveness probe"]

### 9.5 Debugging tools

gRPC:

- Reflection is "a protocol that gRPC servers can use to declare the protobuf-defined APIs they export over a standardized RPC service". [grpc.io Reflection guide, "Overview"]
- "Reflection is used heavily by debugging tools such as `grpcurl` and Postman." [grpc.io Reflection guide, "Overview"]
- grpc.io compares it to serving an OpenAPI document for a REST API. [grpc.io Reflection guide, "Overview"]
- "Reflection is not automatically enabled on a gRPC server." [grpc.io Reflection guide, "Enabling Reflection on a gRPC Server"]
- For public APIs, you may not want to expose reflection, "as you may consider this a security issue". [grpc.io Reflection guide, "Tips"]
- Python: install the `grpcio-reflection` package, `from grpc_reflection.v1alpha import reflection`, then call `reflection.enable_server_reflection(SERVICE_NAMES, server)`. `SERVICE_NAMES` lists the service's full name and `reflection.SERVICE_NAME`. [grpc/grpc `doc/python/server_reflection.md`; `examples/python/helloworld/greeter_server_with_reflection.py`]
- grpcurl is "basically `curl` for gRPC servers". Plain curl can't do it because gRPC sends binary Protobuf. [grpcurl README]
- Without reflection, grpcurl needs "the proto source files that define the service" or protoset files. [grpcurl README]
- Syntax from the README [grpcurl README, "Invoking RPCs", "Adding Headers/Metadata to Request", "Listing Services"]:
  - `grpcurl -plaintext grpc.server.com:80 my.custom.server.Service/Method` (no TLS, empty body).
  - `grpcurl -d '{"id": 1234, "tags": ["foo","bar"]}' grpc.server.com:443 my.custom.server.Service/Method`. The body is JSON and is sent as binary Protobuf.
  - "all arguments must come *before* the server address and method name".
  - Headers: `-H name:value`. Listing: `grpcurl localhost:8787 list`; without reflection: `grpcurl -import-path ../protos -proto my-stuff.proto list`.
- So the page's call would be `grpcurl -plaintext -d '{"id": 42}' localhost:50051 shop.Orders/GetOrder`. [derived from grpcurl README; not run]

GraphQL:

- Introspection queries "help power GraphQL development tools", such as "documentation browsers or rich IDE experiences". [graphql.org/learn/introspection]
- Schema descriptions are "available in introspection queries and visible in developer tools such as GraphiQL". [graphql.org/learn/schema]
- GraphiQL is "An interactive in-browser GraphQL IDE." [graphql.org Tools and Libraries] With it you can explore what data an API exposes. [graphql.org FAQ, "How can I document my GraphQL API?"]
- GraphiQL is a project of the GraphQL Foundation. [graphql.org FAQ]
- For first-party APIs, introspection is "typically not needed in production", and disabling it is common. [graphql.org/learn/introspection, "Introspection in production"]
- Strawberry's `GraphQLRouter` serves GraphiQL by default (option `graphql_ide`, §9.8). [Strawberry FastAPI integration, "Options"]

REST:

- curl is "a tool for transferring data from or to a server using URLs". `-H, --header` adds a request header. [curl man page]

### 9.6 REST versioning

- Google AIP-185: "All Google API interfaces must provide a major version number, which is encoded at the end of the protobuf package, and included as the first part of the URI path for REST APIs." [AIP-185, "Guidance"]
- Only the major version is exposed: "Google APIs use `v1`, not `v1.0`, `v1.1`, or `v1.4.2`". [AIP-185, "Guidance"]
- Alpha and beta add a suffix (`v1alpha`, `v1beta`); the stable channel must not. [AIP-185, "Channel-based versioning"]
- Its scope is "the versioning strategies used by Google APIs". It is Google's rule, not an IETF standard. [AIP-185] (State: Approved; created and updated 2024-10-22.)
- AIP-180: "Renaming a component is semantically equivalent to "remove and add"", and removing a component in the same major version is not allowed. [AIP-180, "Removing or renaming components"]
- Microsoft's Azure guidelines take the opposite rule: "**DO** use a required query parameter named `api-version` on every operation", with `YYYY-MM-DD` values. [Azure REST API Guidelines, "API Versioning"]
  - "**DO NOT** include a version number segment in any operation path." [Azure REST API Guidelines, "API Versioning"]
- Microsoft Graph puts the version in the path: `{scheme}://{host}/{version}/{category}/...`, where "`version` can be v1.0 or beta". [Microsoft Graph REST API Guidelines, "Uniform Resource Locators (URLs)"]
- The older, now deprecated, Microsoft REST API Guidelines allowed both: a path segment (`/v1.0/`) or `?api-version=1.0`. "Services that cannot ensure URL path stability across future versions MUST embed the version in the URL path." [Microsoft REST API Guidelines (deprecated), §12.1]
- So there is no single authoritative REST rule; two large providers' guidelines disagree (path vs query parameter). [derived from AIP-185 and the Azure guidelines]

### 9.7 Protobuf field renames

- Binary wire: only numbers travel (§3). The proto3 guide does not list "rename a field" under "Binary Wire-safe Changes"; it mentions renaming only as an option for a removed field, e.g. with the prefix `OBSOLETE_`. [protobuf.dev proto3 guide, "Binary Wire-safe Changes"]
- An explicit "renaming is wire-safe" sentence: **Not found** in the proto3 guide. It follows from the Encoding page, where names are known only from the `.proto` file. [derived from protobuf.dev Encoding, "Message Structure"]
- "Reusing an old field name later is generally safe, except when using TextProto or JSON encodings where the field name is serialized." [protobuf.dev proto3 guide, "Reserved Field Names"]
- Text format and JSON store names as strings, so old code "will fail when a field or enum value is renamed". [protobuf.dev Proto Best Practices, "Don't use Text Format Messages for Interchange"]
- "If you use protos converted to JSON in your API or for storing data, you may not be able to safely rename fields or enums at all." [protobuf.dev Proto Best Practices, same section]
- ProtoJSON "puts field and enum value names into encoded messages which makes it much harder to change those names later". [protobuf.dev ProtoJSON Format, "Does not have as good schema-evolution guarantees as binary wire format"]
- The `json_name` option sets the JSON key; parsers accept that key and the original proto field name. [protobuf.dev ProtoJSON Format, "Field names as JSON keys"] Using `json_name` to keep an old JSON key after a rename is not stated there. [derived]
- In ProtoJSON, "Changing a field number is safe (as the field numbers are not used in the ProtoJSON format), but still strongly discouraged". [protobuf.dev ProtoJSON Format, "JSON Wire-safe Changes"]
- "Never re-use a tag number. It messes up deserialization." [protobuf.dev Proto Best Practices, "Don't Re-use a Tag Number"]
- When deleting a field, "you must reserve the deleted field number". "You should also reserve the field name to allow JSON and TextFormat encodings of your message to continue to parse." [protobuf.dev proto3 guide, "Deleting Fields"]
- Syntax: `reserved 2, 15, 9 to 11;` and `reserved "foo", "bar";`. Names and numbers cannot be mixed in one statement. [protobuf.dev proto3 guide, "Reserved Field Numbers", "Reserved Field Names"]
- Reserved names only affect `protoc`: "Runtime JSON parsing is not affected by reserved names." [protobuf.dev proto3 guide, "Reserved Field Names"]
- "Changing the field number is equivalent to deleting the field and adding a new field with the same type." [protobuf.dev proto3 guide, "Binary Wire-unsafe Changes"]
- Wire-safe changes "may be a breaking change to application code in a given language". [protobuf.dev proto3 guide, "Binary Wire-safe Changes"]

### 9.8 Snippet details

FastAPI (REST):

- Typed path parameter [FastAPI Path Parameters, "Path parameters with types"]:

  ```python
  @app.get("/items/{item_id}")
  async def read_item(item_id: int):
      return {"item_id": item_id}
  ```

- `/items/3` returns `{"item_id":3}`, a Python `int`. [FastAPI Path Parameters, "Data conversion"]
- `/items/foo` returns a `detail` list with `"type": "int_parsing"`, `"loc": ["path", "item_id"]` and `"msg": "Input should be a valid integer, unable to parse string as an integer"`. `/items/4.2` fails the same way. [FastAPI Path Parameters, "Data validation"]
- The status code for that error: **Not found** on the Path Parameters page. FastAPI's default handler for `RequestValidationError` returns `status_code=422`. [fastapi/fastapi `fastapi/exception_handlers.py`] The generated OpenAPI lists `"422"` with description "Validation Error". [FastAPI Additional Responses in OpenAPI]
- Run: `uv run fastapi dev`, which finds the app from `[tool.fastapi] entrypoint = "main:app"` in `pyproject.toml`; or `uv run fastapi dev main.py`. It serves at `http://127.0.0.1:8000`. `fastapi run` is the production command. [FastAPI First Steps]

gRPC (`grpcio`):

- The `protoc` command is unchanged from §8. [grpc.io Python Basics, "Generating client and server code"]
- Generated names follow the service name: `RouteGuideStub`, `RouteGuideServicer`, `add_RouteGuideServicer_to_server`, in `route_guide_pb2_grpc.py`. [grpc.io Python Basics, "Generating client and server code"] For a service `Orders` that would be `OrdersStub`, `OrdersServicer`, `add_OrdersServicer_to_server`. [grpc.io Python Generated-code reference, §9.11]
- The servicer subclasses the generated class: `class RouteGuideServicer(route_guide_pb2_grpc.RouteGuideServicer):`. A method is `def GetFeature(self, request, context):` and returns a message. `context` is a `grpc.ServicerContext` with information "such as timeout limits". [grpc.io Python Basics, "Implementing RouteGuide"]
- Server [grpc.io Python Basics, "Starting the server"]:

  ```python
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  route_guide_pb2_grpc.add_RouteGuideServicer_to_server(RouteGuideServicer(), server)
  server.add_insecure_port("[::]:50051")
  server.start()
  server.wait_for_termination()
  ```

- "The server `start()` method is non-blocking." `wait_for_termination()` blocks until the server stops. [grpc.io Python Basics, "Starting the server"]
- Client: `channel = grpc.insecure_channel('localhost:50051')`, `stub = route_guide_pb2_grpc.RouteGuideStub(channel)`, `feature = stub.GetFeature(point)`. The call returns a response or raises an exception. [grpc.io Python Basics, "Creating the client"] The Quick start opens the channel with `with grpc.insecure_channel('localhost:50051') as channel:`. [grpc.io Python Quick start]
- Timeout: the `timeout=` keyword (§9.3).
- Errors: on the server, `context.abort(code, details)` "Raises an exception to terminate the RPC with a non-OK status"; `code` must not be `StatusCode.OK`. On the client, `grpc.RpcError` is "Raised by the gRPC library to indicate non-OK-status RPC termination". [gRPC Python API, `ServicerContext.abort`, `RpcError`] Example: `context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid signature")`. [grpc/grpc `examples/python/auth/token_based_auth_server.py`]

Strawberry (GraphQL):

- Package: `pip install 'strawberry-graphql[cli]'` for the dev server, or `pip install 'strawberry-graphql[fastapi]'` for FastAPI. [Strawberry Getting started; Strawberry FastAPI integration]
- The Getting started tutorial assumes "a recent version of Python (3.11+)". [Strawberry Getting started]
- Getting started: `@strawberry.type` classes `Book` and `Query`; `books: typing.List[Book] = strawberry.field(resolver=get_books)`; `schema = strawberry.Schema(query=Query)`; run `strawberry dev schema`, served at `http://0.0.0.0:8000/graphql`. [Strawberry Getting started]
- FastAPI integration [Strawberry FastAPI integration]:

  ```python
  @strawberry.type
  class Query:
      @strawberry.field
      def hello(self) -> str:
          return "Hello World"

  schema = strawberry.Schema(Query)
  graphql_app = GraphQLRouter(schema)
  app = FastAPI()
  app.include_router(graphql_app, prefix="/graphql")
  ```

- The import is `from strawberry.fastapi import GraphQLRouter`. [Strawberry FastAPI integration]
- Strawberry runs sync and async fields on the event loop, so "using a sync `def` will block the entire worker"; it recommends `async def` for all fields. [Strawberry FastAPI integration, Note]
- `GraphQLRouter` options: `graphql_ide` defaults to `"graphiql"` (or `apollo-sandbox`, `pathfinder`, or `None` to turn it off); `allow_queries_via_get` defaults to `True`. [Strawberry FastAPI integration, "Options"]
- camelCase: by default Strawberry converts field names to camel case, so `example_field` becomes `exampleField`. Turn it off with `config=StrawberryConfig(auto_camel_case=False)` (`from strawberry.schema.config import StrawberryConfig`). [Strawberry Schema Configurations, "auto_camel_case"]

### 9.9 MCP analogy

- "Think of MCP like a USB-C port for AI applications." The next sentence says MCP gives AI applications a standard way to connect to external systems, as USB-C does for electronic devices. [MCP docs, "What is the Model Context Protocol (MCP)?"]
- The same page opens: MCP "is an open-source standard for connecting AI applications to external systems". [MCP docs, "What is the Model Context Protocol (MCP)?"]
- URL: https://modelcontextprotocol.io/docs/getting-started/intro , which redirects to the versioned https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro .
- This wording differs from the spec Overview wording our page quotes ("an open protocol…"). Both are MCP's own pages. [MCP docs intro; MCP spec, Overview]

### 9.10 Where each page cell comes from

The API styles page has a Design table and a Run table. Rows that repeat a §5 row cite §5. "Derived" means no source says it in those words. Order on each line: GraphQL / gRPC / REST.

Design:

- **What you design:** types and fields [GraphQL spec §3] / services and methods [grpc.io Core concepts] / resources and standard methods [RFC 9110 §3.1, §9.1]. The examples `Order.totalCents`, `Orders.GetOrder` and `GET /orders/42` come from the page's own snippets (§9.8).
- **Contract:** §5 "Contract / IDL" and "Code generation". `/openapi.json` [FastAPI First Steps].
- **Payload:** §5 "Payload format".
- **Response shape:** §5 "Response shape".
- **Call types:** query, mutation, subscription [GraphQL spec §2.4] / four call kinds [grpc.io Core concepts] / one request, one response; REST is pull-based [Fielding 2000 §5.4]; SSE for push [HTML §9.2.1].
- **Changing the API:** add fields, `@deprecated`, avoid versions [graphql.org/learn/schema-design; GraphQL spec §3.6.2] / new numbers, never reuse one (§9.7) [protobuf.dev proto3 guide] / Google path vs Azure query parameter (§9.6).

Run:

- **Transport, From a browser, HTTP caching, Python library:** §5, same rows.
- **Errors:** §5 "Error model". `NOT_FOUND` (§9.1), plus an optional message (§9.11). `404 Not Found` [RFC 9110 §15.5.5].
- **Auth:** middleware before GraphQL [graphql.org/learn/authorization] / metadata `authorization: Bearer <token>` (§9.2) / `Authorization: Bearer <token>` [RFC 6750 §2.1].
- **Timeouts:** GraphQL "same as REST", because it runs over an HTTP client (derived from §9.3) / deadline sent as `grpc-timeout`, none by default (§3) [gRPC HTTP/2 protocol; grpc.io Deadlines] / HTTPX 5 s, Requests no limit (§9.3).
- **Debugging:** GraphiQL; Strawberry serves it by default (§9.5) / grpcurl with reflection or `.proto` files (§9.5) / curl [curl man page]; a browser can send GET (derived).
- **Health checks:** GraphQL "same as REST", because a Strawberry app is a FastAPI app (derived) / `grpc.health.v1.Health` (§9.4) / no standard; Kubernetes examples use `/healthz` (§9.4).

Surprise on the page: "Changing the field number is equivalent to deleting the field and adding a new field" [protobuf.dev proto3 guide, "Binary Wire-unsafe Changes"]; names travel in JSON and text format, so renames break those [protobuf.dev Proto Best Practices] (§9.7).

### 9.11 The rest of the grpc.io guides

The owner asked whether all of grpc.io/docs was read. Until now §1–9 used 9 of its 24 guides (Authentication, Benchmarking, Cancellation, Deadlines, Health Checking, Metadata, Performance, Reflection, Status Codes), plus "What is gRPC?", the Python pages and the Web pages. The other 15 guides and the Python generated-code reference were read on 2026-11-23. Other languages and Android are out of scope (this repo uses Python).

Bearing on the API styles page:

- **Error handling.** On failure, gRPC returns "one of its error status codes instead, with an optional string error message". [grpc.io Error handling guide, "Standard error model"]
  - A "richer error model", developed by Google, sends error details as Protobuf messages in trailing metadata. Supported in C++, Go, Java, Python and Ruby. [same, "Richer error model"]
  - Proxies, loggers and other HTTP processors "don't have visibility into the error details". [same]
  - It lists the code for each failure, e.g. deadline expired → `DEADLINE_EXCEEDED`, method not found → `UNIMPLEMENTED`, server shutting down → `UNAVAILABLE`. [same, "Error status codes"] It gives no HTTP status mapping (see §9.1).
- **Compression.** Compression "can be enabled or disabled based on call or message level for all languages". A peer may answer with a different compression method, or none. An unsupported algorithm gets `UNIMPLEMENTED`, and the server lists the ones it accepts in `grpc-accept-encoding`. [grpc.io Compression guide]
  - So Protobuf does not compress itself (§6), but gRPC can compress messages on the wire. [derived from protobuf.dev Overview and the Compression guide]
- **Retry.** "Retries are enabled by default, but there is no default retry policy." Without a policy, gRPC only retries "transparently", when it is sure the server application has not seen the call. [grpc.io Retry guide, "Retry configuration"]
  - A policy is set per method in the service config: `maxAttempts`, `initialBackoff`, `maxBackoff`, `backoffMultiplier`, `retryableStatusCodes`. Backoff gets ±20% jitter, and `retryThrottling` limits retry load. [same]
  - Once response headers arrive, the call is committed and not retried. [same, "How gRPC client retry works"]
- **Request hedging.** "Hedging is one of two configurable retry policies supported by gRPC": the client sends copies of a request to different backends and uses the first response. [grpc.io Request Hedging guide]
- **Debugging.** The guide covers `grpcdebug`, which fetches a running app's internal state through admin services (Channelz, Health Checking, CSDS): how many calls were sent or failed per channel, address resolution results, and xDS configuration. It does not mention grpcurl; the Reflection guide does (§9.5). [grpc.io Debugging guide]
- **Interceptors.** For functionality that is "independent of the method being run" and applies to "all or most RPCs". Example uses: logging, metrics, server-side authentication and authorization. [grpc.io Interceptors guide]
- **Wait-for-ready.** A stub option that makes calls "wait for the server to become available before sending the request". [grpc.io Wait-for-Ready guide]
- **Service config.** It "specifies how gRPC clients should behave when interacting with a gRPC server", and service owners provide it. Retry and health-check settings live here. [grpc.io Service Config guide; grpc.io Retry guide; §9.4]
- **Python generated code.** For each service `Foo`, the generated code has `FooStub` (client), `FooServicer` (server) and `add_FooServicer_to_server` (registration). This confirms the names §9.8 derived. [grpc.io Python Generated-code reference]

Operations topics, outside this page's scope (one line each, from each guide's opening):

- Keepalive: HTTP/2 PING-based keepalives. [grpc.io Keepalive guide]
- Flow control: keeps a fast sender from overwhelming a receiver; applies to streaming. [grpc.io Flow Control guide]
- Graceful shutdown: finish in-flight calls within a time limit and accept no new ones. [grpc.io Graceful Shutdown guide]
- Custom load balancing, custom name resolution, custom backend metrics: spread calls across servers, find a service's addresses, and balance on app-specific load. [grpc.io Custom Load Balancing, Custom Name Resolution, Custom Backend Metrics guides]
- OpenTelemetry metrics: per-call and per-attempt client metrics, including retries. [grpc.io OpenTelemetry Metrics guide]

## Open questions

- **Size and speed ratios.** No primary source gives numbers for JSON vs Protobuf size or REST vs gRPC speed. Our `examples/communication/request_payload_size.py` script measures size for our own messages.
- **"REST" in our pages.** Fielding's strict definition requires hypertext-driven APIs [Fielding 2008]; most FastAPI-style JSON APIs with fixed paths do not meet it (derived). The owner should decide whether pages say "REST" or "HTTP/JSON API (REST-style)".
- **REST and versioning.** The REST sources read (Fielding 2000 ch. 5–6, Fielding 2008, RFC 9110) do not give a versioning stance comparable to GraphQL's. Provider guidelines were read on 2026-11-23 (§9.6): Google puts the major version in the path, Azure forbids that and uses an `api-version` query parameter. No standards-body rule was found.
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

Added for §9, all read on 2026-11-23:

HTTP, REST and Python HTTP clients:

- RFC 6750, The OAuth 2.0 Authorization Framework: Bearer Token Usage (October 2012): https://www.rfc-editor.org/rfc/rfc6750.txt
- RFC 9112, HTTP/1.1 (June 2022, STD 99): https://www.rfc-editor.org/rfc/rfc9112.txt
- RFC 7240, Prefer Header for HTTP (June 2014): https://www.rfc-editor.org/rfc/rfc7240.txt
- RFC 9110 (already listed above), §11.5, §11.6.2, §15.5.9, §15.6.5 read for §9.
- HTTPX docs, Timeouts: https://www.python-httpx.org/advanced/timeouts/
- Requests 2.34.2 docs, Advanced Usage and Quickstart, "Timeouts": https://requests.readthedocs.io/en/latest/user/advanced/ , https://requests.readthedocs.io/en/latest/user/quickstart/
- curl man page (describes curl 8.23.1): https://curl.se/docs/manpage.html
- FastAPI docs, Tutorial "Path Parameters": https://fastapi.tiangolo.com/tutorial/path-params/
- FastAPI docs, Tutorial "Testing": https://fastapi.tiangolo.com/tutorial/testing/
- FastAPI docs, Tutorial "Security - First Steps": https://fastapi.tiangolo.com/tutorial/security/first-steps/
- FastAPI docs, Advanced "Additional Responses in OpenAPI": https://fastapi.tiangolo.com/advanced/additional-responses/
- FastAPI source, `fastapi/exception_handlers.py`, master (last commit 2025-09-16): https://github.com/fastapi/fastapi/blob/master/fastapi/exception_handlers.py
- Google AIP-185, API Versioning (Approved; created and updated 2024-10-22): https://google.aip.dev/185
- Google AIP-180, Backwards compatibility (Approved; created and updated 2019-07-23): https://google.aip.dev/180
- Microsoft REST API Guidelines, repository README: https://github.com/microsoft/api-guidelines
- Azure REST API Guidelines, vNext (latest changelog entry 2026-Oct-22): https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md
- Microsoft Graph REST API Guidelines, vNext (last commit 2025-06-05): https://github.com/microsoft/api-guidelines/blob/vNext/graph/GuidelinesGraph.md
- Microsoft REST API Guidelines, deprecated version (last commit 2023-12-21): https://github.com/microsoft/api-guidelines/blob/vNext/graph/Guidelines-deprecated.md
- IETF Datatracker, `draft-inadarei-api-health-check-06`, "Health Check Response Format for HTTP APIs" (expired; last revision 2022-04-19): https://datatracker.ietf.org/doc/draft-inadarei-api-health-check/
- Kubernetes docs, "Configure Liveness, Readiness and Startup Probes" (last modified 2026-06-30): https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- Kubernetes docs, "Kubernetes API health endpoints" (last modified 2026-07-03): https://kubernetes.io/docs/reference/using-api/health-checks/
- Kubernetes docs, Pod v1 API reference, `GRPCAction` (last modified 2026-08-26): https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/
- Kubernetes docs, Feature Gates (removed), `GRPCContainerProbe`: https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates-removed/

gRPC and Protobuf:

- grpc.io, Metadata guide (last modified 2024-11-12): https://grpc.io/docs/guides/metadata/
- grpc.io, Authentication guide (last modified 2024-01-12): https://grpc.io/docs/guides/auth/
- grpc.io, Health Checking guide (last modified 2024-05-20): https://grpc.io/docs/guides/health-checking/
- grpc.io, Reflection guide (last modified 2026-05-11): https://grpc.io/docs/guides/reflection/
- grpc.io, Status Codes guide (already listed above; re-read for §9.1): https://grpc.io/docs/guides/status-codes/
- gRPC Python API reference, v1.85.0: https://grpc.github.io/grpc/python/grpc.html
- gRPC Python API reference, "gRPC Health Checking", v1.85.0: https://grpc.github.io/grpc/python/grpc_health_checking.html
- HTTP to gRPC status code mapping, `doc/http-grpc-status-mapping.md`, grpc/grpc master (last commit 2016-03-31): https://github.com/grpc/grpc/blob/master/doc/http-grpc-status-mapping.md
- gRPC Health Checking Protocol, `doc/health-checking.md`, grpc/grpc master (last commit 2023-04-11): https://github.com/grpc/grpc/blob/master/doc/health-checking.md
- gRPC Python Server Reflection, `doc/python/server_reflection.md`, grpc/grpc master (last commit 2023-12-15): https://github.com/grpc/grpc/blob/master/doc/python/server_reflection.md
- grpc/grpc Python examples, master: token auth client and server (last commit 2024-01-10), metadata client, timeout client (last commit 2023-06-09), health checking server (last commit 2023-06-09), reflection server (last commit 2023-06-09): https://github.com/grpc/grpc/tree/master/examples/python/auth , https://github.com/grpc/grpc/tree/master/examples/python/metadata , https://github.com/grpc/grpc/tree/master/examples/python/timeout , https://github.com/grpc/grpc/tree/master/examples/python/health_checking , https://github.com/grpc/grpc/blob/master/examples/python/helloworld/greeter_server_with_reflection.py
- googleapis, `google/rpc/code.proto`, master (last commit 2026-03-31): https://github.com/googleapis/googleapis/blob/master/google/rpc/code.proto
- grpcurl README, fullstorydev/grpcurl master (last commit 2026-08-31): https://github.com/fullstorydev/grpcurl
- PyPI, `grpcio-health-checking` project (1.85.3, uploaded 2026-11-18): https://pypi.org/project/grpcio-health-checking/
- protobuf.dev, Proto Best Practices: https://protobuf.dev/best-practices/dos-donts/
- protobuf.dev, Language Guide (proto 3), ProtoJSON Format and Encoding (already listed above; re-read for §9.7).

GraphQL:

- graphql.org/learn, Authorization: https://graphql.org/learn/authorization/
- graphql.org/learn, Introspection: https://graphql.org/learn/introspection/
- graphql.org/learn, Schemas and Types: https://graphql.org/learn/schema/
- graphql.org, Tools and Libraries: https://graphql.org/community/tools-and-libraries/
- graphql.org FAQ, Serving over HTTP and GoH (already listed above; re-read for §9.2 and §9.5).
- Strawberry docs, Getting started: https://strawberry.rocks/docs
- Strawberry docs, Schema Configurations: https://strawberry.rocks/docs/types/schema-configurations
- Strawberry docs, Authentication guide: https://strawberry.rocks/docs/guides/authentication
- Strawberry docs, FastAPI integration (already listed above; re-read for §9.8): https://strawberry.rocks/docs/integrations/fastapi

MCP:

- modelcontextprotocol.io, "What is the Model Context Protocol (MCP)?" (page metadata dateModified 2026-11-09; redirects to the 2026-07-28 docs version): https://modelcontextprotocol.io/docs/getting-started/intro

Added for §9.11, all read on 2026-11-23 (last-modified dates from each page's footer where shown):

- grpc.io, Error handling guide (2025-09-22): https://grpc.io/docs/guides/error/
- grpc.io, Compression guide (2023-05-30): https://grpc.io/docs/guides/compression/
- grpc.io, Retry guide (2025-11-26): https://grpc.io/docs/guides/retry/
- grpc.io, Request Hedging guide: https://grpc.io/docs/guides/request-hedging/
- grpc.io, Debugging guide (2024-07-04): https://grpc.io/docs/guides/debugging/
- grpc.io, Interceptors guide (2024-02-29): https://grpc.io/docs/guides/interceptors/
- grpc.io, Wait-for-Ready guide: https://grpc.io/docs/guides/wait-for-ready/
- grpc.io, Service Config guide: https://grpc.io/docs/guides/service-config/
- grpc.io, Keepalive guide: https://grpc.io/docs/guides/keepalive/
- grpc.io, Flow Control guide: https://grpc.io/docs/guides/flow-control/
- grpc.io, Graceful Shutdown guide: https://grpc.io/docs/guides/server-graceful-stop/
- grpc.io, Custom Load Balancing Policies guide: https://grpc.io/docs/guides/custom-load-balancing/
- grpc.io, Custom Name Resolution guide: https://grpc.io/docs/guides/custom-name-resolution/
- grpc.io, Custom Backend Metrics guide: https://grpc.io/docs/guides/custom-backend-metrics/
- grpc.io, OpenTelemetry Metrics guide: https://grpc.io/docs/guides/opentelemetry-metrics/
- grpc.io, Python Generated-code reference (2021-08-11): https://grpc.io/docs/languages/python/generated-code/
