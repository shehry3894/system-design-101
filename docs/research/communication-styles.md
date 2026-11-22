# Research: communication styles (hub)

Scope: how the 15 items in a video the owner shared (REST, SOAP, gRPC, GraphQL, webhooks, WebSocket, WebRTC, MCP, RPC, SSE, MQTT, AMQP, event-driven, Kafka, AsyncAPI) are classified by their own sources; one cited fact sheet for the items that [api-styles.md](api-styles.md) does not cover; and a check of the video's claims.
Out of scope: deep comparisons inside the push and messaging groups (each gets its own note later), WebRTC media internals, Kafka and RabbitMQ operations, MCP security.

Every claim is followed by its source in brackets. Sources read on 2026-11-23. RFCs were read as plain text from rfc-editor.org. The video is a topic list, never a source.

Labels used in this note:

- "derived from …" means the claim follows from the cited facts, but no source states it in those words.
- "(vendor, cross-check)" marks a vendor page.
- "(project claim)" marks a project's marketing statement about itself.

## Terms

Full names:
MQTT = Message Queuing Telemetry Transport (the name of the OASIS technical committee; the 5.0 spec body does not expand the letters) [MQTT 5.0, title page];
AMQP = Advanced Message Queuing Protocol [AMQP 1.0 Part 0, title];
OASIS = the standards body that publishes MQTT 5.0 and AMQP 1.0 [MQTT 5.0, title page; AMQP 1.0 Part 0, title page];
IoT = Internet of Things, M2M = Machine to Machine [MQTT 5.0, Abstract];
QoS = Quality of Service [MQTT 5.0, Abstract];
WebRTC = Real-Time Communication in browsers [W3C WebRTC, title];
NAT = Network Address Translation; ICE, STUN and TURN are the NAT-traversal technologies WebRTC uses [W3C WebRTC §1];
TURN = Traversal Using Relays around NAT, STUN = Session Traversal Utilities for NAT [RFC 8656, title];
JSEP = JavaScript Session Establishment Protocol [RFC 9429, title];
SDP = Session Description Protocol [RFC 8825 §1];
SIP = Session Initiation Protocol [RFC 9429 §1.1, cites RFC 3261];
MCP = Model Context Protocol, LLM = large language model [MCP spec, Overview];
LSP = Language Server Protocol [MCP spec, Overview];
RPI = Remote Procedure Invocation [microservices.io RPI; EIP Integration Styles];
EIP = *Enterprise Integration Patterns* (Hohpe and Woolf) [enterpriseintegrationpatterns.com];
EDA = event-driven architecture [Azure EDA];
ONC RPC = Open Network Computing Remote Procedure Call [RFC 5531, Abstract];
WS-RM = Web Services Reliable Messaging [WS-RM 1.2, title].

## 1. The umbrella term

- **Communication style** is the name microservices.io gives to the pattern group that answers "How do services in a microservice architecture communicate?". The group holds two patterns: Remote Procedure Invocation and Messaging. [microservices.io RPI; microservices.io Messaging; both pages live under `/patterns/communication-style/`]
- **Remote Procedure Invocation**: "The client uses a request/reply-based protocol to make requests to a service." Examples: REST, gRPC, Apache Thrift. [microservices.io RPI]
  - Drawback stated there: synchronous communication means tight runtime coupling; client and service must both be available for the whole request. [microservices.io RPI]
- **Messaging**: services exchange messages over messaging channels, asynchronously. Examples: Apache Kafka, RabbitMQ. [microservices.io Messaging]
  - Benefits: loose runtime coupling; better availability, because the broker buffers messages until the consumer can process them. [microservices.io Messaging]
  - Drawback: a message broker adds complexity and must be highly available. Request/reply over messaging is more complex. [microservices.io Messaging]
  - Five styles of asynchronous communication: request/response, notifications, request/asynchronous response, publish/subscribe, publish/asynchronous response. [microservices.io Messaging]
- **Integration styles** is the older name in EIP: File Transfer, Shared Database, Remote Procedure Invocation and Messaging. [EIP Integration Styles]
- **Server push** as a group is not named by either source. It is this repo's grouping: the server starts the message to a client that is already known (derived from the push mechanisms in §3).

## 2. Request-response: the RPC family

REST, gRPC, GraphQL, SOAP and JSON-RPC are covered in [api-styles.md](api-styles.md). New facts:

