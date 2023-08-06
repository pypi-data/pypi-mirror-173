def create_zone(
        self,
        zone: str,
        zone_type: str,
        primary_ns: str = "",
        zone_transfer_protocol: str = "tcp",
        tsig_key_name: str = "",
        forwarder: str = "",
        forwarder_protocol: str = "Udp",
        dnssec_validation: bool = False,
    ):
        """Create a new primary, secondary, stub or conditionnal forwarder zone

        Args:
            zone (str): The zone to add.
                Should be either a valid domain name, an IP address or
                a network address in CIDR notation.

                Providing an IP or network address creates a reverse zone.

            zone_type (str): The type of zone to create.
                Can be primary, secondary, stub or forwarder.

            primary_ns (str, optional): Addresses of the primary name servers.

                List of comma separated IP addresses of the primary
                name server, used by Secondary or Stub zones. Can be omitted,
                in which case the primary name server is resolved recursively.

            zone_transfer_protocol (str, optional): The zone transfer protocol
                to be used by secondary zones. Can be tcp or tls.
                Defaults to tcp.

            tsig_key_name (str, optional): Name of the TSIG key to use by
                secondary zones.

            forwarder (str, optional): Address of the DNS server to be used as
                a forwarder, required when creating a Forwarder zone.

                The special value `this-server` can be used as a forwarder,
                which indicates to forward all the requests internally to this
                DNS server such that you can override the zone with records and
                rest of the zone gets resolved via This Server.

            forwarder_protocol (str, optional): The DNS transport protocol
                to be used by the Conditional Forwarder zone.

                Used when creating a Conditional Forwarder zone.
                Valid values are [Udp, Tcp, Tls, Https].
                Defaults to Udp.

            dnssec_validation (bool, optional): Whether to enable DNSSEC
                validation for a Forwarder zone.

                False by default.
        """
        url = f"{self.base_url}/zone/create"
        params = {"token": self.token, "zone": zone, "type": zone_type}

        if zone_type == "primary":
            # just need to send the zone and type
            pass

        elif zone_type == "secondary":
            if primary_ns:
                params["primaryNameServerAddresses"] = primary_ns
            if tsig_key_name:
                params["tsigKeyName"] = tsig_key_name
            params["zoneTransferProtocol"] = zone_transfer_protocol

        elif zone_type == "forwarder":
            if forwarder:
                params["forwarder"] = forwarder
            else:
                logger.error(
                    "Must pass a forwarder when creating a Conditional "
                    "Forwarder zone"
                )
                return
            params["protocol"] = forwarder_protocol
            params["dnssecValidation"] = dnssec_validation

        elif zone_type == "stub":
            if primary_ns:
                params["primaryNameServerAddresses"] = primary_ns

        else:
            logger.error(
                "Zone type must be either primary, secondary, forwarder or stub"
            )
            return

        r = self._get(url, params=params)
        if self._is_ok(r):
            logger.info(
                f"Created {zone_type} zone {r.json().get('response').get('domain')}"
            )
        else:
            logger.error(f"Failed to create zone {zone}")
            logger.debug(self._get_error_message(r))