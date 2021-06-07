select t.id, t.name, t.type, t.category, c.title
from tendersapp_tender as t
join projectsapp_customer as c
on t.customer_inn = c.inn
where
t.customer_inn = ANY(array[
	'7722765428', /* ГБУ Гормост + */ 
	'7806215195', /* ГБУ Мостотрест + */ 
	'7826062821', /* ФКУ УПРДОР Северо-запад */ 
	'2320100329', /* ФКУ УПРДОР Черноморье + */ 
	'7714125897', /* ФКУ УПРДОР Центравтомагистраль + */ 
	'1660049283', /* ГКУ Главтатдортранс + */
	'7728381587' /*ГКУ УДМС + */
])