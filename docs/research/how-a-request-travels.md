# Research: How a request travels

Scope: from typing `google.com` in a browser to the request reaching the server's front door (load balancer or gateway).
Out of scope: what happens inside the server.

Every claim is followed by its source in brackets.
RFCs were read as plain text from rfc-editor.org on 2026-11-22.

## Terms

- **IP address**: a fixed-length number that says *where* a host is; a name says *what* we seek, a route says *how to get there*. IPv4 addresses are 32 bits. [RFC 791 §2.3, "Addressing"]
- **Private address**: an address from 10/8, 172.16/12 or 192.168/16, reserved by IANA for private networks and only unique inside one enterprise. [RFC 1918 §3]
- **NAT (Network Address Translation)**: a method that maps IP addresses from one address realm to another. [RFC 2663 §3]
- **Domain name**: an ordered list of one or more labels (for example `google` and `com`). [RFC 9499 §2]
- **Registrant**: the individual or entity who registers a domain name. [https://www.icann.org/registrants]
- **Registrar**: a service provider that acts as a go-between for registrants and registries. [RFC 9499 §9]
- **Registry**: the operation that runs a zone and allows names to be registered in it, for example the operator of a TLD. [RFC 9499 §9]
- **Resolver**: a program that extracts information from name servers in response to client requests. [RFC 1034 §2.4; RFC 9499 §6]
- **Stub resolver**: a resolver that cannot do all resolution itself and depends on a recursive resolver. [RFC 9499 §6]
- **Recursive resolver**: a resolver that acts in recursive mode: it answers from cache or asks other servers until it has the final answer. [RFC 9499 §6]
- **Root server**: an authoritative name server for the DNS root zone; there are 13 named authorities (a to m). [https://www.iana.org/domains/root/servers]
- **TLD (Top-Level Domain)**: a zone one layer below the root, such as `com` or `jp`. [RFC 9499 §2]
- **Authoritative server**: a server that knows a zone's content from local knowledge and answers without asking other servers. [RFC 9499 §6, quoting RFC 2182 §2]
- **TTL (time to live)**: how long, in seconds, a DNS record may be cached before the source should be asked again. [RFC 1035 §3.2.1; RFC 9499 §5]
- **TCP**: a protocol that gives applications a reliable, in-order byte stream over IP. [RFC 9293 §2.2]
- **Port**: a number TCP uses to identify an application service and to keep separate flows apart. [RFC 9293 §2.2]
- **TLS**: a protocol that gives two peers a secure channel with authentication, confidentiality and integrity. [RFC 8446 §1]
- **HTTP request**: a message from client to server with a method and a request target, plus optional header fields and content. [RFC 9110 §3.4]
- **Gateway / reverse proxy**: an intermediary that looks like the origin server to the client but forwards requests inbound to one or more other servers. [RFC 9110 §3.7]
- **Load balancer**: no RFC defines this term. RFC 9110 lists "load balancing of HTTP services across multiple machines" as one use of a gateway. [RFC 9110 §3.7]

## 1. The client's IP address: private and public

- IANA reserved three address blocks for private networks: 10/8, 172.16/12 and 192.168/16. [RFC 1918 §3]
- Anyone can use these blocks without asking IANA or a registry. [RFC 1918 §3]
- A private address is only unique inside one enterprise. [RFC 1918 §3]
- A host with a private address cannot reach hosts outside directly. It needs a mediating gateway. [RFC 1918 §3]
- Public hosts use globally unique addresses assigned by an Internet registry. [RFC 1918 §3]
- Routers should not forward packets with private source or destination addresses between enterprises. [RFC 1918 §3]
- NAT maps addresses from one realm (private) to another (public). [RFC 2663 §3]
- Home and small-office networks often get one public address from their provider for many devices. [RFC 3022 §1]
- NAPT (the common home-router form) lets those devices share that one address by also rewriting the port. [RFC 3022 §1, §2.2]
- NAPT maps (private address, private port) to (public address, assigned port). [RFC 3022 §2.2]
- The router creates that mapping when the first outgoing packet of a session leaves. [RFC 3022 §3.1]
- It keeps the mapping while the session lives and uses it to translate every packet of that session. [RFC 3022 §3.2]
- All requests and responses of a session must pass through the same NAT router. [RFC 3022 §1]
- Cost: an IP address loses its end-to-end meaning, and the network has to hold extra state. [RFC 3022 §1]

## 2. Domain registration: registrant, registrar, registry

This happens long before your request. It is why `google.com` exists at all.

- A registrant registers a domain name. [https://www.icann.org/registrants]
- On registration, the registrant signs a contract with a registrar. [https://www.icann.org/registrants]
- The registrant must give identifying and contact details. [https://www.icann.org/resources/pages/domain-name-registration-process-2023-11-02-en]
- Registrars are responsible for registering domain names. [same ICANN page]
- Each registry is in charge of all domains under its TLD, for example `.com`. [https://www.icann.org/resources/pages/what-2012-02-25-en]
- The registry accepts registration requests, keeps the registration database, and provides name servers that publish the zone. [https://www.icann.org/resources/pages/domain-name-registration-process-2023-11-02-en]
- Contracts: ICANN signs a Registry Agreement with each registry and a Registrar Accreditation Agreement with each registrar. [https://www.icann.org/en/contracted-parties/relationship-between-domain-name-industry-parties]
- Registry and registrar sign a Registry-Registrar Agreement, which does not involve ICANN. [same ICANN page]
- Resellers can sell on behalf of a registrar; the registrar stays responsible. [same ICANN page; https://www.icann.org/resources/pages/domain-name-registration-process-2023-11-02-en]
- Registrars and registries commonly talk using EPP. [RFC 9499 §9]
- In DNS terms, the parent zone (`com`) makes a "cut" and hands control of a subtree (`google.com`) to its owner. That owner can then change its own zone freely. [RFC 1034 §4.2]

## 3. DNS resolution

The browser has a name. It needs an IP address.

### The three parts of DNS

- The name space and resource records: a tree of names with data attached. [RFC 1034 §2.4]
- Name servers: programs that hold parts of the tree. A server is an "authority" for the parts it fully knows. [RFC 1034 §2.4]
- Resolvers: programs that get information from name servers for client programs. [RFC 1034 §2.4]

### Who asks whom

- The user program calls a local resolver through a simple OS call. [RFC 1034 §2.4]
- On most machines that local resolver is a stub: it hands the work to a recursive name server. [RFC 1034 §5.3.1; RFC 9499 §6]
- The stub only needs a list of name server addresses, usually from a config file. [RFC 1034 §5.3.1]
- The stub asks with the "recursion desired" (RD) bit set. [RFC 1034 §4.3.1; RFC 9499 §6]
- In recursive mode the server returns either an error or the answer, "but never referrals". [RFC 1034 §4.3.1]
- A server not doing recursion returns the answer, an error, or a referral to a server "closer" to the answer. [RFC 1034 §4.3.1]
- A recursive resolver must know at least one root server address to start; this list ("root hints") usually ships with the software. [RFC 9499 §6]

### The walk down the tree (for `google.com`)

- The recursive resolver first checks its cache. If the answer is there, it returns it. [RFC 1034 §5.3.3, step 1]
- Otherwise it asks the best servers it knows. [RFC 1034 §5.3.3, step 2]
- A root server is authoritative for the root zone. [https://www.iana.org/domains/root/servers]
- The root does not know `google.com`. It replies with a referral to the `com` TLD servers. [RFC 9499 §4 "Referrals"; RFC 9499 §2 "TLD"]
- The `com` servers reply with a referral to the servers for `google.com`. [RFC 9499 §4 "Referrals"]
- Each referral is cached, then the resolver asks the next server. [RFC 1034 §5.3.3, step 4b]
- The `google.com` authoritative server answers from local knowledge, with the AA flag set. [RFC 9499 §6]
- The resolver caches the answer and returns it to the stub. [RFC 1034 §5.3.3, step 4a]

### Caching and TTL

- A key resolver goal is to avoid network delay by answering from its cache. [RFC 1034 §5.1]
- Shared caches (one cache for many users) work better than private ones. [RFC 1034 §5.1]
- Every record carries a TTL. [RFC 1035 §3.2.1]
- The TTL is the time a record may be cached before the source should be asked again. [RFC 1035 §3.2.1]
- A TTL of zero means "use for this transaction only, do not cache". [RFC 1035 §3.2.1]
- The zone's administrator sets the TTL. [RFC 1034 §3.6]
- Before a planned change, an admin can lower the TTL, then raise it again afterwards. [RFC 1034 §3.6]
- RFC 1035 called the TTL a signed integer by mistake; RFC 2181 fixed it to an unsigned value of at most 2^31 − 1. [RFC 9499 §5]

## 4. TCP three-way handshake and ports

The browser now has an IP address. It opens a TCP connection to it.

- TCP gives a reliable, in-order byte stream. [RFC 9293 §2.2]
- TCP sends data in segments, each inside an IP datagram. [RFC 9293 §2.2]
- TCP uses port numbers to identify services and to keep flows apart. [RFC 9293 §2.2]
- A connection is defined by a pair of sockets (address + port on each side). [RFC 9293 §3.4.1]
- For an `https` URL with no port, the default is TCP port 443, "the reserved port for HTTP over TLS". [RFC 9110 §4.2.2]
- The client's own (source) port usually comes from a high range. Port ranges: 0–1023 System, 1024–49151 User, 49152–65535 Dynamic ("Ephemeral"). [RFC 6335 §6]
- RFC 2663 notes clients "typically" pick a source port in 1024–65535, but this is not universal. [RFC 2663 §2.4]

The handshake [RFC 9293 §3.5, Figure 6]:

1. Client sends SYN with its starting sequence number (example: 100). State: SYN-SENT.
2. Server replies SYN+ACK: its own starting number (300) and ACK 101. State: SYN-RECEIVED.
3. Client sends ACK 301. Both sides are now ESTABLISHED.
4. Data can follow on the next segment.

- The ACK does not use up a sequence number ("we would wind up ACKing ACKs!"). [RFC 9293 §3.5]
- Data may ride in handshake segments, but the receiver must not deliver it until the connection is established. [RFC 9293 §3.5]

## 5. TLS 1.3 handshake (1-RTT)

TCP is up. Now the browser secures it.

- An `https` origin server must be able to set up a TLS connection secured for HTTP. [RFC 9110 §4.2.2]
- "Secured" means the server is authenticated and the traffic has confidentiality and integrity. [RFC 9110 §4.2.2]
- TLS needs only a reliable, in-order stream underneath (here: TCP). [RFC 8446 §1]
- TLS has two parts: a handshake protocol and a record protocol that protects traffic with the agreed keys. [RFC 8446 §1]
- The handshake negotiates a version, picks algorithms, authenticates, and creates shared keys. [RFC 8446 §2]

Message flow of a full handshake [RFC 8446 §2, Figure 1]:

1. Client → Server: **ClientHello**: a random nonce, offered versions, cipher options, and Diffie-Hellman key shares.
2. Server → Client: **ServerHello** with its own key share. Both sides can now derive keys. Everything after this is encrypted.
3. Server → Client (encrypted): **EncryptedExtensions**, **Certificate**, **CertificateVerify** (a signature over the handshake), **Finished** (a MAC over the handshake).
4. Client → Server: **Finished**, then the first application data (the HTTP request).

- So the client can send its request after one round trip. RFC 8446 calls this the "1-RTT" handshake. [RFC 8446 §2, Figure 1; §2.3]
- Application data must not be sent before Finished, except 0-RTT early data. [RFC 8446 §2]
- 0-RTT lets a returning client send data in the first flight using a pre-shared key, "at the cost of certain security properties". [RFC 8446 §1.2, §2.3]
- New in 1.3: all handshake messages after ServerHello are encrypted. [RFC 8446 §1.2]
- New in 1.3: all key exchanges give forward secrecy; static RSA is removed. [RFC 8446 §1.2]
- Clients should send the `server_name` extension, because servers may require it to pick a certificate. [RFC 8446 §4.4.2.2]
- The client trusts the certificate through a chain of trust from a configured trust anchor. [RFC 9110 §4.3.3]

## 6. The HTTP request and response

- HTTP is a stateless request/response protocol. [RFC 9110 §3.4]
- A request has a method and a request target, and may have header fields and content. [RFC 9110 §3.4]
- A response has a status code, and may have header fields and content. [RFC 9110 §3.4]
- The method says the purpose of the request. [RFC 9110 §9.1]
- GET asks for a current representation of the target resource. It is "the primary mechanism of information retrieval". [RFC 9110 §9.3.1]
- The `Host` header carries the host and port from the URL, so one server can serve many host names. [RFC 9110 §7.2]
- A user agent must send `Host`, unless it uses the `:authority` field (HTTP/2 and HTTP/3). [RFC 9110 §7.2]
- In HTTP/1.1, a message is: a start line, header lines, an empty line, an optional body. [RFC 9112 §2.1]
- The request line is `method SP request-target SP HTTP-version`. [RFC 9112 §3]

Example request [RFC 9110 §7.2]:

```
GET /pub/WWW/ HTTP/1.1
Host: www.example.org
```

Status codes [RFC 9110 §15]:

- Three digits, 100–599. The first digit is the class.
- 1xx informational, 2xx success, 3xx redirection, 4xx client error, 5xx server error.
- 301 means the resource has a new permanent URI; the server should send a `Location` header. [RFC 9110 §15.4.2]

## 7. Where a load balancer or gateway sits

- HTTP allows intermediaries between the user agent and the origin server. [RFC 9110 §3.7]
- The three common kinds are proxy, gateway and tunnel. [RFC 9110 §3.7]
- A request through A, B, C to the origin uses four separate connections. [RFC 9110 §3.7, Figure 2]
- A proxy is chosen by the client, usually by local configuration. [RFC 9110 §3.7]
- A gateway ("reverse proxy") acts as the origin server toward the client, then forwards requests inbound to other servers. [RFC 9110 §3.7]
- The client does not choose a gateway. It just connects to the address DNS gave it. [Inference from RFC 9110 §3.7 (gateway acts as origin server) and §7.3.3; see Open questions]
- Uses of gateways include caching ("accelerator"), shielding legacy services, and "load balancing of HTTP services across multiple machines". [RFC 9110 §3.7]
- All origin-server rules apply to a gateway's client-facing side. [RFC 9110 §3.7]
- A gateway may talk to the servers behind it using any protocol it likes. [RFC 9110 §3.7]
- A tunnel is a blind relay; it does not change messages. [RFC 9110 §3.7]
- "Inbound" means toward the origin server; "outbound" means toward the user agent. [RFC 9110 §3.7]
- Later requests may take a different path, "often based on dynamic configuration for load balancing". [RFC 9110 §3.7]

## 8. The response travels back

- The server answers with one or more response messages, each with a status code. [RFC 9110 §3.4]
- There can be zero or more 1xx interim responses, then exactly one final response. [RFC 9110 §15]
- The response flows back outbound through the same chain of connections. [RFC 9110 §3.7]
- At the home router, NAPT looks up the session's mapping and rewrites the public address and port back to the private ones. [RFC 3022 §2.2, §3.2]
- This is why every packet of a session must pass through the same NAT. [RFC 3022 §1]
- When the last session using a mapping ends, the mapping may be removed. [RFC 3022 §3.3]

## Try it

- `dig google.com +trace`
  - Traces "the delegation path from the root name servers". [dig(1) man page, BIND 9.10.6, `+[no]trace`]
  - dig makes iterative queries itself and follows referrals from the root, showing each server's answer. [dig(1)]
  - So you see root → `com` → `google.com` servers, and the final A record with its TTL.
  - Note: on 2026-11-22 this trace did not complete from the researcher's network (only a 17-byte reply came back). Some networks block direct queries to root servers.
- `curl -v https://google.com`
  - `-v` shows what happens "under the hood". [curl(1) man page, `-v, --verbose`; https://curl.se/docs/manpage.html]
  - Lines starting `>` are header data sent, `<` is header data received, `*` is extra info. [curl(1)]
  - Observed on 2026-11-22: `Connected to google.com (142.250.75.46) port 443`, then `SSL connection using TLSv1.3`, then `> GET / HTTP/2`, `> Host: google.com`, `< HTTP/2 301`, `< location: https://www.google.com/`.
  - That one run shows stages 3–6: DNS answer, TCP on port 443, TLS 1.3, HTTP request and a 301 redirect.
- `traceroute google.com`
  - Prints "the route packets take to network host". [traceroute(8) man page, macOS]
  - It sends probes with a small IP TTL (starting at 1, then increasing) and listens for ICMP "time exceeded" from each gateway. [traceroute(8)]
  - Each line shows the hop number, the gateway address and the round-trip time of each probe. A `*` means no reply within the timeout. [traceroute(8)]
  - The IP TTL here is a hop limit, not the DNS TTL from stage 3. [RFC 791 §2.3 "time to live"; traceroute(8)]

## Open questions

- **Load balancer definition.** No RFC read here defines "load balancer". RFC 9110 only names load balancing as a use of gateways. Layer-4 (TCP-level) load balancers that never parse HTTP are not covered by RFC 9110 §3.7. Need an authoritative source if the page wants to distinguish L4 and L7.
- **Client does not choose the gateway.** Stated as an inference from RFC 9110 §3.7 and §7.3.3. Not a direct quote.
- **Which DNS record types the browser asks for** (A, AAAA, HTTPS/SVCB). Not researched. RFC 9460 would be the source for HTTPS records.
- **Browser and OS caches before the stub resolver.** RFC 1034 §5.3.3 says check "local information" first, but browser-specific DNS caches are not in any RFC read here.
- **IPv6.** This note covers IPv4 private addresses and NAT only. IPv6 (RFC 4291, RFC 8200) is not covered.
- **HTTP/2 and HTTP/3.** curl negotiated HTTP/2 via ALPN. ALPN (RFC 7301) and HTTP/2 (RFC 9113) and QUIC/HTTP/3 (RFC 9000, RFC 9114) were not read. With HTTP/3, stages 4 and 5 merge (QUIC runs over UDP), which is not verified here.
- **SNI.** `server_name` is defined in RFC 6066 §3, which was not read. Only RFC 8446 §4.4.2.2 was read.
- **Root server count.** IANA lists 13 named authorities backed by "hundreds of servers". The anycast mechanism behind that was not researched.
- **Cloudflare cross-check.** https://www.cloudflare.com/learning/dns/what-is-dns/ returned HTTP 403 to the fetch tool. No vendor cross-check was done.

## Sources

- RFC 791, Internet Protocol: https://www.rfc-editor.org/rfc/rfc791.txt
- RFC 1034, Domain Names: Concepts and Facilities: https://www.rfc-editor.org/rfc/rfc1034.txt
- RFC 1035, Domain Names: Implementation and Specification: https://www.rfc-editor.org/rfc/rfc1035.txt
- RFC 1918, Address Allocation for Private Internets: https://www.rfc-editor.org/rfc/rfc1918.txt
- RFC 2663, NAT Terminology and Considerations: https://www.rfc-editor.org/rfc/rfc2663.txt
- RFC 3022, Traditional NAT: https://www.rfc-editor.org/rfc/rfc3022.txt
- RFC 6335, IANA port number procedures: https://www.rfc-editor.org/rfc/rfc6335.txt
- RFC 8446, TLS 1.3: https://www.rfc-editor.org/rfc/rfc8446.txt
- RFC 9110, HTTP Semantics: https://www.rfc-editor.org/rfc/rfc9110.txt
- RFC 9112, HTTP/1.1: https://www.rfc-editor.org/rfc/rfc9112.txt
- RFC 9293, TCP: https://www.rfc-editor.org/rfc/rfc9293.txt
- RFC 9499, DNS Terminology: https://www.rfc-editor.org/rfc/rfc9499.txt
- ICANN, Information for Domain Name Registrants: https://www.icann.org/registrants
- ICANN, The Domain Name Registration Process: https://www.icann.org/resources/pages/domain-name-registration-process-2023-11-02-en
- ICANN, Relationship Between Domain Name Industry Parties: https://www.icann.org/en/contracted-parties/relationship-between-domain-name-industry-parties
- ICANN, What Does ICANN Do?: https://www.icann.org/resources/pages/what-2012-02-25-en
- IANA, Root Servers: https://www.iana.org/domains/root/servers
- curl manual: https://curl.se/docs/manpage.html
- Local man pages: dig(1) (BIND 9.10.6), traceroute(8) (macOS)
- Attempted, failed (403): https://www.cloudflare.com/learning/dns/what-is-dns/
