select
    prod_name,
    prod_measure,
    prod_price
from
    product
where
    category_id = (%s);
