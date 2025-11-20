select
    u_id,
    role
from users
where login = (%(login)s) and passwd = (%(passwd)s);
