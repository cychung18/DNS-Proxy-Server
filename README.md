# DNS-Proxy-Server
We developed a DNS Server that forwards queries to upstream DNS resolver and relays answers back to clients. Besides, we implemented UDP and TCP transport protocol and transferred fabricated responses for misspelling to advertise clients.

## Testing
•	Test my DNS proxy using the nslookup command.  You will specify the IP address of the your proxy server as the resolver (as well as specifying the hostname which you are querying).

o	On Mac/Linux, you can do this with:

$ nslookup -vc domain.com [DNS_proxy_IP_address]

o	On Windows:

$ nslookup "-set vc" domain.com [DNS_proxy_IP_address]


•	Test your DNS proxy by changing the DNS server of your laptop to the IP address of your AWS instance.  This can be done in your OS network configuration.  Whenever you visit a new website (or after you clear your DNS cache) you should see DNS queries and answer flowing between your laptop and your AWS instance.  You must verify that the IP address of the DNS server matches your AWS instance.
