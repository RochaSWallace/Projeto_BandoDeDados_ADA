-- Quantas medalhas cada país conseguiu no total desde 1990?
	-- Eu realizei a contagem das medalhes agrupadas pela região, e filtrei pelo ano acima de 1990, e ordenei para ver o maior
SELECT 
	COUNT(medal.medal) AS total_medalhas, region.region 
FROM 
	medal 
JOIN 
	region 
		ON 
			medal.noc = region.noc
JOIN
	modalities
		ON 
			modalities.id = medal.modalities_id
WHERE
	modalities.year > 1990
GROUP BY 
	region.region
ORDER BY COUNT(medal.medal) DESC;


-- 2 - TOP 3 atletas que ganharam mais medalhas de ouro? TOP 3 medalhas de prata? TOP3 medalhas de bronze?
	-- Novamente fiz a contagem da melhas, agora agrupadas pelo nomes do atleta junto a classificação e limitei a 3
	-- E refiz mais duas vezes só trocando a comparação no WHERE para cada tipo de medalha
-- Top 3 Ouro
SELECT
	COUNT(medal) AS total_medal_gold, name
FROM
	athletes
JOIN
	medal
		ON
			athletes.id = medal.athletes_id
WHERE
	medal.medal = 'Gold'
GROUP BY
	athletes.name
ORDER BY
	COUNT(medal) DESC
LIMIT 3;

-- Top 3 Prata
SELECT
	COUNT(medal) AS total_medal_silver, name
FROM
	athletes
JOIN
	medal
		ON
			athletes.id = medal.athletes_id
WHERE
	medal.medal = 'Silver'
GROUP BY
	athletes.name
ORDER BY
	COUNT(medal) DESC
LIMIT 3;

-- Top 3 Bronze
SELECT
	COUNT(medal) AS total_medal_bronze, name
FROM
	athletes
JOIN
	medal
		ON
			athletes.id = medal.athletes_id
WHERE
	medal.medal = 'Bronze'
GROUP BY
	athletes.name
ORDER BY
	COUNT(medal) DESC
LIMIT 3;

-- 3 - Qual a lista de todas as modalidades existentes? A partir de que ano elas foram introduzidas nas olimpíadas?
	-- Realizei o agrupamento pelas modalidades e peguei o valor minimo de cada, o que deve ser o primeiro ano
	-- E ordenei por ordem decrescente para ver os adicionados recentemente
SELECT 
	MIN(year) AS year_inaugural, event 
FROM 
	modalities 
GROUP BY 
	event
ORDER BY
	MIN(year) DESC;

-- 4 - Quantas medalhas de ouro, prata e bronze cada país ganhou no vôlei (tanto masculino, quanto feminino)? 
-- Não é necessário mostrar países que nunca ganharam uma medalha no esporte.
	-- Essa já foi mais dificil, tentei realizar com subqueis mas não deu certo
	-- Com o CASE eu conseguir contar as medalhas individualmete e atribuilas a cada coluna
	-- realizei a filtragem por volei e filtrei novamente com HAVING pra não ter paises sem medalhas
	-- e ordenei pelo total de medalhas
SELECT 
	region.region,
	SUM(CASE WHEN medal.medal = 'Gold' THEN 1 ELSE 0 END) AS total_gold,
	SUM(CASE WHEN medal.medal = 'Silver' THEN 1 ELSE 0 END) AS total_silver,
	SUM(CASE WHEN medal.medal = 'Bronze' THEN 1 ELSE 0 END) AS total_bronze
FROM 
	medal
JOIN
	sports
	ON
		medal.modalities_id = sports.modalities_id
JOIN
	region
	ON
		sports.noc = region.noc
WHERE
	sports.sport = 'Volleyball'
GROUP BY
	region.region
HAVING
	COUNT(medal.medal) > 0
ORDER BY
	COUNT(medal.medal) DESC;

SELECT pais, 
       SUM(CASE WHEN tipo_medalha = 'gold' THEN quantidade_medalhas ELSE 0 END) AS gold,
       SUM(CASE WHEN tipo_medalha = 'silver' THEN quantidade_medalhas ELSE 0 END) AS silver,
       SUM(CASE WHEN tipo_medalha = 'bronze' THEN quantidade_medalhas ELSE 0 END) AS bronze
FROM medalhas
GROUP BY pais;


-- 5 - Qual a média de atletas por ano a partir de 1920 (separar verão de inverno).
	-- Espero ter interpretado a questão de forma correta, já que a soma total deve ser a média do ano
	-- Semelhante a questão anterior, utilizei CASE pra separar por estações e filtrei pelo ano
	-- e também garanti que não tivesse vazios nos atletas assim só precisei dividir os participantes entre estações
SELECT
	modalities.year,
	SUM(CASE WHEN modalities.season = 'Summer' THEN 1 ELSE 0 END) AS Summer,
	SUM(CASE WHEN modalities.season = 'Winter' THEN 1 ELSE 0 END) AS Winter
FROM
	athletes
JOIN
	modalities
		ON
			athletes.id = modalities.athletes_id
WHERE
	modalities.year > 1920
	AND 
	athletes.name IS NOT NULL
GROUP BY
	modalities.year
ORDER BY
	COUNT(athletes.name) DESC;

-- 6 - Proporção de homens e mulheres antes e depois de 1950 (compare e explique).

SELECT 
	COUNT(sex)
FROM
	athletes
JOIN
	modalities
		ON
			athletes.id = modalities.athletes_id
WHERE 
	modalities.year < 1950
GROUP BY
	athletes.sex;

SELECT DISTINCT sex FROM athletes;
