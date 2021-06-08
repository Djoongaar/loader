/* select p.name, r.name, c.title from projectsapp_project as p
	join projectsapp_region as r
	on p.region_id = r.id
	join projectsapp_customer as c
	on p.customer_id = c.id */

select s.origin, s.category, s.date, s.user_id, u.username, u.first_name, u.last_name, u.email from searchapp_searchrequest as s
	join auth_user as u
	on s.user_id = u.id
	

/*select * from auth_user*/

/*select type, name from tendersapp_tender where customer_inn = any(array['7722765428', '7714125897', '7826062821', '7806215195']) and type is not null*/

/*select * from tendersapp_tender where type = 'Искусственное сооружение' and category = 'Капитальный ремонт'*/