select *
from apartments;

select distinct district
from apartments;

select count(*), district
from apartments
group by district
order by count(*) desc;

-- Vila Mariana, Jardim Paulista, Pinheiros, Bela Vista, Consolação, Higienópolis, Paraíso, Jardins, Aclimação, Santa Cecília, Cerqueira César, Jardim América, Jardim Europa, Chácara Klabin
-- Saúde, Vila Clementino, Centro, Liberdade, Jabaquara, Vila Guarani, Planalto Paulista, Sumaré, República

select *
from (select street, district, size, rooms, bathrooms, garages, rent, condo, rent + condo as total, code
      from apartments
      where district = 'Consolação')
where total < 2500
order by size desc, total;

