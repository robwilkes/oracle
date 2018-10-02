<?xml version="1.0" encoding="utf-8"?>
<script xmlns="http://iptego.de/palladion/script-spec"
        name="Peak Concurrent (per CUC) - Absolute"
        description="This script will find peak concurrent calls per Customer Unique Code (CUC) over a given timeframe"
        result-type="custom"
    filename="app-results.csv">
        <param-spec>
                <param name="start_ts" label="Started after" type="datetime" required="yes"/>
                <param name="end_ts" label="Started before" type="datetime" required="yes"/>
        </param-spec>
        <result-schema>
        	<column name="cuc" type="VARCHAR(255)" null="false" />
                <column name="inbound" type="BIGINT(20)" null="false" />
                <column name="outbound" type="BIGINT(20)" null="false" />
                <column name="total" type="BIGINT(20)" null="false" />
                <column name="peak" type="BIGINT(20)" null="false" />
                <column name="peak_timestamp" type="datetime" null="false" />
                <column name="avg_dur" type="BIGINT(20)" null="false" />
                <column name="call_min" type="BIGINT(20)" null="false" />
                <column name="mos_avg" type="VARCHAR(10)" null="false" />
        </result-schema>
</script>