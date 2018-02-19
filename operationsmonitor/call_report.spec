<?xml version="1.0" encoding="utf-8"?>
<script xmlns="http://iptego.de/palladion/script-spec"
        name="Call Report"
        description="This script will provide a summary report on all calls over a given timeframe"
        result-type="custom"
    filename="app-results.csv">
        <param-spec>
                <param name="days" label="Days (subtract)" type="number" required="no"/>
                <param name="weeks" label="Weeks (subtract)" type="number" required="no"/>
                <param name="months" label="Months (subtract)" type="number" required="no"/>
        </param-spec>
        <result-schema>
                <column name="callid" type="VARCHAR(255)" null="true"/>
                <column name="caller" type="VARCHAR(255)" null="false"/>
                <column name="callee" type="VARCHAR(255)" null="false"/>
                <column name="start_timestamp" type="datetime" null="false" />
                <column name="end_timestamp" type="datetime" null="false" />
                <column name="duration(sec)" type="INT(11)" null="false" />
                <column name="code" type="INT(11)" null="false" />
                <column name="ingress" type="VARCHAR(255)" null="true" />
                <column name="egress" type="VARCHAR(255)" null="true" />
                <column name="pai" type="VARCHAR(255)" null="true" />
                <column name="mos_avg" type="VARCHAR(10)" null="false"/>
                <column name="state" type="VARCHAR(255)" null="false" />
                <column name="type" type="VARCHAR(255)" null="false" />
        </result-schema>
</script>