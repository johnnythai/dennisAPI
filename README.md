### Overview
Django REST framework. Asynchronous web server. Websocket.
Consumes Alpaca Trade API for account info, market data, positions, transaction history, etc.
Streams market data with Django Channels, websocket server, and Alpaca Trade Websocket.
Django Celery to handle multiple consumer connections.

#### Environment Variables
1. ALPACA_API_KEY
2. ALPACA_SECRET_KEY
3. DJANGO_SECRET_KEY

#### General
|                   | Endpoint                    | Result                     |
|:------------------|:----------------------------|:---------------------------|
|**Admin**          | /admin/                     |                            |
|**CSRF Token**     | GET /api/CSRF/              | CSRF Token                 |
|**Users**          | GET /api/users/             | List of users              |
|**Create User**    | POST /api/users/create/     |                            |
|**JWT**            | POST /api/token/            | JWT for authentication     |
|**Refresh JWT**    | GET /api/token/refresh/     |                            |


#### Alpaca
	{headers: {'Authorization': 'Bearer $JWT'}}
|                   | Endpoint             | Result                     |
|:------------------|:---------------------|:---------------------------|
|**Account Info**   | GET /api/account/    | Alpaca Account entity      |
|**Positions**      | GET /api/positions/  | Alpaca position            |
|**Orders**         | GET /api/orders/     | Alpaca orders              |
|**Portfolio**      | GET /api/portfolio/  | Alpaca portfolio history   |
|**Activities**     | GET /api/activities/ | Alpaca account activities  |
|**Market Clock**   | GET /api/clock/      | Market Clock               |

#### TODO
1. Historic Data
2. Buy/Sell Order, Order Type, Time in Force
3. Order History