select id, name, type, category 
	from tendersapp_tender where 
	/*type = 'Искусственное сооружение'*/ type is not null and
	 name ~ '(мост|Мост|путепров|Путепров|эстакад|Эстакад|Подэстакад|подэстакад|тоннел|Тоннел|переход|Переход|категорирован|Категорирован|сооружен|Сооружен|развяз|Развяз|водопропускн|Водопропускн|ТПУ|ППТ)'
