set nocount on
go

select "drop subscription " + s.subname,
  " for publication " + p.pubname,
  " with primary at PRIMARY_SERVER." + d.dbname,
  " with replicate at " + d.dsname + "." + d.dbname,
  " without purge" + char(10) + "go"
from rs_subscriptions s, rs_publications p, rs_databases d
  where p.pdbid = s.pdbid and s.dbid = d.dbid
  and p.pdbid in (123,456,789)
go
