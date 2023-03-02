# tg_futures
<h4>Телеграм бот, который показывает информацию о фьючерсах на бирже binance</h4>
<br>
<p>В этом телеграм боте реализовано несколько методов для получения информации по фьючерсам.</p>
<p><b>Что умеет:</b></p>
<ul>
<li>Вы можите получить информацию о последних 3 сделках по выбранному фьючерсу</li>
<li>Вы можите получить информацию о свечах по выбранному фьючерсу</li>
<li>Вы можите получить информацию о статистеке за 24 часа</li>
<li>Вы можите получить лучшую цену покупки/продажи</li>
<li>Добавить фьючерс в список отслеживаемых(состоит из инлайн-кнопок с названиями фьючерсов)</li>
<li>Удалить фьючерс из списка</li>
<li>При нажатии на фьючерс покажет его последнию цену на бирже</li>
<li>Так же задать оповещения по фьючерсу(можно по нескольким)</li>
</ul>
<br>
<p>Все данные беруться из бесплатного api https://fapi.binance.com/fapi/v1/</p>
<p>Бот создан на языке python, aiogram3</p>
<br>
<p>Для бота использовал бд postgresql<p>
<p>Было создано 3 таблицы<p>
<ol>
<li>futures c столбцом future для хранения названия фьючерса</li>
<li>tg_bot_user c столбцом tg_user_id для хранения tg_id пользователя</li>
<li>tg_bot_users_futures для связи многие ко многим. Два столбца: users_id там находяться id пользователей из таблицы tg_bot_user и futures_id для id фьючерсов из таблицы futures</li>
</ol>
