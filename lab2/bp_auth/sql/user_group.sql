select
    u_id,
    role
from
    users
where
    login = (%s)
    and passwd = (%s)
;
