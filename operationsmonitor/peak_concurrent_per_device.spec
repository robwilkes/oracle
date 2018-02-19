<?xml version="1.0" encoding="utf-8"?>
<script xmlns="http://iptego.de/palladion/script-spec"
        name="Peak Concurrent (per device)"
        description="This script will find peak concurrent calls per device over a given relative timeframe"
        result-type="custom"
    filename="app-results.csv">
        <param-spec>
                <param name="days" label="Days (subtract)" type="number" required="no"/>
                <param name="weeks" label="Weeks (subtract)" type="number" required="no"/>
        </param-spec>
        <result-schema>
        		<column name="device" type="VARCHAR(255)" null="false" />
                <column name="total" type="BIGINT(20)" null="false" />
                <column name="peak" type="BIGINT(20)" null="false" />
                <column name="mos_avg" type="VARCHAR(10)" null="false" />
        </result-schema>
</script>