- **RPC model.** The remote procedure call model is similar to a local procedure call. "One thread of control logically winds through two processes": the caller sends a call message and waits (blocks) for a reply. [RFC 5531 §4]
  - RPC is a family name, not one protocol: ONC RPC [RFC 5531], XML-RPC [XML-RPC spec], JSON-RPC 2.0 [api-styles.md §1] and gRPC [api-styles.md §3] are members (derived from each spec calling itself an RPC protocol).
- **XML-RPC.** "A Remote Procedure Calling protocol that works over the Internet." A message is an HTTP POST request with an XML body; the return value is also XML. Spec dated 15 June 1999, by Dave Winer, last updated 30 June 2003. [XML-RPC spec]
- **SOAP and reliability.** SOAP 1.2 deliberately omits from its messaging framework features such as "reliability", "security", "correlation", "routing" and message exchange patterns; they are left to extensions. [SOAP 1.2 Part 1 §1]
  - Reliable delivery is a separate spec: WS-ReliableMessaging 1.2 (OASIS Standard, 2 February 2009) transfers messages reliably "in the presence of software component, system, or network failures". [WS-RM 1.2, Abstract]
  - SOAP over email exists as a W3C Note (3 July 2002), not a Recommendation. [SOAP 1.2 Email Binding]
- **MCP (Model Context Protocol).** "An open protocol that enables seamless integration between LLM applications and external data sources and tools." [MCP spec, Overview]
  - It uses JSON-RPC 2.0 messages between hosts (LLM applications), clients (connectors inside the host) and servers (services that provide context and capabilities). [MCP spec, Overview]
  - It takes inspiration from the Language Server Protocol. [MCP spec, Overview]
  - Standard transports: stdio (newline-delimited messages to a client-launched subprocess) and Streamable HTTP (each message is an HTTP POST to one MCP endpoint; replies come as a JSON object or a request-scoped SSE stream). [MCP Transports]
  - Versions are dates (`YYYY-MM-DD`) marking the last backwards-incompatible change. The current protocol version is 2026-07-28. [MCP Versioning]
  - Anthropic open-sourced MCP on 25 November 2024. [Anthropic, "Introducing the Model Context Protocol"]
  - So MCP is a member of the RPC family, built for AI tools (derived from MCP spec, Overview).

## 3. Server push

Webhooks, SSE and WebSocket are covered in [api-styles.md §1](api-styles.md). New facts:

- **SSE reconnects by itself.** An `EventSource` has a reconnection time (implementation-defined, "probably in the region of a few seconds") and a last event ID. On reconnect the browser sends the ID in the `Last-Event-ID` header. [HTML §9.2.2, §9.2.3, §9.2.4]
- **SSE and proxies.** "Legacy proxy servers are known to, in certain cases, drop HTTP connections after a short timeout." The spec advises a comment line (starting with `:`) about every 15 seconds. [HTML §9.2.7]
- **SSE connection limit.** Clients with HTTP's per-server connection limit "might run into trouble" when several pages of one site each open an `EventSource`. [HTML §9.2.7]
- **WebSocket data.** The handshake is an HTTP `GET` with `Upgrade: websocket`; the server answers `101 Switching Protocols`. Data frames are text (UTF-8) or binary (meaning left to the application). [RFC 6455 §1.2, §5.6]
- **WebRTC.**
  - The W3C spec (Recommendation, 13 March 2025) defines browser APIs for sending media and generic data "to and received from another browser or device". [W3C WebRTC, Abstract]
  - It covers connecting to remote peers "using NAT-traversal technologies such as ICE, STUN, and TURN". [W3C WebRTC §1]
  - `RTCPeerConnection` sets up peer-to-peer communication with another browser or endpoint. [W3C WebRTC §4.1]
  - **Signaling is the application's job.** WebRTC call setup controls the media plane, "leaving signaling-plane behavior up to the application as much as possible", for example SIP or a custom protocol. [RFC 9429 §1.1]
  - Session setup typically runs "over TLS-secured web technologies using application-specific protocols". [RFC 8825 §1]
  - **Relays.** Behind some NATs a host cannot reach a peer directly; it must use "an intermediate node that acts as a communication relay" (TURN). [RFC 8656, Abstract]
  - Multi-party RTP topologies include central Selective Forwarding Middleboxes. [RFC 7667 §3.7]
  - So a WebRTC app still needs a server for signaling, and often a TURN relay (derived from RFC 9429 §1.1 and RFC 8656).

