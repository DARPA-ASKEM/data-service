LOAD CSV WITH HEADERS FROM 'file:///provenance.csv' AS row
with row
CALL apoc.merge.node([coalesce(row.left_type, 'Default')], 
{id :toInteger(row.left),concept:coalesce(row.concept,".")}) yield node as l
with *
CALL apoc.merge.node([row.right_type], 
{id :toInteger(row.right),concept:"."}) yield node as r
with *
CALL apoc.merge.relationship(l,row.relation_type, 
{user_id:coalesce(toInteger(row.user_id),1)},{},r,{}) yield rel 
RETURN r,l,rel