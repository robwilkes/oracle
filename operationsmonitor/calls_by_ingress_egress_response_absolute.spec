<?xml version="1.0" encoding="utf-8"?>
<script xmlns="http://iptego.de/palladion/script-spec"
        name="Calls by Ingress/Egress/Response - Absolute"
        description="This script will find all the calls by corresponding ingress/egress devices"
        result-type="custom"
    filename="app-results.csv">
        <param-spec>
                <param name="start_ts" label="Started after" type="datetime" required="yes"/>
                <param name="end_ts" label="Started before" type="datetime" required="yes"/>
                <param name="ingress_devs" label="Ingress devices, comma separated" type="textarea" required="yes"/>
                <param name="egress_devs" label="Egress devices, comma separated" type="textarea" required="yes"/>
                <param name="response_codes" label="Response codes, comma separated" type="textarea" required="yes"/>
        </param-spec>
        <result-schema>
                <column name="callid" type="VARCHAR(255)" null="true"/>
                <column name="caller" type="VARCHAR(255)" null="false"/>
                <column name="callee" type="VARCHAR(255)" null="false"/>
                <column name="timestamp" type="datetime" null="false" />
                <column name="duration(sec)" type="INT(11)" null="true" />
                <column name="code" type="INT(11)" null="true" />
                <column name="state" type="VARCHAR(255)" null="false" />
                <column name="ingress" type="VARCHAR(255)" null="true" />
                <column name="egress" type="VARCHAR(255)" null="true" />
        </result-schema>
</script>