## 4. Messaging

- **Event-driven architecture (EDA)** is an architecture style: event producers, event consumers, and event channels (often brokers) between them. [Azure EDA]
  - "A producer doesn't know which consumers are listening." Consumers are decoupled from each other. [Azure EDA]
  - Two models: publish-subscribe (no durable log; new subscribers don't see past events) and event streaming (events written to an ordered, durable log that clients read from any position). [Azure EDA]
  - When not to use it: when synchronous calls meet the latency and throughput needs; when business transactions need strong consistency across services, because EDA brings eventual consistency; when the team lacks experience running asynchronous systems. [Azure EDA]
- **MQTT.**
  - "A Client Server publish/subscribe messaging transport protocol. It is light weight, open, simple, and designed to be easy to implement." Suited to constrained environments such as M2M and IoT. [MQTT 5.0, Abstract]
  - Version 5.0 is an OASIS Standard of 7 March 2019. [MQTT 5.0, title page]
  - Three QoS levels: "At most once" (loss can occur), "At least once" (duplicates can occur), "Exactly once". [MQTT 5.0, Abstract]
  - It runs over TCP/IP, or over other network protocols that provide ordered, lossless, bi-directional connections. [MQTT 5.0, Abstract]
  - Every packet starts with a fixed header of byte 1 (packet type and flags) and byte 2 onward (remaining length). [MQTT 5.0 §2.1.1]
  - `PINGREQ` has remaining length 0, no variable header and no payload, so it is 2 bytes (derived from MQTT 5.0 §3.12).
  - Invented by Andy Stanford-Clark (IBM) and Arlen Nipper (Arcom, now Eurotech) in 1999. [mqtt.org FAQ]
- **AMQP 1.0.**
  - "An open internet protocol for business messaging": a binary wire-level protocol for the reliable exchange of messages between two parties. [AMQP 1.0 Part 0, Abstract]
  - OASIS Standard 29 October 2012; also ISO/IEC 19464. [AMQP 1.0 Part 0, title page; amqp.org]
  - Layered: type system, transport, message format, transactions (Part 4 groups interactions within atomic transactions), security. [AMQP 1.0 Part 0, Abstract]
- **RabbitMQ** (a broker, not a protocol).
  - Originally developed for AMQP 0-9-1. For new applications the RabbitMQ team recommends AMQP 1.0. [RabbitMQ Protocols]
  - "Despite the name, AMQP 1.0 is a very different protocol from AMQP 0-9-1 / 0-9 / 0-8, sharing nothing at the wire level." [RabbitMQ Protocols]
  - Also speaks MQTT 3.1, 3.1.1 and 5.0, and STOMP, through plugins. [RabbitMQ Protocols]
  - AMQP 0-9-1 model: publishers send to exchanges; exchanges copy messages to queues by rules called bindings; consumers read from queues. [RabbitMQ AMQP concepts]
  - With acknowledgements on, the broker removes a message only after the consumer acknowledges it. [RabbitMQ AMQP concepts]
- **Apache Kafka.**
  - "An event streaming platform": publish and subscribe to streams of events, store them, and process them. [Kafka intro]
  - Servers and clients talk over "a high-performance TCP network protocol". [Kafka intro]
  - "Events are not deleted after consumption." Retention is a per-topic setting; old events are discarded after it. [Kafka intro]
  - "Kafka's performance is effectively constant with respect to data size." Topics are partitioned across brokers. [Kafka intro]
  - Project claims: "network limited throughput … latencies as low as 2ms"; clusters "up to a thousand brokers, trillions of messages per day". [Kafka home (project claim)]
  - LinkedIn and Uber are on Kafka's "Powered By" page. [Kafka Powered By]

## 5. Describing APIs (not a way to communicate)

- **OpenAPI** describes HTTP APIs; **AsyncAPI** describes message-driven APIs for any protocol and "is not itself a wire protocol". [api-styles.md §1]

## 6. The video's claims, checked

| # | Claim in the video | Verdict | Source |
|---|---|---|---|
| 1 | gRPC is "7 to 10 times faster than REST" | **No source.** grpc.io's benchmarking page has no REST comparison. | grpc.io Benchmarking |
| 2 | "GitHub's entire API is built on GraphQL" | **Wrong.** GitHub documents a REST API and a GraphQL API. | GitHub REST docs; GitHub GraphQL docs |
| 3 | GraphQL "stands for graph query language" | **No source.** The spec never expands the name; it calls GraphQL "a query language and execution engine". | GraphQL spec Sept 2026, Introduction |
| 4 | GraphQL was created by Facebook | **Holds.** Created in 2012; developed at Facebook; now governed by the GraphQL Foundation. | GraphQL spec Sept 2026; graphql.org FAQ |
| 5 | SOAP has built-in reliability; "guaranteed delivery" | **Wrong for core SOAP.** SOAP 1.2 omits reliability; WS-ReliableMessaging is a separate OASIS spec. | SOAP 1.2 Part 1 §1; WS-RM 1.2 |
| 6 | SOAP can run over SMTP or TCP | **Holds**, but the email binding is only a W3C Note. | SOAP 1.2 Part 1, Abstract; SOAP Email Binding |
| 7 | WebRTC needs "no server in the middle" | **Partly wrong.** Signaling is left to the app's own server; TURN relays when a direct path fails; multi-party calls can use central forwarding boxes. | RFC 9429 §1.1; RFC 8656; RFC 7667 §3.7 |
| 8 | SSE "works through firewalls without any special configuration" | **Partly wrong.** The spec warns that legacy proxies drop idle connections, and advises a comment every 15 s. | HTML §9.2.7 |
| 9 | SSE reconnects automatically and resumes by event ID | **Holds.** | HTML §9.2.3, §9.2.4 |
| 10 | The smallest MQTT message is 2 bytes | **Holds** (`PINGREQ`). | MQTT 5.0 §3.12 |
| 11 | AMQP is MQTT's "older sibling" | **No source.** MQTT dates from 1999; the AMQP pages read give no origin year. | mqtt.org FAQ |
| 12 | AMQP supports transactions | **Holds.** | AMQP 1.0 Part 0 (Part 4) |
| 13 | RabbitMQ is "the most popular implementation" of AMQP | **Not checked.** Note: RabbitMQ was built for AMQP 0-9-1, which shares nothing on the wire with AMQP 1.0, the standard. | RabbitMQ Protocols |
| 14 | Kafka keeps messages as long as configured | **Holds.** | Kafka intro |
| 15 | Kafka handles "millions of messages per second" | **No per-second figure found.** The project claims "trillions of messages per day". | Kafka home (project claim) |
| 16 | MCP came out in late 2024 | **Holds.** 25 November 2024. | Anthropic announcement |
| 17 | WebSocket can send text, JSON or binary | **Holds.** Frames are text or binary; JSON is text. | RFC 6455 §5.6 |
| 18 | AsyncAPI is "like OpenAPI" for message-based systems | **Holds.** | AsyncAPI 3.1.0, Introduction |
| 19 | Event-driven services "don't even know each other exist" | **Holds** for producers and consumers. | Azure EDA |
| 20 | gRPC is behind Netflix and Uber | **Not found** in the grpc.io pages read (its About page quotes Square). | grpc.io About |
| 21 | "Every smart home device uses" MQTT | **No source.** mqtt.org names automotive, manufacturing, telecoms, oil and gas. | mqtt.org |

## 7. Classification of the 15 (derived from §1–§5)

| Item | Kind, in its own source's words | Group |
|---|---|---|
| REST | architectural style | request-response |
| gRPC | RPC framework | request-response |
| GraphQL | query language and execution engine | request-response |
| SOAP | protocol for exchanging structured information | request-response |
| RPC | the remote procedure call model (a family) | request-response |
| MCP | open protocol for LLM apps, on JSON-RPC 2.0 | request-response |
| Webhooks | HTTP callbacks (community spec) | server push |
| SSE | browser interface plus `text/event-stream` format | server push |
| WebSocket | two-way protocol over TCP | server push |
| WebRTC | browser APIs plus IETF protocols for peer-to-peer media and data | server push (peer-to-peer) |
| Event-driven | architecture style | messaging |
| MQTT | publish/subscribe messaging transport protocol | messaging |
| AMQP | binary wire-level protocol for business messaging | messaging |
| Kafka | event streaming platform | messaging |
| AsyncAPI | specification for describing message-driven APIs | describing APIs |

## Open questions

- **"Server push" as a group** is this repo's own label; neither microservices.io nor EIP uses it. The push page should say so.
- **AMQP origin year** was not found on amqp.org.
- **Fowler, "What do you mean by Event-Driven?"** returned 404 at the URL tried; not read. The Azure page stands in until it is found.
- **Kafka per-second throughput** has no primary number; the project's daily figure is a marketing claim.
- **WebRTC topologies**: RFC 7667 covers RTP in general, not WebRTC only. The push page should read the WebRTC-specific RFCs before saying more.

## Sources

- microservices.io, "Pattern: Remote Procedure Invocation (RPI)": https://microservices.io/patterns/communication-style/rpi.html
- microservices.io, "Pattern: Messaging": https://microservices.io/patterns/communication-style/messaging.html
- Enterprise Integration Patterns, "Introduction to Integration Styles": https://www.enterpriseintegrationpatterns.com/patterns/messaging/IntegrationStylesIntro.html
- RFC 5531, RPC: Remote Procedure Call Protocol Specification Version 2 (May 2009): https://www.rfc-editor.org/rfc/rfc5531.txt
- XML-RPC Specification (1999, updated 2003): http://xmlrpc.com/spec.md
- SOAP Version 1.2 Part 1, W3C Recommendation 27 April 2007: https://www.w3.org/TR/soap12-part1/
- WS-ReliableMessaging 1.2, OASIS Standard 2 February 2009: http://docs.oasis-open.org/ws-rx/wsrm/200702/wsrm-1.2-spec-os.html
- SOAP Version 1.2 Email Binding, W3C Note 3 July 2002: https://www.w3.org/TR/soap12-email
- MCP specification, Overview: https://modelcontextprotocol.io/specification/latest
- MCP specification, Transports: https://modelcontextprotocol.io/specification/latest/basic/transports
- MCP Versioning: https://modelcontextprotocol.io/specification/versioning
- Anthropic, "Introducing the Model Context Protocol", 25 November 2024: https://www.anthropic.com/news/model-context-protocol
- HTML Living Standard §9.2 Server-sent events: https://html.spec.whatwg.org/multipage/server-sent-events.html
- RFC 6455, The WebSocket Protocol (December 2011): https://www.rfc-editor.org/rfc/rfc6455.txt
- WebRTC: Real-Time Communication in Browsers, W3C Recommendation 13 March 2025: https://www.w3.org/TR/webrtc/
- RFC 8825, Overview: Real-Time Protocols for Browser-Based Applications (January 2021): https://www.rfc-editor.org/rfc/rfc8825.txt
- RFC 9429, JavaScript Session Establishment Protocol (April 2024): https://www.rfc-editor.org/rfc/rfc9429.txt
- RFC 8656, TURN (February 2020): https://www.rfc-editor.org/rfc/rfc8656.txt
- RFC 7667, RTP Topologies (November 2015): https://www.rfc-editor.org/rfc/rfc7667.txt
- Microsoft Azure Architecture Center, "Event-driven architecture style" (vendor docs): https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven
- MQTT Version 5.0, OASIS Standard 7 March 2019: https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
- mqtt.org home and FAQ: https://mqtt.org/ , https://mqtt.org/faq/
- AMQP 1.0 Part 0: Overview, OASIS Standard 29 October 2012: https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-overview-v1.0-os.html
- amqp.org home (ISO/IEC 19464): https://www.amqp.org/
- RabbitMQ, "Which protocols does RabbitMQ support?": https://www.rabbitmq.com/docs/protocols
- RabbitMQ, "AMQP 0-9-1 Model Explained": https://www.rabbitmq.com/tutorials/amqp-concepts
- Apache Kafka, Introduction: https://kafka.apache.org/intro
- Apache Kafka, home page: https://kafka.apache.org/
- Apache Kafka, Powered By: https://kafka.apache.org/powered-by
- grpc.io, Benchmarking: https://grpc.io/docs/guides/benchmarking/
- grpc.io, About: https://grpc.io/about/
- GitHub REST API docs: https://docs.github.com/en/rest
- GitHub GraphQL API docs: https://docs.github.com/en/graphql
- GraphQL specification, September 2026 edition: https://spec.graphql.org/September2026/
- graphql.org FAQ: https://graphql.org/faq/
