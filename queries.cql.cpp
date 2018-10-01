
//cypher query language
//eur-lex
//Pedro V


///////////////Defining the Graph///////////////

///https://s3.eu-central-1.amazonaws.com/maastrichtuniversity-ids-open/lex2rdf/cases_full.csv
///https://s3.eu-central-1.amazonaws.com/maastrichtuniversity-ids-open/lex2rdf/cases_test.csv
//Added 3392 labels, created 3392 nodes, set 20837 properties, created 14329 relationships, completed after 622188 ms.

source,target,paragraph,subject,country,case_label,ecli,case_type,judge,advocate,country-chamber,chamber,main_subject,lodge_date,document_date,year_document,month_document,year_lodge,month_lodge,case_time,n_countries,joined_cases,ruling_title,ruling_name,ruling_type,ruling_content

///short after drill query
source,target,paragraph,case_label,ecli,judge,advocate,country,lodge_date,document_date,year_document,case_time,year_lodge,ruling_name

///select, where country =1, 
///drill http://localhost:8047/

//Loading table 
LOAD CSV WITH HEADERS FROM "https://s3.eu-central-1.amazonaws.com/maastrichtuniversity-ids-open/lex2rdf/cases_iicp.csv" AS row
//Defining vertex
MERGE (src:Case {Celex: row.source, 
	Ecli: row.ecli, 
	RulingName: row.ruling_name, 
	Time: row.case_time, 
	YearDoc: toInteger(row.year_document),
	YearLodge: toInteger(row.year_lodge)
	})
MERGE (tgt:Case {
Celex: row.target})
MERGE (ct:Country {	Name: row.country})
MERGE (j:Judge {	Name: row.judge})
MERGE (a:Advocate {	Name: row.advocate})
MERGE (frag:Fragment {N: row.paragraph})
//Defining edges 
MERGE (tgt)<-[:cites]-(src)
MERGE (frag)<-[:has_fragment]-(tgt)
MERGE (j)-[:delivers_law]->(src)
MERGE (src)-[:has_advocate]->(a)
MERGE (ct)<-[:country_origin]-(src)

//ON CREATE SET src.weight = toInt(row.main_subject)
//MERGE (r)-[:Crime {Orig: toInt(row.Crim_o), Dest: toInt(row.Crim_d)}]-(y)

MATCH p=()-[r:delivers_law]->()-[:cites]-() 
MATCH q=()<-[r:has_fragment]-()
RETURN p, q LIMIT 25

MATCH (s)-[:cites]->(t) -[:has_fragment]->(f)
MATCH (a)<-[:has_advocate]-(s)<-[:delivers_law]-(j) 
MATCH (c)<-[:country_origin]-(s)
RETURN s,t,f,a,j,c LIMIT 25




///apache http://localhost:8047


///where statement to filter countries or subjects
ATCH (n)-[k:KNOWS]->(f)
WHERE k.since < 2000
RETURN f.name, f.age, f.email



/// General query
SELECT 
columns[0] as `source`
,columns[1] as `target`
,columns[2] as `paragraph`
,columns[5] as `case_label`
,columns[6] as `ecli`
,columns[8] as `judge`
,columns[9] as `advocate`
,columns[13] as `lodge_date`
,columns[14] as `document_date`
,columns[15] as `year_document`
,columns[19] as `case_time`
,columns[17] as `year_lodge`
,columns[23] as `ruling_name`
FROM dfs.`/Users/pedrohserrano/cases_full.csv` 
WHERE (columns[20]='1' 
	AND columns[7]='Judgement' 
	AND columns[3]='Intellectual; industrial and commercial property' 
	AND columns[4]='Netherlands'
	AND columns[12] ='1' 
	AND columns[15] > 2000)
ORDER BY `case_time` DESC
LIMIT 20;

/// Number of cases by subject matters
SELECT columns[3] as `subject`, COUNT(DISTINCT columns[0]) as `cases`
FROM dfs.`/Users/pedrohserrano/cases_full.csv` 
GROUP BY columns[3]
ORDER BY `cases` desc

/// Number of cases by country-chamber
SELECT columns[4] as `country`, columns[11] as `chamber`, COUNT(DISTINCT columns[0]) as `cases`
FROM dfs.`/Users/pedrohserrano/cases_full.csv` 
WHERE columns[15] > 2000 AND columns[7]='Judgement' 
GROUP BY columns[4], columns[11]
ORDER BY `cases` desc

///grouo by time of the cases



