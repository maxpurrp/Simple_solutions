# Django + Stripe API
Сайт с возможностью выбрать товар и его количество и оплатить с помощью Stripe. 
Сайт имеет API с двумя методами :
```GET /buy/{id}``` 
С помощью первого метода модно получить Stripe Session id для оплаты выбранного Item. При выполнении этого метода с помощью библиотеки stripe выполняется запрос на создание id и выдается при успешном запросе. 
```GET /item/{id}```
С помощью второго метода можно получить простую HTML страницу, на которой будет указана вся информация о выбранном Item.
Так же есть кнопка добавить в заказ и купить. При нажатии на кнопку добавить в заказ, данный товар будет в числе ваших товаров, которые вы захотите купить вместе. Вы можете выбрать несколько товаров, это сформирует один заказ и будет получен платеж с общей стоимостью заказа.

## Discount
В панели администратора помимо моделей ```Item``` и ```Order``` так же описана модель ```Discount```.  С помощью нее можно добавить заказу скидку в процентом соотношении. 


## Tax

Также описана модель ```Tax```, которая прибавляет к конечной стоимости(с учетом скидки,  или без нее) налог.

## Order
Данная модель имеет 5 полей: пользователь, товары(Item), скидка, налог и общая стоимость заказа. 
Поле пользователя, товара и общей стоимости высчитываются при добавлении товаров в заказ. Поле скидки и налога нужно добавлять самостоятельно в панели админа(т.к. разным пользователям в дальнейшем могут быть доступны различные скидки). 

## Item
Модель обладает тремя полями: наименование товара, описание и стоимость. Добавление товара также происходит через панель администратора. 

## Docker
1. ```git clone https://github.com/maxpurrp/Simple_solutions```
2. ```cd  .\Simple_solutions\Solutions\```
3. ```docker  build  -t  app  .```
4. ```docker  run  -it  -p  8000:8000  app```

Or visit sebsite : http://92.118.114.138:8000/item/1/