///Approximation of laws (1st with 1598 cases)
///Intellectual; industrial and commercial property (10 with 704 cases)
///Competition (Third with 1168 cases)

///All columns
columns[0] as `source`
,columns[1] as `target`
,columns[2] as `paragraph`
,columns[3] as `subject`
,columns[4] as `country`
,columns[5] as `case_label`
,columns[6] as `ecli`
,columns[7] as `case_type`
,columns[8] as `judge`
,columns[9] as `advocate`
,columns[10] as `country-chamber`
,columns[11] as `chamber`
,columns[12] as `main_subject`
,columns[13] as `lodge_date`
,columns[14] as `document_date`
,columns[15] as `year_document`
,columns[16] as `month_document`
,columns[17] as `year_lodge`
,columns[18] as `month_lodge`
,columns[19] as `case_time`
,columns[20] as `n_countries`
,columns[21] as `joined_cases`
,columns[22] as `ruling_title`
,columns[23] as `ruling_name`
,columns[24] as `ruling_type`
,columns[25] as `ruling_content`


///////////////Graph decriptive analysis///////////////


//Count vertex total
MATCH (n)  
RETURN count(n)

//Count edges total
MATCH ()-[r]->()
RETURN count(r)

//Outdegrees vertex type: Zone
MATCH (n:Zone)-[r:Move_to]->()
RETURN n.Name as Node, count(r) as Outdegree
ORDER BY Outdegree DESC
UNION
MATCH (a:Zone)-[r:Move_to]->(leaf)
WHERE not((leaf)-->())
RETURN leaf.Name as Node, 0 as Outdegree
//On the document it shows rank top 5 and last 5

//Indegrees vertex type: Zone
MATCH (n:Zone)<-[r:Move_to]-()
RETURN n.Name as Node, count(r) as Indegree
ORDER BY Indegree DESC
UNION
MATCH (a:Zone)<-[r:Move_to]-(root)
WHERE not((root)<--())
RETURN root.Name as Node, 0 as Indegree
//On the document it shows rank top 5 and last 5

//Total degrees vertex type: Zone
MATCH (n:Zone)-[r:Move_to]-()
RETURN n.Name, count(distinct r) as Degree
ORDER BY Degree DESC

//Graphs degree Histogram
MATCH (n:Zone)-[r:Move_to]-()
WITH n as Nodes, count(distinct r) as Degree
RETURN Degree, Count(Nodes)
ORDER BY Degree ASC

//Calculate the diameter of the subgraph in which only considers colonies
MATCH (z1:Zone),(z2:Zone)
WHERE z1 <> z2
WITH z1, z2
MATCH p=shortestPath((z1)-[r:Move_to*]->(z2))
RETURN z1.Name, z2.Name, length(p)
ORDER BY length(p) DESC LIMIT 1

//Since we have the the diameter then all shortest paths
MATCH p = allShortestPaths((n:Zone)-[r:Move_to*]-(m:Zone))
WHERE n.Name='Archipelbuurt' AND m.Name = 'Transvaalkwartier-Midden'
RETURN EXTRACT(n IN NODES(p)| n.Name) AS Paths


///////////////Análisis exploratorio del grafo///////////////


//Show up all relations
MATCH (o)-[:Belong]->(r)-[c:Crime]->(y) RETURN o,r,y
//Image 1 in the document

//Show up all edges which have move_to relation ordered
MATCH (n:Zone)-[:Move_to*]->(m:Zone)
RETURN n, m
ORDER BY n.Crime DESC, n.Offenders DESC
LIMIT 10
//En el documento se muestran los 5 distintos

//Show up top 10 people movement
MATCH (n:Zone)-[r:Move_to]->(m:Zone)
WHERE n<>m
RETURN n.Name, r
ORDER BY r.dist DESC, n.Crime DESC, n.Offenders DESC
LIMIT 10
//En el documento va la gráfica y el grafo, ya

//Show up the relation zone belong to region, then to see communities 
MATCH (n:Zone)-[r:Belong]->(m:Reg)
WHERE n<>m
RETURN n, m, r
ORDER BY n.Crime DESC
LIMIT 100
//Is the second graph on the document

//Dijkstras algorithm to the most influential zone
MATCH (n:Zone {Name:'Kerketuinen/Zichtenburg'}), (m:Zone),
path = shortestPath((n:Zone)-[:Move_to*]->(m:Zone))
WITH REDUCE(dist = 0, rel in rels(path) | dist + toInt(rel.dist)) AS distance, path, n, m
RETURN n, m, path, distance
ORDER BY distance desc

